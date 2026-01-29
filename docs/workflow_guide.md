# ワークフローガイド

このドキュメントでは、知識管理から実験実行までの全体的なワークフローを説明します。

## 概要

### ワークフローの全体像

```
知識収集 → タスク生成 → タスク変換 → プロジェクトリンク同期 → エージェント実行 → 結果記録 → フィードバック
```

### 実装状況（2026年1月時点）

| ステップ | 実装状況 | 説明 |
|:---|:---|:---|
| 1. 知識収集 | ✅ 実装済み | Obsidian、Zettelkasten |
| 2. タスク生成 | ✅ 実装済み | GTD、Inbox → Tasks |
| 3. タスク変換 | ✅ 実装済み | task_converter.py |
| 4. プロジェクトリンク同期 | ✅ 実装済み | sync_project_links.py |
| 5. エージェント実行 | ✅ 実装済み | マルチエージェントシステム |
| 6. 結果記録 | ✅ 実装済み | 実験レポート、知識ノート |
| 7. フィードバックループ | ✅ 実装済み | 学びから新しい知識へ |

## クイックスタート

### 基本的なワークフロー（簡潔版）

1. **知識ノートを作成**: `knowledge/zettelkasten/permanent/` に新しいノートを作成
2. **タスクを生成**: `knowledge/inbox/` に追加 → `knowledge/tasks/active/` にコピー
3. **タスクを変換**: `python scripts/workflow/task_converter.py`
4. **リンクを同期**: `python scripts/workflow/sync_project_links.py`（タスクに `project` フィールドがある場合）
5. **エージェント実行**: Plannerがタスクを読み取り、各エージェントに割り当て
6. **結果を記録**: 実験結果を `results/` に保存し、知識ノートを更新

詳細は以下の各ドキュメントを参照してください。

## 詳細ドキュメント

### ワークフローの詳細ステップ

- [ワークフローの詳細ステップ](./workflow/workflow_steps.md) - 各ステップの詳細な説明

### エージェント実行フロー

- [エージェント実行フロー（詳細）](./workflow/workflow_agent_flow.md) - エージェント間の連携と各ステップの詳細

### 実践例

- [実践例](./workflow/workflow_examples.md) - 実際の使用例（ベースライン実験、特徴量追加実験など）

### トラブルシューティング

- [トラブルシューティング](./workflow/workflow_troubleshooting.md) - よくある問題と解決方法

### ベストプラクティス

- [ベストプラクティス](./workflow/workflow_best_practices.md) - 推奨される運用方法

## 関連ドキュメント

- **プロジェクト全体アーキテクチャ**: `docs/project_architecture.md`
- **スクリプトガイド**: `docs/scripts_guide.md`
- **エージェント定義（チーム憲法）**: `.cursor/kaggle_team.mdc`
- **実験フロー指示**: `.cursor/experiment_flow_instructions.mdc`
- **Developer ルール**: `.cursor/developer_experiment_rules.mdc`
- **Docs Manager ルール**: `.cursor/docs_manager_rules.mdc`
- **Version Controller ルール**: `.cursor/version_controller_rules.mdc`
