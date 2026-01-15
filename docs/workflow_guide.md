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

---

## クイックスタート

### 基本的なワークフロー（簡潔版）

1. **知識ノートを作成**: `knowledge/zettelkasten/permanent/` に新しいノートを作成
2. **タスクを生成**: `knowledge/inbox/` に追加 → `knowledge/tasks/active/` にコピー
3. **タスクを変換**: `python scripts/workflow/task_converter.py`
4. **リンクを同期**: `python scripts/workflow/sync_project_links.py`（タスクに `project` フィールドがある場合）
5. **エージェント実行**: Plannerがタスクを読み取り、各エージェントに割り当て
6. **結果を記録**: 実験結果を `results/` に保存し、知識ノートを更新

詳細は以下の各セクションを参照してください。

---

## 詳細なワークフロー

### ステップ1: 知識収集（Obsidian）

#### Zettelkastenノートの作成

1. `knowledge/zettelkasten/permanent/` ディレクトリに新しいノートを作成
2. タイムスタンプベースのIDで命名（形式: `YYYYMMDDHHMMSS_[description].md`）
   - 例: `20260105180000_disaster_tweets_eda.md`
3. ノートに知識を記録し、関連ノートへのリンクを追加

#### ノートの例（実際の実装に基づく）

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

#### ノートの配置場所

- `knowledge/zettelkasten/permanent/`: 永続的な知識ノート
- `knowledge/zettelkasten/references/`: 外部資料の要約やリンク
- `knowledge/zettelkasten/structure/`: システム構造や設計に関するノート
- `knowledge/zettelkasten/index/`: 知識ノートのインデックス

---

### ステップ2: タスク生成（GTD）

#### タスクの作成手順

1. 知識ノートから実装可能なタスクを特定
2. `knowledge/inbox/` にタスク/アイデア/メモを追加（共通Inbox）
3. タスクとして採用する場合は `knowledge/tasks/{active|waiting|someday}/` に **コピーしてSSOT化**
4. 元のInboxファイルは `knowledge/inbox/archive/` に移動（入力ログとして保持）
5. 必要に応じてメタデータに `related_notes` を記録

> **運用ルールの詳細**: レビュー・モード、SSOT、コピー→アーカイブ等の詳細は `.cursor/docs_manager_rules.mdc` を参照してください。

#### タスクの例（実際の実装に基づく）

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

#### タスクの配置場所

- `knowledge/tasks/active/`: アクティブなタスク（次にやるべきこと）
- `knowledge/tasks/waiting/`: 待機中タスク（他のタスクの完了を待つ）
- `knowledge/tasks/someday/`: いつかやる/たぶんやるタスク
- `knowledge/tasks/completed/`: 完了したタスク

---

### ステップ3: タスク変換（JSON）

#### MarkdownからJSONへの変換

```bash
python scripts/workflow/task_converter.py
```

このスクリプトは：
- `knowledge/tasks/` 内のMarkdownファイルを読み込み
- JSON形式に変換
- `tasks/current_sprint.json` に保存（上書き）

**重要**: `tasks/current_sprint.json` は自動生成されるため、**手で編集しないでください**。

#### 変換後のJSON構造（実際の実装に基づく）

```json
{
  "generated_at": "2026-01-14T11:52:42",
  "tasks": [
    {
      "id": "task-20260112173705",
      "title": "Disaster Tweets: keyword特徴量の追加実験",
      "type": "task",
      "status": "in_progress",
      "priority": "high",
      "mode": "experiment",
      "project": "kaggle_disaster_tweets_baseline_improvement",
      "assigned_agent": null,
      "assignee": null,
      "context": [
        "project_kaggle_disaster_tweets_baseline_improvement",
        "project_kaggle_disaster_tweets"
      ],
      "dependencies": [
        "exp20260106030720_report"
      ],
      "related_notes": [
        "disaster_tweets_baseline_improvement_ideas_20260112162435",
        "exp20260106030720_report",
        "disaster_tweets_eda_20260105180000"
      ],
      "source_file": "knowledge/tasks/active/task_disaster_tweets_keyword_feature_20260112173705.md",
      "tags": [
        "kaggle",
        "kaggle_disaster_tweets",
        "improvement",
        "feature-engineering",
        "keyword",
        "experiment"
      ],
      "due_date": null,
      "updated_at": "2026-01-12T00:00:00"
    }
  ]
}
```

