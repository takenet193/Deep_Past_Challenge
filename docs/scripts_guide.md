# スクリプトガイド

このドキュメントでは、プロジェクト内の各スクリプトの目的、使い方、入出力を説明します。

## 概要

### ディレクトリ構造

```
scripts/
├── workflow/          # タスク管理、プロジェクトリンク同期など
│   ├── task_converter.py
│   ├── task_loader.py
│   ├── sync_project_links.py
│   └── move_task.py
└── kaggle/            # Kaggle提出用
    ├── check_kaggle_auth.sh
    ├── submit_to_kaggle.sh
    └── submit_with_token.sh
```

## 詳細ドキュメント

- [ワークフロー管理スクリプト](./scripts/workflow_scripts.md) - タスク変換、タスク読み込み、プロジェクトリンク同期、タスク移動
- [Kaggle提出スクリプト](./scripts/kaggle_scripts.md) - Kaggle API認証確認、提出処理
- [スクリプト実行のワークフロー](./scripts/scripts_workflow.md) - 典型的な使用フロー
- [トラブルシューティング](./scripts/scripts_troubleshooting.md) - よくある問題と解決方法

## 関連ドキュメント

- **ワークフローガイド**: `docs/workflow_guide.md`
- **システム概要・アーキテクチャ**: `docs/system_overview.md`
- **タスク管理（GTD）**: `knowledge/tasks/_gtd_guide.md`（存在する場合）
- **Docs Managerルール**: `.cursor/docs_manager_rules.mdc`
- **Developer 実験運用ルール**: `.cursor/developer_experiment_rules.mdc`
