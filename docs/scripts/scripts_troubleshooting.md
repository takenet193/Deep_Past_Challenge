# スクリプトトラブルシューティング

このドキュメントでは、スクリプト実行時に発生する可能性のある問題とその解決方法を説明します。

## `task_converter.py` でエラーが出る場合

**問題**: YAML frontmatterのパースエラー

**原因と解決方法**:
- **YAML frontmatterの形式を確認**: `---` で囲まれているか、閉じタグがあるか
- **ファイルエンコーディング**: UTF-8で保存されているか確認
- **パス**: スクリプトはリポジトリルートから実行してください

**確認方法**:
```bash
# エラーメッセージを確認
python scripts/workflow/task_converter.py

# 問題のあるファイルを特定
# エラーメッセージにファイル名が表示されます
```

**問題**: 重複警告が表示される

**原因と解決方法**:
- 同じタスクIDが複数のディレクトリに存在する
- 不要なファイルを削除してください
- 通常、完了したタスクは `completed/` にのみ存在すべきです

**対処法**:
```bash
# 重複ファイルを確認
python scripts/workflow/task_converter.py
# → 警告メッセージで重複ファイルの場所が表示される

# 不要なファイルを削除（通常は active/ の方を削除）
rm knowledge/tasks/active/task-xxx.md
```

## `task_loader.py` でタスクが見つからない場合

**問題**: `load_task()` や `load_active_tasks()` が空のリストを返す

**原因と解決方法**:
- **`current_sprint.json` が存在するか確認**: 先に `task_converter.py` を実行してください
- **タスクIDの確認**: 大文字小文字・ハイフン/アンダースコアの違いに注意
- **ステータスの確認**: `load_active_tasks()` は `status: "in_progress"` のタスクを返します

**確認方法**:
```python
# task_loader.pyを使用して確認
from scripts.workflow.task_loader import load_tasks_index

index = load_tasks_index()
print(f"Total tasks: {len(index.get('tasks', []))}")
```

## `sync_project_links.py` でリンクが更新されない場合

**問題**: 実行してもリンクが更新されない

**原因と解決方法**:
- **マーカーの確認**: `<!-- AUTO:project:start -->` と `<!-- AUTO:project:end -->` が正しく記述されているか確認
- **projectフィールドの確認**: タスクのYAML frontmatterに `project: <project_name>` が設定されているか確認
- **プロジェクトノートの存在確認**: `knowledge/tasks/projects/project_<project_name>.md` が存在するか確認

**確認方法**:
```bash
# ドライランで変更内容を確認
python scripts/workflow/sync_project_links.py --dry-run
```

## `move_task.py` で移動に失敗する場合

**問題**: 移動元のファイルが削除されない

**原因と解決方法**:
- **ファイル権限の確認**: ファイルの書き込み権限があるか確認
- **ファイルが開かれていないか確認**: 他のプロセスがファイルを使用していないか確認
- **手動削除**: 警告メッセージに従って、手動で削除してください

**確認方法**:
```bash
# 移動先のファイルが作成されているか確認
ls -lh knowledge/tasks/completed/task-xxx.md

# 移動元のファイルが残っているか確認
ls -lh knowledge/tasks/active/task-xxx.md
```

## Kaggle提出スクリプトでエラーが出る場合

**問題**: `check_kaggle_auth.sh` で認証に失敗する

**原因と解決方法**:
- **`kaggle.json` の存在確認**: `~/.kaggle/kaggle.json` が存在するか確認
- **ファイル権限の確認**: `chmod 600 ~/.kaggle/kaggle.json` を実行
- **APIトークンの確認**: KaggleのAccountページで新しいトークンを生成

**問題**: `submit_to_kaggle.sh` で提出に失敗する

**原因と解決方法**:
- **提出ファイルの存在確認**: `SUBMISSION_FILE` のパスが正しいか確認
- **コンペティション名の確認**: `COMPETITION` が正しいか確認
- **提出ファイルの形式確認**: CSVファイルが正しい形式か確認

## 関連ドキュメント

- [スクリプトガイド](../scripts_guide.md) - スクリプトの概要
- [ワークフロー管理スクリプト](./workflow_scripts.md) - ワークフロー管理用スクリプト
- [Kaggle提出スクリプト](./kaggle_scripts.md) - Kaggle提出用スクリプト
- [スクリプト実行のワークフロー](./scripts_workflow.md) - 典型的な使用フロー

