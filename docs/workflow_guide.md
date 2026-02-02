# ワークフローガイド

このドキュメントでは、知識管理から実験実行までの全体的なワークフローを説明します。

## ワークフロー概要

1. **知識ノートを作成**: `knowledge/zettelkasten/permanent/` に新しいノートを作成
2. **タスクを生成**: `knowledge/inbox/` に追加 → `knowledge/tasks/active/` にコピー
3. **タスクを変換**: `python scripts/workflow/task_converter.py`
4. **リンクを同期**: `python scripts/workflow/sync_project_links.py`（タスクに `project` フィールドがある場合）
5. **エージェント実行**: Plannerがタスクを読み取り、各エージェントに割り当て
6. **結果を記録**: 実験結果を `results/` に保存し、知識ノートを更新

## 詳細ドキュメント

- [ワークフローの詳細ステップ](./workflow/workflow_steps.md) - 各ステップの詳細な説明
- [エージェント実行フロー（詳細）](./workflow/workflow_agent_flow.md) - エージェント間の連携と各ステップの詳細
- [実践例](./workflow/workflow_examples.md) - 実際の使用例（ベースライン実験、特徴量追加実験など）
- [トラブルシューティング](./workflow/workflow_troubleshooting.md) - よくある問題と解決方法
- [ベストプラクティス](./workflow/workflow_best_practices.md) - 推奨される運用方法

## 関連ドキュメント

- **プロジェクト全体アーキテクチャ**: `docs/project_architecture.md`
- **スクリプトガイド**: `docs/scripts_guide.md`
- **エージェント定義（チーム憲法）**: `.cursor/kaggle_team.mdc`
- **実験フロー指示**: `.cursor/experiment_flow_instructions.mdc`
- **Developer ルール**: `.cursor/developer_experiment_rules.mdc`
- **Docs Manager ルール**: `.cursor/docs_manager_rules.mdc`
- **Version Controller ルール**: `.cursor/version_controller_rules.mdc`
