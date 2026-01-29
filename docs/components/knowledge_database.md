# 知識・タスクデータベース (KaggleBase)

## 概要

Obsidianを用いた知識管理システム。Zettelkasten（永続的な知識）とGTD（実行可能なタスク）を組み合わせ、有機的な知識循環を実現します。

## 名称提案: **KaggleBase** (Kaggle Knowledge Base)

代替案: CompetitionVault, InsightHub, ML-Zettel

## 実装済み機能

### ディレクトリ構造

```
knowledge/
├── inbox/                      # 未整理の情報
│   ├── _inbox_guide.md        # ガイド
│   ├── YYYYMMDD_idea_*.md     # アイディアメモ
│   ├── YYYYMMDD_reference_*.md # 参考資料候補
│   ├── YYYYMMDD_task_candidate_*.md # タスク候補
│   └── archive/                # アーカイブ
│
├── zettelkasten/              # 知識ノート（永続的）
│   ├── _zettelkasten_guide.md # ガイド
│   ├── permanent/             # 永続ノート
│   │   ├── 20240101000000_feature_engineering_basics.md
│   │   └── 20240102000000_gradient_boosting_theory.md
│   ├── references/            # 外部資料（論文、書籍等）
│   │   ├── papers/            # 学術論文
│   │   └── books/             # 書籍
│   ├── structure/             # 構造・設計に関するノート
│   └── index/                 # インデックス
│
├── tasks/                     # GTDタスク管理
│   ├── _gtd_guide.md          # ガイド
│   ├── _MASTER_TASKS.md       # マスタータスクリスト
│   ├── active/                # アクティブなタスク
│   │   ├── task_YYYYMMDDHHMMSS_*.md
│   │   └── _active_guide.md
│   ├── waiting/                # 待機中
│   │   └── _waiting_guide.md
│   ├── someday/                # いつかやる
│   │   └── _someday_guide.md
│   ├── completed/              # 完了
│   │   └── _completed_guide.md
│   ├── projects/               # プロジェクト（複数タスクの集合）
│   │   ├── project_*.md
│   │   ├── archive/            # アーカイブ済みプロジェクト
│   │   └── _projects_guide.md
│   └── archive/                # アーカイブ
│       └── _archive_guide.md
│
└── templates/                 # テンプレート
    ├── inbox/
    ├── tasks/
    └── zettelkasten/
```

### タグ規則体系

実際の実装では、**YAMLフロントマターのフィールド**と**タグ**を組み合わせて管理しています。

### 1. タイプ管理（YAMLフロントマターの`type`フィールド）
- `type: task` - タスク（GTD）
- `type: project` - プロジェクト（複数タスクの集合）
- `type: idea` - アイディア
- `type: permanent` - 永続ノート（Zettelkasten）
- `type: reference` - 参考資料

### 2. ステータス管理（YAMLフロントマターの`status`フィールド）
- `status: inbox` - 未整理（inbox/）
- `status: active` - アクティブ（tasks/active/）
- `status: waiting` - 待機中（tasks/waiting/）
- `status: completed` - 完了（tasks/completed/）
- `status: archived` - アーカイブ

### 3. プロジェクト管理（YAMLフロントマターの`project`フィールド）
- `project: kaggle_disaster_tweets` - コンペ固有プロジェクト
- `project: docs_revision` - ドキュメント改訂プロジェクト
- `project: infrastructure` - インフラ整備プロジェクト

### 4. タグ（YAMLフロントマターの`tags`フィールド）
タグは**フラットな形式**で使用されます。主なタグ例：

**コンペ・プロジェクト関連**:
- `kaggle` - Kaggle関連全般
- `kaggle_disaster_tweets` - Disaster Tweetsコンペ
- `project` - プロジェクト関連
- `docs` - ドキュメント関連

**タスク・作業関連**:
- `experiment` - 実験関連
- `improvement` - 改善関連
- `hyperparameter` - ハイパーパラメータ関連
- `baseline` - ベースライン関連

**技術・領域関連**:
- `nlp` - 自然言語処理
- `eda` - 探索的データ分析
- `logistic-regression` - モデル名
- `tfidf` - 特徴量エンジニアリング手法

**その他**:
- `gtd` - GTDシステム関連
- `reference` - 参考資料
- `report` - レポート

### Zettelkastenノートテンプレート（permanent/）

