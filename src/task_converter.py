"""
タスクをMarkdown（Obsidian形式）からJSONに変換するスクリプト

Zettelkasten + GTD形式のタスクをマルチエージェントシステムが
読み取れるJSON形式に変換します。
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import frontmatter


def parse_task_markdown(file_path: Path) -> Dict:
    """
    Markdownファイルからタスク情報を抽出
    
    Args:
        file_path: タスクのMarkdownファイルパス
        
    Returns:
        タスク情報の辞書
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    metadata = post.metadata
    content = post.content
    
    # タスクIDを生成（ファイル名から、またはメタデータから）
    task_id = metadata.get('id', file_path.stem)
    
    # タイトルを抽出（メタデータまたは最初の見出しから）
    title = metadata.get('title', '')
    if not title:
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
    
    # ステータスを判定（ファイルの場所から）
    status = 'pending'
    if 'active' in str(file_path):
        status = 'active'
    elif 'waiting' in str(file_path):
        status = 'waiting'
    elif 'completed' in str(file_path):
        status = 'completed'
    elif 'inbox' in str(file_path):
        status = 'pending'
    
    # メタデータから情報を取得
    priority = metadata.get('priority', 'medium')
    project = metadata.get('project', 'general')
    context = metadata.get('context', 'general')
    due_date = metadata.get('due_date', None)
    tags = metadata.get('tags', [])
    related_notes = metadata.get('related_notes', [])
    assigned_agent = metadata.get('assigned_agent', 'planner')
    dependencies = metadata.get('dependencies', [])
    
    # 期待される成果を抽出
    expected_outcome = metadata.get('expected_outcome', {})
    
    # タスクJSONを構築
    task_json = {
        "id": task_id,
        "title": title,
        "description": content[:500] if content else "",  # 最初の500文字
        "status": status,
        "priority": priority,
        "project": project,
        "context": context,
        "due_date": due_date,
        "tags": tags if isinstance(tags, list) else [tags] if tags else [],
        "related_notes": related_notes if isinstance(related_notes, list) else [related_notes] if related_notes else [],
        "assigned_agent": assigned_agent,
        "dependencies": dependencies if isinstance(dependencies, list) else [dependencies] if dependencies else [],
        "metadata": {
            "created": metadata.get('created', datetime.now().isoformat()),
            "updated": metadata.get('updated', datetime.now().isoformat()),
            "source": str(file_path.relative_to(Path.cwd()))
        },
        "expected_outcome": expected_outcome
    }
    
    return task_json


def convert_tasks_to_json(
    knowledge_dir: Path = Path("knowledge/tasks"),
    output_dir: Path = Path("tasks"),
    status_filter: Optional[str] = None
) -> List[Dict]:
    """
    知識ベースのタスクをJSON形式に変換
    
    Args:
        knowledge_dir: タスクのMarkdownファイルがあるディレクトリ
        output_dir: JSONファイルの出力先
        status_filter: 特定のステータスのみを変換（'pending', 'active', 'waiting', 'completed'）
        
    Returns:
        変換されたタスクのリスト
    """
    tasks = []
    
    # 各ステータスディレクトリを探索
    status_dirs = {
        'pending': knowledge_dir / 'inbox',
        'active': knowledge_dir / 'active',
        'waiting': knowledge_dir / 'waiting',
        'completed': knowledge_dir / 'completed'
    }
    
    for status, status_dir in status_dirs.items():
        if status_filter and status != status_filter:
            continue
            
        if not status_dir.exists():
            continue
            
        # Markdownファイルを検索
        for md_file in status_dir.glob("*.md"):
            try:
                task_json = parse_task_markdown(md_file)
                tasks.append(task_json)
                
                # JSONファイルとして保存
                output_file = output_dir / status / f"{task_json['id']}.json"
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(task_json, f, ensure_ascii=False, indent=2)
                    
            except Exception as e:
                print(f"Error processing {md_file}: {e}")
    
    # 全タスクのインデックスファイルを作成
    index_file = output_dir / "tasks_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "tasks": tasks
        }, f, ensure_ascii=False, indent=2)
    
    return tasks


def update_task_status(
    task_id: str,
    new_status: str,
    tasks_dir: Path = Path("tasks")
) -> bool:
    """
    タスクのステータスを更新
    
    Args:
        task_id: タスクID
        new_status: 新しいステータス
        tasks_dir: タスクJSONファイルのディレクトリ
        
    Returns:
        更新が成功したかどうか
    """
    # 既存のタスクを検索
    for status_dir in ['pending', 'in_progress', 'completed']:
        task_file = tasks_dir / status_dir / f"{task_id}.json"
        if task_file.exists():
            with open(task_file, 'r', encoding='utf-8') as f:
                task = json.load(f)
            
            # ステータスを更新
            task['status'] = new_status
            task['metadata']['updated'] = datetime.now().isoformat()
            
            # 新しい場所に移動
            new_status_dir = 'pending' if new_status == 'pending' else 'in_progress' if new_status == 'active' else 'completed'
            new_task_file = tasks_dir / new_status_dir / f"{task_id}.json"
            new_task_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(new_task_file, 'w', encoding='utf-8') as f:
                json.dump(task, f, ensure_ascii=False, indent=2)
            
            # 古いファイルを削除
            if task_file != new_task_file:
                task_file.unlink()
            
            return True
    
    return False


if __name__ == "__main__":
    # タスクをJSONに変換
    tasks = convert_tasks_to_json()
    print(f"Converted {len(tasks)} tasks to JSON format")

