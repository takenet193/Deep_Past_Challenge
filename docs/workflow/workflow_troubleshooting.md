# ワークフロートラブルシューティング

このドキュメントでは、ワークフロー実行時に発生する可能性のある問題とその解決方法を説明します。

## タスク変換でエラーが出る場合

**問題**: `python scripts/workflow/task_converter.py` でエラーが発生する

**原因と解決方法**:
- **YAML frontmatterの形式エラー**: `---` で囲まれているか、閉じタグがあるか確認
- **ファイルエンコーディング**: UTF-8で保存されているか確認
- **パス**: スクリプトはリポジトリルートから実行してください

**確認方法**:
```bash
# エラーメッセージを確認
python scripts/workflow/task_converter.py

# 問題のあるファイルを特定
# エラーメッセージにファイル名が表示されます
```

## プロジェクトリンク同期でリンクが更新されない場合

**問題**: `python scripts/workflow/sync_project_links.py` を実行してもリンクが更新されない

**原因と解決方法**:
- **マーカーの確認**: `<!-- AUTO:project:start -->` と `<!-- AUTO:project:end -->` が正しく記述されているか確認
- **projectフィールドの確認**: タスクのYAML frontmatterに `project: <project_name>` が設定されているか確認
- **プロジェクトノートの存在確認**: `knowledge/tasks/projects/project_<project_name>.md` が存在するか確認

**確認方法**:
```bash
# ドライランで変更内容を確認
python scripts/workflow/sync_project_links.py --dry-run
```

## エージェントがタスクを見つけられない場合

**問題**: Plannerが `tasks/current_sprint.json` からタスクを読み取れない

**原因と解決方法**:
- **JSONファイルの存在確認**: `tasks/current_sprint.json` が存在するか確認
- **タスク変換の実行**: `python scripts/workflow/task_converter.py` を実行してJSONを生成
- **タスクIDの確認**: 大文字小文字・ハイフン/アンダースコアの違いに注意

**確認方法**:
```python
# task_loader.pyを使用して確認
from scripts.workflow.task_loader import load_tasks_index

index = load_tasks_index()
print(f"Total tasks: {len(index.get('tasks', []))}")
```

## 実験レポートが作成されない場合

**問題**: Validatorが実験レポートを作成しない

**原因と解決方法**:
- **結果ファイルの確認**: `results/exp[timestamp]_[description]/exp[timestamp]_metrics.json` が存在するか確認
- **ユーザー入力の確認**: Validatorはユーザーから結果（Public LBスコア等）を受け取る必要がある
- **引き継ぎの確認**: Developerから引き継ぎを受けているか確認

## プロジェクトノートにタスクが表示されない場合

**問題**: プロジェクトノートの「タスク一覧（AUTO）」セクションにタスクが表示されない

**原因と解決方法**:
- **プロジェクトリンク同期の実行**: `python scripts/workflow/sync_project_links.py` を実行
- **projectフィールドの確認**: タスクのYAML frontmatterに `project: <project_name>` が設定されているか確認
- **マーカーの確認**: `<!-- AUTO:tasks:start -->` と `<!-- AUTO:tasks:end -->` が正しく記述されているか確認

## 関連ドキュメント

- [ワークフローガイド](../workflow_guide.md) - ワークフローの概要
- [ワークフローの詳細ステップ](./workflow_steps.md) - 各ステップの詳細
- [エージェント実行フロー](./workflow_agent_flow.md) - エージェント間の連携詳細
- [実践例](./workflow_examples.md) - 実際の使用例
- [ベストプラクティス](./workflow_best_practices.md) - 推奨される運用方法

