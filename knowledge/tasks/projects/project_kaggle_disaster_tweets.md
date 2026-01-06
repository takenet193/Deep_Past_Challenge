---
type: project
id: project-kaggle_disaster_tweets
title: Kaggle Disaster Tweets（NLP Getting Started）
project: kaggle_disaster_tweets
created: 2026-01-05
updated: 2026-01-05
tags:
- project
- kaggle
- baseline
- kaggle_disaster_tweets
links: []
---

# Project: kaggle_disaster_tweets

#kaggle_disaster_tweets

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

<!-- AUTO:tasks:start -->
## タスク一覧（AUTO）

### active
- [[task_disaster_tweets_find_discussions_20260105120011|task-20260105120011: Disaster Tweets: 参考にすべきDiscussion/Notebookを見つける]]
- [[task_disaster_tweets_improvement_loop_20260105120030|task-20260105120030: Disaster Tweets: 改善ループ（ディスカッション収集→実験→記録）を回す]]

### completed
- [[task_disaster_tweets_overview_20260105120010|task-20260105120010: Disaster Tweets: データをダウンロードして配置を確定する]]
- [[task_disaster_tweets_baseline_submit_20260105120020|task-20260105120020: Disaster Tweets: 提出して結果を記録する]]
- [[task_disaster_tweets_competition_rules_metrics_20260105121000|task-20260105121000: Disaster Tweets: コンペ内容（ルール/評価基準/提出形式）を調べて確定する]]
- [[task_disaster_tweets_eda_20260105170000|task-20260105170000: Disaster Tweets: EDA（データ概観とベースライン設計の当たりを付ける）]]
- [[task_disaster_tweets_experiment_management_20260105180000|task-20260105180000: Disaster Tweets: 実験管理方法を確定する]]
<!-- AUTO:tasks:end -->

## 目的 / 成果物
- まずは「動く」最小ベースライン（学習・CV・推論・提出ファイル作成）を作り、以降の改善の比較基準にする
- 再現可能な実験形（seed / CV分割 / ログ / 結果記録）を整える

## 状態メモ
- コンペ名/URL: `https://www.kaggle.com/competitions/nlp-getting-started`
- 評価指標: F1（高いほど良い）
- 提出形式: `submission.csv`（列: `id`, `target` / targetは 1=災害, 0=非災害）
- データ配置: `data/raw/`（`train.csv`, `test.csv`。Gitには載せない）

## 公式情報（SSOT）
- 概要（Description）
  - NLP入門向けの “Getting Started” コンペ
  - 目的: ツイートが **実災害（real disasters）** に関するものか、そうでないかを分類する
  - 背景: 災害時のTwitterは重要な情報源だが、比喩表現などで **人間には明らかでも機械には曖昧**なケースがある
  - データ規模: 手分類されたツイート約 **10,000件**
  - 実行環境: Kaggle Notebooks（無料・セットアップ不要のJupyter環境）でも完結可能
  - 注意: データに **不適切（罵倒/卑語/攻撃的）** な表現が含まれる可能性あり
  - 参考: Kaggle Discord（コミュニティ）あり（必要時にリンクを控える）
- ルール（Competition Rules / 要点）
  - アカウント: **1人1アカウント**（複数アカウントからの提出は禁止）
  - 共有: **チーム外への私的共有（コード/データ）は禁止**
    - ただし、フォーラム等で **全参加者に公開**する形の共有はOK
  - チーム:
    - 最大 **10人**
    - チームマージ可（期限あり / 合算提出数が上限以内であること）
  - 提出:
    - 1日 **最大10回**
    - 最終提出として **最大2件**を選択可能
  - タイムライン:
    - Start: 2019-12-20
    - End: なし（常設）
  - データ利用: **Competition Use + Academic / Non-Commercial（非商用）**のみ
  - 公開データのためKaggleランキングポイント対象外
  - チート禁止: **手作業でのラベリング（Hand-labeling）は禁止**
  - AutoML: 適切なライセンスがあれば **利用可**
- 評価指標（Evaluation）: F1
  - 提出は「予測」と「正解」の間のF1で評価される
