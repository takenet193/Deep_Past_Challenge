# ワークフローの詳細ステップ

このドキュメントでは、知識管理から実験実行までの各ステップの詳細を説明します。

## ステップ1: 知識収集（Obsidian）

### Zettelkastenノートの作成

1. `knowledge/zettelkasten/permanent/` ディレクトリに新しいノートを作成
2. タイムスタンプベースのIDで命名（形式: `YYYYMMDDHHMMSS_[description].md`）
   - 例: `20260105180000_disaster_tweets_eda.md`
3. ノートに知識を記録し、関連ノートへのリンクを追加

### ノートの例（実際の実装に基づく）

```markdown
---
id: 20260105180000
title: Disaster Tweets - EDA結果
author: takeikumi
type: permanent
form: report
tags: [kaggle, eda, kaggle_disaster_tweets, nlp, report]
links:
  - project_kaggle_disaster_tweets
created: 2026-01-05
updated: 2026-01-05
---

# Disaster Tweets - EDA結果

## 内容
Disaster Tweetsコンペの探索的データ分析（EDA）結果。

## 基本統計
- train: 7613行、5列
- test: 3263行、4列

## 関連ノート
- [[project_kaggle_disaster_tweets]] プロジェクトノート
```

### ノートの配置場所

- `knowledge/zettelkasten/permanent/`: 永続的な知識ノート
- `knowledge/zettelkasten/references/`: 外部資料の要約やリンク
- `knowledge/zettelkasten/structure/`: システム構造や設計に関するノート
- `knowledge/zettelkasten/index/`: 知識ノートのインデックス

## ステップ2: タスク生成（GTD）

### タスクの作成手順

1. 知識ノートから実装可能なタスクを特定
2. `knowledge/inbox/` にタスク/アイデア/メモを追加（共通Inbox）
3. タスクとして採用する場合は `knowledge/tasks/{active|waiting|someday}/` に **コピーしてSSOT化**
4. 元のInboxファイルは `knowledge/inbox/archive/` に移動（入力ログとして保持）
5. 必要に応じてメタデータに `related_notes` を記録

> **運用ルールの詳細**: レビュー・モード、SSOT、コピー→アーカイブ等の詳細は `.cursor/docs_manager_rules.mdc` を参照してください。

### タスクの例（実際の実装に基づく）

```markdown
---
type: task
id: task-20260112173705
title: "Disaster Tweets: keyword特徴量の追加実験"
author: takeikumi
status: active
priority: high
project: kaggle_disaster_tweets_baseline_improvement
mode: experiment
context:
  - project_kaggle_disaster_tweets_baseline_improvement
  - project_kaggle_disaster_tweets
dependencies:
  - exp20260106030720_report
related_notes:
  - disaster_tweets_baseline_improvement_ideas_20260112162435
  - exp20260106030720_report
  - disaster_tweets_eda_20260105180000
created: 2026-01-12
updated: 2026-01-12
tags: [kaggle, kaggle_disaster_tweets, improvement, feature-engineering, keyword, experiment]
---

# タスク: Disaster Tweets - keyword特徴量の追加実験

## 目的
ベースライン実験（exp20260106030720）を起点に、keyword特徴量を追加して性能を向上させる。

## 手順
1. keywordカラムをターゲットエンコーディングで特徴量化
2. TF-IDF特徴量と結合
3. LogisticRegressionで評価
4. 結果を記録
```

### タスクの配置場所

- `knowledge/tasks/active/`: アクティブなタスク（次にやるべきこと）
- `knowledge/tasks/waiting/`: 待機中タスク（他のタスクの完了を待つ）
- `knowledge/tasks/someday/`: いつかやる/たぶんやるタスク
- `knowledge/tasks/completed/`: 完了したタスク

## ステップ3: タスク変換（JSON）

### MarkdownからJSONへの変換

```bash
python scripts/workflow/task_converter.py
```

このスクリプトは：
- `knowledge/tasks/` 内のMarkdownファイルを読み込み
- JSON形式に変換
- `tasks/current_sprint.json` に保存（上書き）

**重要**: `tasks/current_sprint.json` は自動生成されるため、**手で編集しないでください**。

### 変換後のJSON構造

