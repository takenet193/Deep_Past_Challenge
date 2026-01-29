"""
Document audit script for rule violations.

Checks markdown files against the following rules:
1. File line count (300 lines max, preferably 150)
2. Heading level (### max)
3. Broken links
4. Filename-content mismatch
5. Content duplication
6. Long lines (100 chars max)

Output: JSON file with violations
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]

# Check target directories
CHECK_DIRS = [
    REPO_ROOT / "docs",
    REPO_ROOT / "knowledge",
    REPO_ROOT / "README.md",
]

# Rule thresholds
MAX_LINES = 300
PREFERRED_MAX_LINES = 150
MAX_HEADING_LEVEL = 3  # ### is level 3
MAX_LINE_LENGTH = 100


@dataclass
class LineCountViolation:
    file: str
    lines: int


@dataclass
class HeadingLevelViolation:
    file: str
    line: int
    heading: str
    level: int


@dataclass
class BrokenLink:
    file: str
    line: int
    link: str
    text: str
    link_type: str  # "markdown" or "wiki"


@dataclass
class FilenameContentMismatch:
    file: str
    reason: str


@dataclass
class ContentDuplication:
    pattern: str
    files: List[str]
    count: int


@dataclass
class LongLine:
    file: str
    line: int
    length: int
    content: str


@dataclass
class AuditResults:
    line_count_violations: List[LineCountViolation]
    heading_level_violations: List[HeadingLevelViolation]
    broken_links: List[BrokenLink]
    filename_content_mismatch: List[FilenameContentMismatch]
    content_duplication: List[ContentDuplication]
    long_lines: List[LongLine]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "line_count_violations": [asdict(v) for v in self.line_count_violations],
            "heading_level_violations": [asdict(v) for v in self.heading_level_violations],
            "broken_links": [asdict(v) for v in self.broken_links],
            "filename_content_mismatch": [asdict(v) for v in self.filename_content_mismatch],
            "content_duplication": [asdict(v) for v in self.content_duplication],
            "long_lines": [asdict(v) for v in self.long_lines],
        }


def find_markdown_files() -> List[Path]:
    """Find all markdown files to check."""
    files = []
    for check_target in CHECK_DIRS:
        if check_target.is_file():
            files.append(check_target)
        elif check_target.is_dir():
            files.extend(check_target.rglob("*.md"))
    # Exclude template files and hidden files
    files = [f for f in files if not f.name.startswith("_") and not f.name.startswith(".")]
    return sorted(files)


def check_line_count(file_path: Path) -> Optional[LineCountViolation]:
    """Check if file exceeds line count limit."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        line_count = len(lines)
        if line_count > MAX_LINES:
            rel_path = file_path.relative_to(REPO_ROOT)
            return LineCountViolation(file=str(rel_path), lines=line_count)
    except Exception:
        pass
    return None


def check_heading_levels(file_path: Path) -> List[HeadingLevelViolation]:
    """Check for heading levels deeper than ###."""
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        rel_path = file_path.relative_to(REPO_ROOT)
        
        for line_num, line in enumerate(lines, 1):
            # Match markdown headings: #, ##, ###, ####, etc.
            match = re.match(r"^(#{4,})\s+(.+)$", line.strip())
            if match:
                level = len(match.group(1))
                heading_text = match.group(2).strip()
                violations.append(
                    HeadingLevelViolation(
                        file=str(rel_path),
                        line=line_num,
                        heading=heading_text,
                        level=level,
                    )
                )
    except Exception:
        pass
    return violations


def resolve_link_path(link: str, base_file: Path) -> Optional[Path]:
    """Resolve a link path relative to the base file."""
    # Remove anchor if present
    link = link.split("#")[0]
    if not link:
        return None
    
    # Handle different link formats
    if link.startswith("http://") or link.startswith("https://"):
        return None  # External links, skip
    
    # Remove leading ./
    if link.startswith("./"):
        link = link[2:]
    
    # Resolve relative to base file's directory
    if link.startswith("../"):
        resolved = (base_file.parent / link).resolve()
    else:
        resolved = (base_file.parent / link).resolve()
    
    # Check if resolved path is within repo
    try:
        resolved.relative_to(REPO_ROOT)
        return resolved
    except ValueError:
        return None


