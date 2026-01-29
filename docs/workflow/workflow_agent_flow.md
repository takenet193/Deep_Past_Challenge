# エージェント実行フロー（詳細）

このドキュメントでは、マルチエージェントシステムにおけるエージェント間の連携と各ステップの詳細を説明します。

## エージェント間の連携

各エージェントは以下の順序で連携します：

```
User → Document Manager → Planner → User → Developer → Validator → User → Validator → Document Manager → Version Controller
```

## 各ステップの詳細

### Step 1: アイディア受領・情報収集
**担当**: Document Manager

- **入力**: ユーザーのアイディア・フィードバック、関連ドキュメント・リソース
- **処理**: アイディアの整理・要約、関連情報の収集・整理、前回のexperiment結果の確認
- **出力**: 整理されたアイディア、関連情報の要約、コンテキスト情報

### Step 2: 計画立案
**担当**: Planner

- **入力**: Document Managerからの整理されたアイディア
- **処理**: 実装の目的と仮説を明確化、具体的な実装手順を立案、期待される成果を定量化、リスク要因と対策を特定
- **出力**: 実行計画（`[Plan:]` と `[Action:]`）

### Step 3: 計画承認
**担当**: ユーザー

- **処理**: Plannerの計画をレビュー、承認または差し戻しの判断

### Step 4: 実装・実行
**担当**: Developer

- **入力**: 承認された計画
- **処理**: 
  - `experiments/exp[timestamp]_[description]/` ディレクトリの作成
  - コードの実装・実行（train.py, predict.py）
  - 結果ファイルの生成
  - **提出ファイル（submission.csv）の作成まで完了**
- **出力**: Pythonコードブロック、`[Result:]` 実行結果要約
- **引き継ぎ**: Developer → Validator（提出ファイル作成完了後）

### Step 5: 結果入力依頼・レポート作成
**担当**: Validator

- **入力**: Developerが作成した実験コードと結果ファイル、**ユーザーから提供される提出後の結果**（Public LBスコア等）
- **処理**:
  1. Developerからの引き継ぎを受ける
  2. **ユーザーに結果入力を依頼する**: Kaggle提出後の結果（Public LBスコア等）をユーザーに入力依頼
  3. **ユーザーから結果を受け取る**
  4. **関連タスク・プロジェクトの検索と提案**:
     - `experiments/exp[timestamp]_[description]/exp[timestamp]_config.yaml`からプロジェクト名を取得
     - `knowledge/tasks/projects/project_[project_name].md`を検索
     - `knowledge/tasks/active/`, `knowledge/tasks/completed/`から関連タスクを検索
     - `knowledge/zettelkasten/`から関連知識ノートを検索
     - 見つかった関連タスク・プロジェクト・ノートがあれば、ユーザーに提案して確認する
  5. モデル性能の客観的評価（CV結果、Public LBスコア等を含む）
  6. 結果の解釈と分析
  7. 実験レポートの作成（関連タスク・プロジェクト・ノートを含む）
- **出力**: 実験レポート（`results/exp[timestamp]_[description]/exp[timestamp]_report.md`）

### Step 6: ドキュメント化
**担当**: Document Manager

- **入力**: 実験結果、評価結果
- **処理**: 実験概要の文書化、結果の要約、学んだことの記録
- **出力**: Markdownレポート、実験概要、結果サマリー

### Step 7: バージョン管理
**担当**: Version Controller

- **入力**: 全ファイル（コード、結果、ドキュメント）
- **処理**: 変更の記録、適切なコミットメッセージの生成、Gitコミットの実行
- **出力**: Gitコマンド、コミットメッセージ

詳細は `.cursor/experiment_flow_instructions.mdc` を参照してください。

## 関連ドキュメント

- [ワークフローガイド](../workflow_guide.md) - ワークフローの概要
- [ワークフローの詳細ステップ](./workflow_steps.md) - 各ステップの詳細
- [実践例](./workflow_examples.md) - 実際の使用例
- [マルチエージェントシステム](../components/multi_agent_system.md) - エージェントの詳細仕様

