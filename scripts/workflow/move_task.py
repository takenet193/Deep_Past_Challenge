"""
タスクファイルを安全に移動するユーティリティ

mv コマンドで移動した際に元のファイルが残ってしまう問題を防ぐため、
移動後に確実に元のファイルを削除します。
"""

import sys
from pathlib import Path
import shutil


def safe_move_task(source: Path, destination: Path) -> bool:
    """
    タスクファイルを安全に移動する
    
    Args:
        source: 移動元のファイルパス
        destination: 移動先のファイルパス
        
    Returns:
        移動が成功した場合はTrue、失敗した場合はFalse
    """
    if not source.exists():
        print(f"エラー: 移動元のファイルが存在しません: {source}")
        return False
    
    # 移動先のディレクトリが存在しない場合は作成
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    # ファイルをコピー
    try:
        shutil.copy2(source, destination)
    except Exception as e:
        print(f"エラー: ファイルのコピーに失敗しました: {e}")
        return False
    
    # コピーが成功したことを確認
    if not destination.exists():
        print(f"エラー: 移動先にファイルが存在しません: {destination}")
        return False
    
    # 元のファイルを削除
    try:
        source.unlink()
    except Exception as e:
        print(f"警告: 元のファイルの削除に失敗しました: {e}")
        print(f"移動先: {destination}")
        print(f"元のファイルを手動で削除してください: {source}")
        return False
    
    # 元のファイルが残っていないことを確認
    if source.exists():
        print(f"警告: 元のファイルがまだ存在します: {source}")
        print(f"手動で削除してください")
        return False
    
    print(f"✓ タスクを移動しました: {source.name}")
    print(f"  移動元: {source}")
    print(f"  移動先: {destination}")
    return True


def main():
    """コマンドライン引数から移動元と移動先を取得して移動"""
    if len(sys.argv) != 3:
        print("使用方法: python scripts/workflow/move_task.py <移動元> <移動先>")
        print("例: python scripts/workflow/move_task.py knowledge/tasks/active/task-xxx.md knowledge/tasks/completed/task-xxx.md")
        sys.exit(1)
    
    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    
    if safe_move_task(source, destination):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()