def check_broken_links(file_path: Path) -> List[BrokenLink]:
    """Check for broken links in the file."""
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        rel_path = file_path.relative_to(REPO_ROOT)
        
        in_code_block = False
        code_block_delimiter = None
        
        for line_num, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    code_block_delimiter = line.strip()
                elif line.strip() == code_block_delimiter:
                    in_code_block = False
                    code_block_delimiter = None
                continue
            
            if in_code_block:
                continue  # Skip links in code blocks
            
            # Check markdown links: [text](path)
            markdown_link_pattern = r"\[([^\]]+)\]\(([^\)]+)\)"
            for match in re.finditer(markdown_link_pattern, line):
                link_text = match.group(1)
                link_path = match.group(2)
                resolved = resolve_link_path(link_path, file_path)
                if resolved is None or not resolved.exists():
                    violations.append(
                        BrokenLink(
                            file=str(rel_path),
                            line=line_num,
                            link=link_path,
                            text=link_text,
                            link_type="markdown",
                        )
                    )
            
            # Check wiki links: [[link]]
            wiki_link_pattern = r"\[\[([^\]]+)\]\]"
            for match in re.finditer(wiki_link_pattern, line):
                link_text = match.group(1)
                # Try different extensions
                link_paths = [
                    f"{link_text}.md",
                    f"{link_text}",
                ]
                found = False
                for link_path in link_paths:
                    resolved = resolve_link_path(link_path, file_path)
                    if resolved and resolved.exists():
                        found = True
                        break
                
                if not found:
                    violations.append(
                        BrokenLink(
                            file=str(rel_path),
                            line=line_num,
                            link=link_text,
                            text=link_text,
                            link_type="wiki",
                        )
                    )
    except Exception as e:
        print(f"Error checking links in {file_path}: {e}")
    return violations


def check_filename_content_mismatch(file_path: Path) -> Optional[FilenameContentMismatch]:
    """Check if filename matches content."""
    rel_path = file_path.relative_to(REPO_ROOT)
    filename = file_path.stem.lower()
    
    # Known problematic patterns
    if "project_architecture" in filename:
        try:
            content = file_path.read_text(encoding="utf-8").lower()
            # Check if it contains topics that should be separate files
            topics = ["ロードマップ", "roadmap", "タスク管理", "task management", "チーム運用", "team operations"]
            found_topics = [topic for topic in topics if topic in content]
            if len(found_topics) > 1:
                return FilenameContentMismatch(
                    file=str(rel_path),
                    reason=f"ロードマップ、タスク管理、チーム運用など複数のトピックが含まれている可能性: {', '.join(found_topics)}",
                )
        except Exception:
            pass
    
    # Check for generic names that might contain multiple topics
    generic_names = ["guide", "manual", "documentation", "docs"]
    if any(name in filename for name in generic_names):
        try:
            content = file_path.read_text(encoding="utf-8")
            # Count major sections (## headings)
            major_sections = len(re.findall(r"^##\s+", content, re.MULTILINE))
            if major_sections > 5:
                return FilenameContentMismatch(
                    file=str(rel_path),
                    reason=f"多数の主要セクション（{major_sections}個）が含まれており、分割を検討すべき",
                )
        except Exception:
            pass
    
    return None