---

### ステップ4: プロジェクトリンク同期（タスク確定時）

#### プロジェクトとタスクの相互リンクを同期

```bash
python scripts/workflow/sync_project_links.py
```

このスクリプトは：
- タスクに `project` フィールドが設定されている場合に実行
- プロジェクトノートとタスクファイルの相互リンクを自動更新
- タスクノートに `<!-- AUTO:project:start -->` と `<!-- AUTO:project:end -->` の間にプロジェクトリンクを追加
- プロジェクトノートに `<!-- AUTO:tasks:start -->` と `<!-- AUTO:tasks:end -->` の間にタスク一覧を追加

#### 実行タイミング

以下のいずれかの場合に実行：
- ✅ タスクを確定（コピー）した後（`project`フィールドが設定されている場合）
- ✅ タスクの`project`フィールドを変更した後
- ✅ プロジェクトノートを作成・更新した後

#### ドライラン（変更内容の確認のみ）

```bash
python scripts/workflow/sync_project_links.py --dry-run
```

ファイルを更新せずに、変更内容を確認できます。

---

### ステップ5: エージェント実行

#### エージェント実行フロー（実際の実装に基づく）

```
User → Document Manager → Planner → User → Developer → Validator → User → Validator → Document Manager → Version Controller
```

#### 詳細なフロー

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

#### Plannerエージェントの動作

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

---

### ステップ6: 結果記録

#### 実験結果の記録方法

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

#### 実験レポートの例（実際の実装に基づく）

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

---

### ステップ7: フィードバックループ

#### 知識の更新

1. **新しい知識ノート**: 実験から得られた学びを新しいノートとして記録
   - `knowledge/zettelkasten/permanent/` に新しいノートを作成
   - 実験レポートへのリンクを追加

2. **既存ノートの更新**: 関連する既存ノートにリンクを追加
   - 実験レポートの `links` フィールドに既存ノートのIDを追加
   - 既存ノートの `links` フィールドに実験レポートのIDを追加

3. **新しいタスク**: 学びから新しい実装アイディアをタスクとして生成
   - 実験レポートの「次のステップ」から新しいタスクを作成
   - `knowledge/inbox/` に追加 → `knowledge/tasks/active/` にコピー

#### 循環の完成

```
知識 → タスク → 実験 → 学び → 知識 → ...
```

この循環により、知識とタスクが有機的に成長していきます。

---

## エージェント実行フロー（詳細）

### エージェント間の連携

各エージェントは以下の順序で連携します：

```
User → Document Manager → Planner → User → Developer → Validator → User → Validator → Document Manager → Version Controller
```

### 各ステップの詳細

#### Step 1: アイディア受領・情報収集
**担当**: Document Manager

- **入力**: ユーザーのアイディア・フィードバック、関連ドキュメント・リソース
- **処理**: アイディアの整理・要約、関連情報の収集・整理、前回のexperiment結果の確認
- **出力**: 整理されたアイディア、関連情報の要約、コンテキスト情報

#### Step 2: 計画立案
**担当**: Planner

- **入力**: Document Managerからの整理されたアイディア
- **処理**: 実装の目的と仮説を明確化、具体的な実装手順を立案、期待される成果を定量化、リスク要因と対策を特定
- **出力**: 実行計画（`[Plan:]` と `[Action:]`）

#### Step 3: 計画承認
**担当**: ユーザー

- **処理**: Plannerの計画をレビュー、承認または差し戻しの判断

#### Step 4: 実装・実行
**担当**: Developer

- **入力**: 承認された計画
- **処理**: 
  - `experiments/exp[timestamp]_[description]/` ディレクトリの作成
  - コードの実装・実行（train.py, predict.py）
  - 結果ファイルの生成
  - **提出ファイル（submission.csv）の作成まで完了**
- **出力**: Pythonコードブロック、`[Result:]` 実行結果要約
- **引き継ぎ**: Developer → Validator（提出ファイル作成完了後）