- 提出形式（Submission File）
  - testの各 `id` について、ツイートが実災害なら `1`、そうでなければ `0` を予測
  - ヘッダー付きで `id,target` の2列（例: `0,0` / `3,1`）

## データ
- 配置（ローカル）: `data/raw/`
  - `data/raw/train.csv`
  - `data/raw/test.csv`
  - `data/raw/sample_submission.csv`
- ファイル/列
  - `train.csv`: `id, keyword, location, text, target`
    - `target`: 1=災害 / 0=非災害
  - `test.csv`: `id, keyword, location, text`（targetなし）
  - `sample_submission.csv`: `id, target`（提出フォーマット例）
- EDA結果（要点）:
  - 欠損: `keyword` 約0.8%、`location` 約33%、`text` なし
  - target分布: 0が57% / 1が43%（軽度不均衡、StratifiedKFoldで対応）
  - テキスト長: 平均約100文字、最大157文字
  - keyword: 221種類、targetとの相関が強い（例: debris=100%災害）
  - ベースライン方針: `text` のみ使用、`location` は使わない、`keyword` は改善時に検討
- EDA詳細ノート: [[disaster_tweets_eda_20260105180000|EDA結果（詳細）]]

## ベースライン
- 方針（EDAで確定）:
  - 特徴量: `text` のみ使用（`keyword`/`location` は改善時に検討）
  - 前処理: lowercase、URL/メンション除去は効果確認しながら判断
  - 特徴量エンジニアリング: TF-IDF（ngram_range=(1,2), max_features=20000）
  - モデル: LogisticRegression（`predict_proba`で閾値調整しやすい）
  - CV: StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
- ベースライン実験ログ:
  - [[exp20260106030720_report|exp20260106030720: baseline_tfidf_lr_text_only]] - CV F1: 0.7425, Train F1: 0.8542, **Public LB: 0.80079**

## ディスカッション / ノートブック
- ベースラインに触れているDiscussion/Notebook:
  - （見つけたらリンク＋学びを1行）
  - （見つけたらリンク＋学びを1行）

## 実験データ管理（このプロジェクトの運用）

### ディレクトリ構造・命名規則
- **実験コード**: `experiments/exp[timestamp]_[description]/`（タイムスタンプ形式、衝突回避）
- **実験結果**: `results/exp[timestamp]_[description]/`（分離型）
- **前処理済みデータ**: `data/processed/[pipeline_name]/`（前処理パイプラインごと）
- **全ファイルに実験ID付与**: 実験ディレクトリ内・resultsディレクトリ内の全ファイルに同じタイムスタンプを付与

### 設定ファイル・ログ
- **config.yaml**: テンプレート（`experiments/_template_experiment/config.yaml`）をコピーし、実験IDと設定を編集
- **実行ログ**: `metrics.json`（評価指標）、`cv_results.json`（各フォールド詳細）、`.log`（オプション）
- **seed固定**: 全実験で `random_state=42` を統一

### Git管理方針
- **コミット対象**: 実験コード（`.py`）、`config.yaml`、`README.md`、軽量な結果ファイル（`metrics.json`, `submission.csv`）
- **除外対象**: モデルファイル（`.pkl`）、ログファイル（`.log`）※`.gitignore` で除外
- **コミットメッセージ**: `[expID] 実験内容の要約`

### 実験ノートとの連携
- **実験README**: `experiments/_template_experiment/README.md` テンプレートを使用
- **zettelkasten/permanent**: 実験結果は `form: report` でノート化
- **プロジェクトノート**: 各実験のREADMEへのリンクを「ベースライン実験ログ」に追記

### 詳細ルール
- **Developer実験運用ルール**: `.cursor/developer_experiment_rules.mdc` を参照

## 運用メモ
- このコンペ固有のノートには `#kaggle_disaster_tweets` を付ける（抽出/転用のため）
- 重要な決定（CV/metric/seed/提出形式）は、このノートにまず追記してから各ノートへ展開する

## 関連ノート（情報ハブ）
- `docs/project_architecture.md`
- `knowledge/zettelkasten/permanent/kaggle_basics_20240101.md`
- `knowledge/zettelkasten/permanent/model_selection_20240103.md`