```markdown
---
id: 20240101000000
title: Gradient Boostingの基礎理論
author: takeikumi
type: permanent
form: note  # or: report, summary
tags: [kaggle, model, gradient-boosting, xgboost]
links:
  - project_kaggle_disaster_tweets  # 関連プロジェクト
  - 20240102000000  # 関連ノートへのリンク
created: 2024-01-01
updated: 2024-01-15
---

# Gradient Boostingの基礎理論

## 内容

Gradient Boostingの基本的な考え方と数学的背景について...

## 主要な概念
1. 損失関数の勾配
2. 弱学習器の逐次追加
3. 学習率とその影響

## 実践的な知見
- XGBoost vs LightGBM vs CatBoost
- ハイパーパラメータのチューニング戦略

## 学び
実験exp20260106030720の結果から、学習率を0.1から0.05に下げることで...

## 関連ノート
- [[project_kaggle_disaster_tweets|プロジェクト: Disaster Tweets]]
- [[20240102000000|関連ノート名]]
```

### GTDタスクテンプレート（tasks/active/）

```markdown
---
type: task
id: task-20240115120000
title: 'Disaster Tweets: ベースラインモデルの構築'
author: takeikumi
status: active
priority: high
project: kaggle_disaster_tweets
mode: experiment  # or: research, infrastructure, docs
context:
  - project_kaggle_disaster_tweets
dependencies: []
related_notes:
  - disaster_tweets_eda_20260105180000
created: 2024-01-15
updated: 2024-01-15
tags:
  - kaggle
  - kaggle_disaster_tweets
  - baseline
  - experiment
---

# タスク: Disaster Tweets - ベースラインモデルの構築

## 目的

Disaster Tweetsコンペの初期ベースラインとして、TF-IDF + LogisticRegressionモデルを構築し評価する。

## 期待される成果
- CV F1 Score > 0.70
- Public LB Score > 0.75
- 実験コードと結果が適切に保存されている

## 実行手順
1. データの読み込み（train.csv, test.csv）
2. 前処理（lowercase、URL除去、メンション除去）
3. TF-IDF特徴量エンジニアリング
4. LogisticRegressionモデルの訓練
5. 5-fold StratifiedKFold CVによる評価
6. 提出用CSV生成

## 完了条件
- [ ] 実験コードが`experiments/expYYYYMMDDHHMMSS_*/`に保存されている
- [ ] 評価結果が`results/expYYYYMMDDHHMMSS_*/`に保存されている
- [ ] 実験レポート（`expYYYYMMDDHHMMSS_report.md`）が作成されている
- [ ] Gitにコミットされている

## 実験結果（後で記入）
- 実験ID: 
- CV F1 Score: 
- Public LB: 
- 学んだこと:
```

### プロジェクトテンプレート（tasks/projects/）

```markdown
---
type: project
id: project-[project-name]
title: [プロジェクト名]
project: [project_id]
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - project
  - [関連タグ]
status: active
---

# [プロジェクト名]

## タスク一覧（Dataview）

```dataview
TABLE WITHOUT ID
  default(id, file.name) AS id,
  link(file.path, default(title, file.name)) AS task,
  status,
  priority,
  due_date,
  mode,
  updated
FROM "knowledge/tasks"
WHERE type = "task" AND project = this.project
SORT choice(status="active",0, choice(status="waiting",1, choice(status="someday",2, 3))) ASC,
  choice(priority="critical",0, choice(priority="high",1, choice(priority="medium",2, 3))) ASC,
  due_date ASC,
  updated DESC
```

## 目的 / 成果物

[プロジェクトの目的と期待される成果物]

### 背景

[プロジェクトの背景]

### 成果物

[期待される成果物のリスト]

## 状態メモ

- 開始日: YYYY-MM-DD
- 現在の実装状況:
  - [実装状況のメモ]

## 関連ノート（情報ハブ）

[関連する知識ノートへのリンク]
```

## 将来実装予定

### Kaggle Discussion自動取り込みパイプライン

Kaggle APIを使用してディスカッションを定期的に取得し、`knowledge/references/kaggle_discussions/`に保存する機能。

詳細は「[将来実装機能の詳細設計](../future_features.md)」セクションを参照してください。

## 関連ドキュメント

- [プロジェクトアーキテクチャ](../project_architecture.md) - システム設計の概要
- [システム概要](../system_overview.md) - システム全体の概要
- [JSON形式タスク管理システム](./task_management.md) - タスク管理システムの詳細

