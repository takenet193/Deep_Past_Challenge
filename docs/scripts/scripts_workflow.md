# スクリプト実行のワークフロー

このドキュメントでは、スクリプトの典型的な使用フローを説明します。

## 典型的な使用フロー

### 1. タスク管理のワークフロー

```bash
# 1. タスク作成・更新
# knowledge/tasks/active/ にMarkdownファイルを追加・編集

# 2. タスク変換（JSON生成）
python scripts/workflow/task_converter.py
# → 重複チェックも自動実行される

# 3. プロジェクトリンク同期（タスクにprojectフィールドがある場合）
python scripts/workflow/sync_project_links.py

# 4. エージェント実行
# Plannerが tasks/current_sprint.json を読み取り、タスクを分解

# 5. タスク完了（推奨: move_task.pyを使用）
python scripts/workflow/move_task.py \
  knowledge/tasks/active/task-xxx.md \
  knowledge/tasks/completed/task-xxx.md

# 6. 再変換（必要に応じて）
python scripts/workflow/task_converter.py
```

### 2. Kaggle提出のワークフロー

```bash
# 1. 認証確認
bash scripts/kaggle/check_kaggle_auth.sh

# 2. 実験実行（Developerエージェントが実行）
# experiments/exp[timestamp]_[description]/exp[timestamp]_train.py

# 3. 提出ファイルの確認
ls -lh results/exp[timestamp]_[description]/exp[timestamp]_submission.csv

# 4. 提出実行
# scripts/kaggle/submit_to_kaggle.sh を編集して実行
bash scripts/kaggle/submit_to_kaggle.sh

# 5. 結果確認
# Kaggleのコンペティションページで結果を確認
```

## 関連ドキュメント

- [スクリプトガイド](../scripts_guide.md) - スクリプトの概要
- [ワークフロー管理スクリプト](./workflow_scripts.md) - ワークフロー管理用スクリプト
- [Kaggle提出スクリプト](./kaggle_scripts.md) - Kaggle提出用スクリプト
- [トラブルシューティング](./scripts_troubleshooting.md) - よくある問題と解決方法