#### Step 5: 結果入力依頼・レポート作成
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

#### Step 6: ドキュメント化
**担当**: Document Manager

- **入力**: 実験結果、評価結果
- **処理**: 実験概要の文書化、結果の要約、学んだことの記録
- **出力**: Markdownレポート、実験概要、結果サマリー

#### Step 7: バージョン管理
**担当**: Version Controller

- **入力**: 全ファイル（コード、結果、ドキュメント）
- **処理**: 変更の記録、適切なコミットメッセージの生成、Gitコミットの実行
- **出力**: Gitコマンド、コミットメッセージ

詳細は `.cursor/experiment_flow_instructions.mdc` を参照してください。

---

## 実践例

### 例1: ベースライン実験の実行（実際の例）

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

### 例2: 特徴量追加実験の実行（実際の例）

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

---

## トラブルシューティング

### タスク変換でエラーが出る場合

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

### プロジェクトリンク同期でリンクが更新されない場合

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

### エージェントがタスクを見つけられない場合

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

### 実験レポートが作成されない場合

**問題**: Validatorが実験レポートを作成しない

**原因と解決方法**:
- **結果ファイルの確認**: `results/exp[timestamp]_[description]/exp[timestamp]_metrics.json` が存在するか確認
- **ユーザー入力の確認**: Validatorはユーザーから結果（Public LBスコア等）を受け取る必要がある
- **引き継ぎの確認**: Developerから引き継ぎを受けているか確認

### プロジェクトノートにタスクが表示されない場合

**問題**: プロジェクトノートの「タスク一覧（AUTO）」セクションにタスクが表示されない

**原因と解決方法**:
- **プロジェクトリンク同期の実行**: `python scripts/workflow/sync_project_links.py` を実行
- **projectフィールドの確認**: タスクのYAML frontmatterに `project: <project_name>` が設定されているか確認
- **マーカーの確認**: `<!-- AUTO:tasks:start -->` と `<!-- AUTO:tasks:end -->` が正しく記述されているか確認

---

## ベストプラクティス

### 知識管理

- **ノートは小さく、焦点を絞る**: 1つのノートに1つのトピック
- **関連ノートへのリンクを積極的に作成**: `links` フィールドに追加
- **定期的にノートをレビューし、整理**: 重複や古い情報を統合
- **タイムスタンプ形式のIDを使用**: `YYYYMMDDHHMMSS` 形式で命名

### タスク管理

- **タスクは具体的で実装可能なものにする**: 曖昧な表現を避ける
- **依存関係を明確に記録**: `dependencies` フィールドに追加
- **期待される成果を定量化**: メトリクスや目標値を明確に
- **プロジェクトフィールドを設定**: 関連するプロジェクトを明確に
- **modeフィールドを設定**: `experiment`, `research`, `docs`, `infrastructure` など

### 実験管理

- **各実験の目的を明確にする**: 仮説を明確に記述
- **結果を詳細に記録**: CV結果、Public LBスコア、学んだことを記録
- **失敗した実験からも学びを抽出**: なぜ失敗したかを分析
- **親実験を記録**: `parent_experiment` フィールドに追加
- **関連タスク・ノートをリンク**: 実験レポートの `links` フィールドに追加

### ワークフロー

- **タスク変換は定期的に実行**: タスクを追加・更新・移動した後に実行
- **プロジェクトリンク同期はタスク確定時に実行**: `project` フィールドが設定されている場合
- **エージェント実行前に計画を確認**: Plannerの計画をレビューしてから承認
- **結果入力は迅速に**: Validatorが結果入力を依頼したら、できるだけ早く入力

---

## 関連ドキュメント

- **プロジェクト全体アーキテクチャ**: `docs/project_architecture.md`
- **スクリプトガイド**: `docs/scripts_guide.md`
- **エージェント定義（チーム憲法）**: `.cursor/kaggle_team.mdc`
- **実験フロー指示**: `.cursor/experiment_flow_instructions.mdc`
- **Developer ルール**: `.cursor/developer_experiment_rules.mdc`
- **Docs Manager ルール**: `.cursor/docs_manager_rules.mdc`
- **Version Controller ルール**: `.cursor/version_controller_rules.mdc`