JSON構造の詳細については、[タスク管理システムのドキュメント](../components/task_management.md#タスクjson-スキーマ)を参照してください。

## ステップ4: プロジェクトリンク同期（タスク確定時）

### プロジェクトとタスクの相互リンクを同期

```bash
python scripts/workflow/sync_project_links.py
```

このスクリプトは：
- タスクに `project` フィールドが設定されている場合に実行
- プロジェクトノートとタスクファイルの相互リンクを自動更新
- タスクノートに `<!-- AUTO:project:start -->` と `<!-- AUTO:project:end -->` の間にプロジェクトリンクを追加
- プロジェクトノートに `<!-- AUTO:tasks:start -->` と `<!-- AUTO:tasks:end -->` の間にタスク一覧を追加

### 実行タイミング

以下のいずれかの場合に実行：
- ✅ タスクを確定（コピー）した後（`project`フィールドが設定されている場合）
- ✅ タスクの`project`フィールドを変更した後
- ✅ プロジェクトノートを作成・更新した後

### ドライラン（変更内容の確認のみ）

```bash
python scripts/workflow/sync_project_links.py --dry-run
```

ファイルを更新せずに、変更内容を確認できます。

## ステップ5: エージェント実行

### エージェント実行フロー（実際の実装に基づく）

```
User → Document Manager → Planner → User → Developer → Validator → User → Validator → Document Manager → Version Controller
```

### 詳細なフロー

1. **Document Manager**: アイディア受領・情報収集
   - ユーザーのアイディアを整理・要約
   - 関連情報の収集・整理
   - 前回のexperiment結果の確認（該当する場合）

2. **Planner**: 計画立案
   - `scripts/workflow/task_loader.py` を使用して未処理タスクを読み込む
   - タスクを具体的な実装ステップに分解
   - 各ステップを適切なエージェントに割り当て
   - ユーザーに計画を提示して承認を得る

3. **Developer**: 実装・実行
   - 実験コードと結果ファイルの作成
   - `experiments/exp[timestamp]_[description]/` に実験コードを保存
   - `results/exp[timestamp]_[description]/` に結果ファイルを保存
   - 提出ファイル（submission.csv）の作成まで完了

4. **Validator**: 評価と実験レポート作成
   - Developerから引き継ぎを受ける
   - **ユーザーに結果入力を依頼**: Kaggle提出後の結果（Public LBスコア等）をユーザーに入力依頼
   - **ユーザーから結果を受け取る**
   - 関連タスク・プロジェクトの検索と提案
   - 実験レポート（`results/exp[timestamp]_[description]/exp[timestamp]_report.md`）を作成

5. **Docs Manager**: 文書化
   - 実験結果の要約
   - 知識ノートへの反映

6. **Version Controller**: Git管理
   - 変更の記録
   - 適切なコミットメッセージの生成（Conventional Commits準拠）
   - Gitコミットの実行

### Plannerエージェントの動作

1. **タスク読み取り**: `scripts/workflow/task_loader.py` を使用して未処理タスクを読み込む
   
   Plannerエージェントは、`tasks/current_sprint.json` からタスクを読み取り、計画立案に必要な情報を取得します。
   
   ```python
   from scripts.workflow.task_loader import load_pending_tasks, format_task_for_planner
   
   # 未処理タスク（status="pending"）を読み込む
   pending_tasks = load_pending_tasks()
   
   # 各タスクをPlannerが読みやすい形式にフォーマットして表示
   for task in pending_tasks:
       formatted = format_task_for_planner(task)
       print(formatted)
   ```
   
   **説明**:
   - `load_pending_tasks()`: `tasks/current_sprint.json` から未処理タスク（`status="pending"`）を読み込む
   - `format_task_for_planner(task)`: タスク情報をPlannerが読みやすい形式（タイトル、ID、優先度、プロジェクト、依存関係など）にフォーマット
   - Plannerはこのフォーマットされた情報を基に、実装計画を立案します

2. **計画立案**: タスクを具体的な実装ステップに分解
   - 実装の目的と仮説を明確化
   - 具体的な実装手順を立案
   - 期待される成果を定量化
   - リスク要因と対策を特定

3. **エージェント割り当て**: 各ステップを適切なエージェントに割り当て
   - Developer: 実験コードと結果ファイルの作成
   - Validator: 評価と実験レポート作成
   - Docs Manager: 文書化
   - Version Controller: Git管理

各エージェントの詳細は `.cursor/kaggle_team.mdc` と `.cursor/experiment_flow_instructions.mdc` を参照してください。

## ステップ6: 結果記録

### 実験結果の記録方法

1. **実験コード**: `experiments/exp[YYYYMMDDHHMMSS]_[description]/`
   - `exp[timestamp]_config.yaml`: 実験設定ファイル
   - `exp[timestamp]_train.py`: 学習スクリプト
   - `exp[timestamp]_predict.py`: 推論スクリプト

2. **実験結果**: `results/exp[YYYYMMDDHHMMSS]_[description]/`
   - `exp[timestamp]_metrics.json`: 評価指標（CV Mean, CV Std, Train, Public LB）
   - `exp[timestamp]_cv_results.json`: CV結果（各フォールドの詳細）
   - `exp[timestamp]_submission.csv`: 提出ファイル
   - `exp[timestamp]_model.pkl`: モデルファイル（Git管理対象外）
   - `exp[timestamp]_report.md`: 実験レポート（Validatorエージェントが作成）

3. **知識ノートへの反映**: 実験レポートの `links` フィールドに知識ノートへのリンクを追加
   - 関連する知識ノートのIDを `links` に追加
   - プロジェクトノートへのリンクを追加

4. **タスクの完了**: タスクを `knowledge/tasks/completed/` に移動

### 実験レポートの例（実際の実装に基づく）

```markdown
---
id: 20260106030720
title: Disaster Tweets - baseline_tfidf_lr_text_only
author: takeikumi
type: experiment_report
experiment_id: exp20260106030720
project: kaggle_disaster_tweets
form: report
description: ベースライン: textのみ + TF-IDF(1-2gram) + LogisticRegression
parent_experiment: null
related_task: task-20260105120020
tags: [kaggle, kaggle_disaster_tweets, baseline, tfidf, logistic-regression, nlp, experiment, report]
status: completed
metrics:
  train_f1: 0.8542
  cv_mean: 0.7425
  cv_std: 0.0137
  public_lb: 0.80079
model:
  type: LogisticRegression
  features: tfidf
links:
  - project_kaggle_disaster_tweets
  - task-20260105120020
  - disaster_tweets_eda_20260105180000
created: 2026-01-06
updated: 2026-01-06
---

# Disaster Tweets - baseline_tfidf_lr_text_only

## 実験概要
- 実験ID: exp20260106030720
- CV F1 Score: 0.7425 ± 0.0137
- Public LB: 0.80079

## 実装内容
- textのみ + TF-IDF(1-2gram) + LogisticRegression

## 学んだこと
- シンプルなベースラインで良好な性能を達成
- 次のステップ: keyword特徴量追加とC値チューニング
```

## ステップ7: フィードバックループ

### 知識の更新

1. **新しい知識ノート**: 実験から得られた学びを新しいノートとして記録
   - `knowledge/zettelkasten/permanent/` に新しいノートを作成
   - 実験レポートへのリンクを追加

2. **既存ノートの更新**: 関連する既存ノートにリンクを追加
   - 実験レポートの `links` フィールドに既存ノートのIDを追加
   - 既存ノートの `links` フィールドに実験レポートのIDを追加

3. **新しいタスク**: 学びから新しい実装アイディアをタスクとして生成
   - 実験レポートの「次のステップ」から新しいタスクを作成
   - `knowledge/inbox/` に追加 → `knowledge/tasks/active/` にコピー

### 循環の完成

```
知識 → タスク → 実験 → 学び → 知識 → ...
```

この循環により、知識とタスクが有機的に成長していきます。

## 関連ドキュメント

- [ワークフローガイド](../workflow_guide.md) - ワークフローの概要
- [エージェント実行フロー](./workflow_agent_flow.md) - エージェント間の連携詳細
- [実践例](./workflow_examples.md) - 実際の使用例
- [トラブルシューティング](./workflow_troubleshooting.md) - よくある問題と解決方法
- [ベストプラクティス](./workflow_best_practices.md) - 推奨される運用方法

