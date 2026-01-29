# ワークフロー実践例

このドキュメントでは、実際の使用例を通じてワークフローの使い方を説明します。

## 例1: ベースライン実験の実行（実際の例）

**実際の実験**: `exp20260106030720_baseline_tfidf_lr`

1. **知識収集**: EDA結果を `knowledge/zettelkasten/permanent/20260105180000_disaster_tweets_eda.md` に記録

2. **タスク生成**: `knowledge/inbox/` にタスク候補を追加 → `knowledge/tasks/active/task-20260105120020.md` にコピー
   - タスクID: `task-20260105120020`
   - プロジェクト: `kaggle_disaster_tweets`

3. **タスク変換**: 
   ```bash
   python scripts/workflow/task_converter.py
   ```
   - `tasks/current_sprint.json` にタスクが追加される

4. **プロジェクトリンク同期**:
   ```bash
   python scripts/workflow/sync_project_links.py
   ```
   - プロジェクトノートとタスクファイルの相互リンクを更新

5. **エージェント実行**: 
   - Plannerがタスクを読み取り、実装計画を立案
   - Developerが実験コードを作成・実行
   - 実験ID: `exp20260106030720`
   - 実験ディレクトリ: `experiments/exp20260106030720_baseline_tfidf_lr/`
   - 結果ディレクトリ: `results/exp20260106030720_baseline_tfidf_lr/`

6. **結果記録**: 
   - CV F1 Score: 0.7425 ± 0.0137
   - Public LB: 0.80079
   - Validatorが実験レポートを作成: `results/exp20260106030720_baseline_tfidf_lr/exp20260106030720_report.md`
   - タスクを `knowledge/tasks/completed/` に移動

## 例2: 特徴量追加実験の実行（実際の例）

**実際の実験**: `exp20260112174906_keyword_tfidf_lr`

1. **知識収集**: 改善アイディアを `knowledge/zettelkasten/permanent/20260112162435_disaster_tweets_baseline_improvement_ideas.md` に記録

2. **タスク生成**: `knowledge/tasks/active/task-20260112173705.md` を作成
   - タスクID: `task-20260112173705`
   - プロジェクト: `kaggle_disaster_tweets_baseline_improvement`
   - 依存関係: `exp20260106030720_report`

3. **タスク変換**: `python scripts/workflow/task_converter.py`

4. **プロジェクトリンク同期**: `python scripts/workflow/sync_project_links.py`

5. **エージェント実行**: 
   - Developerがkeyword特徴量を追加した実験コードを作成
   - 実験ID: `exp20260112174906`
   - 親実験: `exp20260106030720`

6. **結果記録**: 
   - CV F1 Score: 0.7501 ± 0.0123
   - Public LB: 0.80123
   - ベースラインから0.00044改善
   - Validatorが実験レポートを作成

## 関連ドキュメント

- [ワークフローガイド](../workflow_guide.md) - ワークフローの概要
- [ワークフローの詳細ステップ](./workflow_steps.md) - 各ステップの詳細
- [エージェント実行フロー](./workflow_agent_flow.md) - エージェント間の連携詳細
- [トラブルシューティング](./workflow_troubleshooting.md) - よくある問題と解決方法

