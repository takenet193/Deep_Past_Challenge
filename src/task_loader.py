"""
マルチエージェントシステムがタスクJSONを読み取るためのユーティリティ

Plannerエージェントがタスクを読み取り、分解して各エージェントに
割り当てる際に使用します。
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


def load_task(task_id: str, tasks_dir: Path = Path("tasks")) -> Optional[Dict]:
    """
    特定のタスクを読み込む
    
    Args:
        task_id: タスクID
        tasks_dir: タスクJSONファイルのディレクトリ
        
    Returns:
        タスク情報の辞書、見つからない場合はNone
    """
    # 各ステータスディレクトリを検索
    for status_dir in ['pending', 'in_progress', 'completed']:
        task_file = tasks_dir / status_dir / f"{task_id}.json"
        if task_file.exists():
            with open(task_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    return None


def load_pending_tasks(tasks_dir: Path = Path("tasks")) -> List[Dict]:
    """
    未処理のタスクをすべて読み込む
    
    Args:
        tasks_dir: タスクJSONファイルのディレクトリ
        
    Returns:
        未処理タスクのリスト
    """
    pending_dir = tasks_dir / "pending"
    if not pending_dir.exists():
        return []
    
    tasks = []
    for task_file in pending_dir.glob("*.json"):
        with open(task_file, 'r', encoding='utf-8') as f:
            tasks.append(json.load(f))
    
    # 優先順位と期限でソート
    tasks.sort(key=lambda x: (
        {'high': 0, 'medium': 1, 'low': 2}.get(x.get('priority', 'medium'), 1),
        x.get('due_date', '9999-12-31')
    ))
    
    return tasks


def load_active_tasks(tasks_dir: Path = Path("tasks")) -> List[Dict]:
    """
    進行中のタスクをすべて読み込む
    
    Args:
        tasks_dir: タスクJSONファイルのディレクトリ
        
    Returns:
        進行中タスクのリスト
    """
    in_progress_dir = tasks_dir / "in_progress"
    if not in_progress_dir.exists():
        return []
    
    tasks = []
    for task_file in in_progress_dir.glob("*.json"):
        with open(task_file, 'r', encoding='utf-8') as f:
            tasks.append(json.load(f))
    
    return tasks


def load_tasks_by_project(project: str, tasks_dir: Path = Path("tasks")) -> List[Dict]:
    """
    特定のプロジェクトのタスクを読み込む
    
    Args:
        project: プロジェクト名
        tasks_dir: タスクJSONファイルのディレクトリ
        
    Returns:
        プロジェクトのタスクリスト
    """
    all_tasks = []
    
    for status_dir in ['pending', 'in_progress', 'completed']:
        status_path = tasks_dir / status_dir
        if not status_path.exists():
            continue
            
        for task_file in status_path.glob("*.json"):
            with open(task_file, 'r', encoding='utf-8') as f:
                task = json.load(f)
                if task.get('project') == project:
                    all_tasks.append(task)
    
    return all_tasks


def load_tasks_index(tasks_dir: Path = Path("tasks")) -> Optional[Dict]:
    """
    タスクインデックスファイルを読み込む
    
    Args:
        tasks_dir: タスクJSONファイルのディレクトリ
        
    Returns:
        インデックス情報の辞書
    """
    index_file = tasks_dir / "tasks_index.json"
    if not index_file.exists():
        return None
    
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_task_for_planner(task: Dict) -> str:
    """
    タスクをPlannerエージェントが読みやすい形式にフォーマット
    
    Args:
        task: タスク情報の辞書
        
    Returns:
        フォーマットされた文字列
    """
    lines = [
        f"# タスク: {task['title']}",
        f"ID: {task['id']}",
        f"ステータス: {task['status']}",
        f"優先度: {task['priority']}",
        f"プロジェクト: {task['project']}",
        "",
        f"## 説明",
        task.get('description', '')[:500],
        "",
        f"## 期待される成果",
    ]
    
    if task.get('expected_outcome'):
        outcome = task['expected_outcome']
        if isinstance(outcome, dict):
            lines.append(f"- タイプ: {outcome.get('type', 'N/A')}")
            if 'metrics' in outcome:
                lines.append(f"- 評価指標: {', '.join(outcome['metrics'])}")
            if 'target_improvement' in outcome:
                lines.append(f"- 目標改善: {outcome['target_improvement']}")
        else:
            lines.append(str(outcome))
    
    if task.get('related_notes'):
        lines.extend([
            "",
            f"## 関連ノート",
            ", ".join(task['related_notes'])
        ])
    
    if task.get('dependencies'):
        lines.extend([
            "",
            f"## 依存タスク",
            ", ".join(task['dependencies'])
        ])
    
    return "\n".join(lines)


if __name__ == "__main__":
    # 使用例
    pending_tasks = load_pending_tasks()
    print(f"未処理タスク数: {len(pending_tasks)}")
    
    for task in pending_tasks[:3]:  # 最初の3つを表示
        print("\n" + "="*50)
        print(format_task_for_planner(task))

