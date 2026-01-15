---
type: task
id: task-20260105120020
title: "Disaster Tweets: 提出して結果を記録する"
author: takeikumi
status: active
priority: high
project: kaggle_disaster_tweets
mode: experiment
context:
  - project_kaggle_disaster_tweets
dependencies:
  - task-20260105120011
  - task-20260105180000
related_notes:
  - project_kaggle_disaster_tweets
  - disaster_tweets_eda_20260105180000
created: 2026-01-05
updated: 2026-01-05
tags: [kaggle, kaggle_disaster_tweets, baseline]
---

# タスク: Disaster Tweets: 提出して結果を記録する

#kaggle_disaster_tweets

## 目的
- EDAで決定したベースライン方針に基づいて、最初のモデルを実装・訓練・評価し、提出して結果を記録する
- 実験管理ルール（`.cursor/developer_experiment_rules.mdc`）に従って、再現可能な形で実験を実施する

## 成果物（このタスクの完了条件）
- ベースライン実験のコード・設定・結果が `experiments/exp[timestamp]_baseline_tfidf_lr/` と `results/exp[timestamp]_baseline_tfidf_lr/` に保存されている
- `submission.csv` をKaggleに提出し、Public LBの結果を取得している
- 実験結果（CVスコア、Public LB）と学びをプロジェクトノートに反映している
- 実験README（`exp[timestamp]_README.md`）に実験内容が記録されている

## 実施計画（チェックリスト）

### 1. 実験準備
- [x] 実験IDをタイムスタンプ形式で生成（`exp20260106030720`）
- [x] `experiments/exp20260106030720_baseline_tfidf_lr/` ディレクトリを作成
- [x] `results/exp20260106030720_baseline_tfidf_lr/` ディレクトリを作成
- [x] テンプレートから `config.yaml` と `README.md` をコピーし、**全ファイル名に実験IDを付与**
  - `exp20260106030720_config.yaml`
  - `exp20260106030720_report.md`（実験レポート）
  - `exp20260106030720_train.py`
  - `exp20260106030720_predict.py`

### 2. config.yamlの編集
- [x] `experiment.id`: 実験ID（タイムスタンプ）を設定（`exp20260106030720`）
- [x] `experiment.name`: `baseline_tfidf_lr_text_only`
- [x] `experiment.description`: "textのみ + TF-IDF(1-2gram) + LogisticRegression"
- [x] `experiment.created_at`: ISO形式の日時（`2026-01-06T03:07:20`）
- [x] `data.train_path`: `"data/raw/train.csv"`（生データを使用）
- [x] `data.test_path`: `"data/raw/test.csv"`
- [x] `preprocessing.lowercase`: `true`
- [x] `preprocessing.remove_urls`: `true`（効果確認のため）
- [x] `preprocessing.remove_mentions`: `true`
- [x] `preprocessing.remove_hashtags`: `false`（意味を持つ可能性あり）
- [x] `feature_engineering.type`: `"tfidf"`
- [x] `feature_engineering.params.max_features`: `20000`（EDAで決定）
- [x] `feature_engineering.params.ngram_range`: `[1, 2]`（EDAで決定）
- [x] `feature_engineering.params.min_df`: `2`
- [x] `model.type`: `"LogisticRegression"`
- [x] `model.params.C`: `1.0`
- [x] `model.params.max_iter`: `2000`
- [x] `model.params.random_state`: `42`
- [x] `validation.method`: `"stratified_kfold"`
- [x] `validation.n_folds`: `5`
- [x] `validation.shuffle`: `true`
- [x] `validation.random_state`: `42`
- [x] `seed`: `42`

### 3. 実装（train.py）
- [x] `config.yaml` を読み込み、リポジトリルート基準でパス解決
- [x] データ読み込み（`train.csv`, `test.csv`）
- [x] 前処理（lowercase、URL除去、メンション除去）
- [x] TF-IDF特徴量エンジニアリング（configの設定に従う）
- [x] StratifiedKFoldでCV評価（F1スコア）
  - CV F1 Score: 0.7425 (+/- 0.0137)
  - CV Scores: [0.7587, 0.7444, 0.7178, 0.7411, 0.7506]
- [x] 全データで学習（最終モデル）
  - Train F1 Score: 0.8542
- [x] 結果の保存
  - `exp20260106030720_metrics.json`（CV Mean: 0.7425, CV Std: 0.0137, Train F1: 0.8542）
  - `exp20260106030720_cv_results.json`（各フォールドの詳細）
  - `exp20260106030720_model.pkl`（学習済みモデル）

### 4. 推論・提出ファイル作成（predict.py）
- [x] 学習済みモデルを読み込み
- [x] testデータに対して予測
- [x] `submission.csv` を作成（`id, target` 形式）
- [x] `exp20260106030720_submission.csv` として保存
  - 予測分布: {0: 2171, 1: 1092}