def check_content_duplication(files: List[Path]) -> List[ContentDuplication]:
    """Check for duplicated content patterns across files."""
    violations = []
    
    # Patterns to check for duplication
    patterns = {
        "フォルダ構造の説明": [
            r"ディレクトリ構造",
            r"フォルダ構造",
            r"directory structure",
            r"folder structure",
        ],
        "gitignore説明": [
            r"\.gitignore",
            r"gitignore",
        ],
        "json説明": [
            r"\.json",
            r"json形式",
        ],
        "templates説明": [
            r"テンプレート",
            r"template",
        ],
        "pythonコード説明": [
            r"python.*コード",
            r"python.*script",
        ],
    }
    
    pattern_matches: Dict[str, List[str]] = defaultdict(list)
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
            rel_path = str(file_path.relative_to(REPO_ROOT))
            
            for pattern_name, pattern_list in patterns.items():
                for pattern in pattern_list:
                    if re.search(pattern, content, re.IGNORECASE):
                        pattern_matches[pattern_name].append(rel_path)
                        break
        except Exception:
            continue
    
    # Find patterns that appear in multiple files
    for pattern_name, matching_files in pattern_matches.items():
        if len(matching_files) > 1:
            violations.append(
                ContentDuplication(
                    pattern=pattern_name,
                    files=matching_files,
                    count=len(matching_files),
                )
            )
    
    return violations


def check_long_lines(file_path: Path) -> List[LongLine]:
    """Check for lines exceeding max length."""
    violations = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        rel_path = file_path.relative_to(REPO_ROOT)
        
        in_code_block = False
        code_block_delimiter = None
        
        for line_num, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    code_block_delimiter = line.strip()
                elif line.strip() == code_block_delimiter:
                    in_code_block = False
                    code_block_delimiter = None
                continue
            
            if in_code_block:
                continue  # Skip code blocks
            
            # Check line length (excluding newline)
            line_length = len(line.rstrip("\n\r"))
            if line_length > MAX_LINE_LENGTH:
                violations.append(
                    LongLine(
                        file=str(rel_path),
                        line=line_num,
                        length=line_length,
                        content=line.rstrip("\n\r")[:100] + "..." if len(line) > 100 else line.rstrip("\n\r"),
                    )
                )
    except Exception:
        pass
    return violations


def run_audit() -> AuditResults:
    """Run all audit checks."""
    print("Finding markdown files...")
    files = find_markdown_files()
    print(f"Found {len(files)} markdown files")
    
    results = AuditResults(
        line_count_violations=[],
        heading_level_violations=[],
        broken_links=[],
        filename_content_mismatch=[],
        content_duplication=[],
        long_lines=[],
    )
    
    print("\nChecking line counts...")
    for file_path in files:
        violation = check_line_count(file_path)
        if violation:
            results.line_count_violations.append(violation)
    
    print("Checking heading levels...")
    for file_path in files:
        violations = check_heading_levels(file_path)
        results.heading_level_violations.extend(violations)
    
    print("Checking broken links...")
    for file_path in files:
        violations = check_broken_links(file_path)
        results.broken_links.extend(violations)
    
    print("Checking filename-content mismatch...")
    for file_path in files:
        violation = check_filename_content_mismatch(file_path)
        if violation:
            results.filename_content_mismatch.append(violation)
    
    print("Checking content duplication...")
    results.content_duplication = check_content_duplication(files)
    
    print("Checking long lines...")
    for file_path in files:
        violations = check_long_lines(file_path)
        results.long_lines.extend(violations)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Audit markdown files for rule violations")
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output JSON file path (default: results/docs_audit_YYYYMMDDHHMMSS.json)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary to stdout",
    )
    
    args = parser.parse_args()
    
    results = run_audit()
    
    # Generate output filename
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = REPO_ROOT / "results" / f"docs_audit_{timestamp}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save results
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results.to_dict(), f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {output_path}")
    
    # Print summary
    if args.summary:
        print("\n=== Audit Summary ===")
        print(f"Line count violations: {len(results.line_count_violations)}")
        print(f"Heading level violations: {len(results.heading_level_violations)}")
        print(f"Broken links: {len(results.broken_links)}")
        print(f"Filename-content mismatches: {len(results.filename_content_mismatch)}")
        print(f"Content duplications: {len(results.content_duplication)}")
        print(f"Long lines: {len(results.long_lines)}")


if __name__ == "__main__":
    main()