### 5. 提出・結果記録
- [x] Kaggleに `exp20260106030720_submission.csv` を提出
- [x] Public LBの結果を取得: **0.80079**
- [x] `exp20260106030720_metrics.json` にPublic LBスコアを追記
- [x] `exp20260106030720_report.md` に実験内容・結果を記録
  - 実験ID、実施日、目的
  - 仮説、実装内容（前処理/特徴量/モデル/CV）
  - ハイパーパラメータ
  - 結果（Train F1: 0.8542, CV Mean: 0.7425, CV Std: 0.0137, Public LB: 未提出）
  - 学んだこと、次のステップ

### 6. プロジェクトノートへの反映
- [x] プロジェクトノート `project_kaggle_disaster_tweets.md` の「ベースライン実験ログ」に実験レポートへのリンクを追加
- [x] Public LBスコア（0.80079）と学びをプロジェクトノートに追記

### 7. Git管理
- [ ] 実験コード（`.py`）、`config.yaml`、`exp20260106030720_report.md` をコミット
- [ ] 結果ファイル（`metrics.json`, `submission.csv`）をコミット
- [ ] コミットメッセージ: `exp(baseline): ベースラインTF-IDF+LRモデル exp20260106030720`

## 実現可能性の検討

### ✅ 揃っているもの
- **データ**: `data/raw/train.csv`, `data/raw/test.csv` が存在
- **ベースライン方針**: EDAで決定済み（textのみ、TF-IDF、LogisticRegression）
- **実験管理ルール**: `.cursor/developer_experiment_rules.mdc` で明確に定義
- **テンプレート**: `experiments/_template_experiment/config.yaml`, `README.md` が存在
- **技術要素**: 標準ライブラリで実装可能
  - TF-IDF: `sklearn.feature_extraction.text.TfidfVectorizer`
  - LogisticRegression: `sklearn.linear_model.LogisticRegression`
  - StratifiedKFold: `sklearn.model_selection.StratifiedKFold`
  - F1スコア: `sklearn.metrics.f1_score`
  - モデル保存: `pickle` または `joblib`

### ⚠️ 新規作成が必要なもの
- **train.py**: テンプレートがないため、新規作成が必要
  - config.yaml読み込み、データ読み込み、前処理、特徴量エンジニアリング、CV評価、モデル学習、結果保存
- **predict.py**: テンプレートがないため、新規作成が必要
  - モデル読み込み、testデータ読み込み、予測、submission.csv作成

### 📝 実装時の注意点
- **前処理の実装**:
  - URL除去: 正規表現 `r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'`
  - メンション除去: 正規表現 `r'@\w+'`
  - lowercase: `str.lower()`
- **パス解決**: リポジトリルート基準で相対パスを解決（`Path(__file__).parent.parent.parent`）
- **結果保存先**: `results/exp[timestamp]_baseline_tfidf_lr/` に実験ID付きファイル名で保存
- **依存関係**: `task-20260105120011`（Discussion探索）は参考程度で、必須ではない可能性あり

### ✅ 結論
**実装可能**: 必要な情報・方針・ルールは揃っており、標準的なライブラリで実装可能。`train.py` と `predict.py` の新規作成が必要だが、技術的には問題なし。

## 参考資料
- EDA結果: [[disaster_tweets_eda_20260105180000|Disaster Tweets - EDA結果]]
- 実験管理ルール: `.cursor/developer_experiment_rules.mdc`
- テンプレート: `experiments/_template_experiment/`
- プロジェクトノート: [[project_kaggle_disaster_tweets|project: kaggle_disaster_tweets]]
- 改善案: [[disaster_tweets_baseline_improvement_ideas_20260112162435|ベースラインからの改善案]]

## 結果（実施報告）
- ベースライン実験（exp20260106030720）を実装・実行完了
- CV F1 Score: 0.7425 (+/- 0.0137)、Train F1 Score: 0.8542
- **Public LB F1 Score: 0.80079**（CVより高い！）
- submission.csvを作成・提出完了
- 実験レポート（`exp20260106030720_report.md`）に実験内容・結果を記録
- プロジェクトノートに実験ログへのリンクとPublic LBスコアを追記
- **残タスク**: Gitコミット

## 学び
- シンプルなベースライン（textのみ + TF-IDF + LogisticRegression）でCV F1=0.7425、**Public LB=0.80079**を達成
- **Public LBがCVより高い**（0.80079 vs 0.7425）のは興味深い結果
  - CVが保守的だった可能性、またはtestデータの分布がtrainと異なる可能性
- Train F1=0.8542とCV F1=0.7425の差から、やや過学習の傾向が見られるが、Public LBは良好
- CVスコアの標準偏差が0.0137と比較的小さく、安定している
- 実験管理ルールに従った実装により、再現可能な実験が実現できた

<!-- AUTO:project:start -->
- [[project_kaggle_disaster_tweets|project: kaggle_disaster_tweets]]
<!-- AUTO:project:end -->


