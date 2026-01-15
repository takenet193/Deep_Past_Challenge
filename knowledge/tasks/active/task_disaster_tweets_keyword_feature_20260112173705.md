---
type: task
id: task-20260112173705
title: "Disaster Tweets: keyword特徴量の追加実験"
author: takeikumi
status: completed
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

#kaggle_disaster_tweets

## 目的

ベースライン実験（exp20260106030720、CV F1=0.7425、Public LB=0.80079）を起点に、**keyword特徴量を追加**して性能を向上させる。

**期待効果**: CV F1 +0.01-0.04程度（CV F1が0.75-0.80程度まで向上する可能性）

## 背景・根拠

### EDAでの発見
- **keywordとtargetの相関が非常に強い**ことが確認されている
  - `debris`=100%災害、`wreckage`=100%災害、`derailment`=100%災害
  - `outbreak`=97.5%災害、`oil%20spill`=97.4%災害
- ベースライン実験では**textのみ**を使用しており、keywordは未使用

### ベースライン結果
- **CV Mean F1**: 0.7425
- **CV Std F1**: 0.0137（安定している）
- **Train F1**: 0.8542
- **Public LB F1**: 0.80079

## 成果物（このタスクの完了条件）

- keyword特徴量を追加した実験のコード・設定・結果が `experiments/exp[timestamp]_keyword_tfidf_lr/` と `results/exp[timestamp]_keyword_tfidf_lr/` に保存されている
- CV評価が完了し、ベースラインとの比較が可能になっている
- `submission.csv` をKaggleに提出し、Public LBの結果を取得している
- 実験結果（CVスコア、Public LB）と学びを実験レポートに記録している
- プロジェクトノート（`project_kaggle_disaster_tweets_baseline_improvement.md`）に実験ログを追加している

## 実施計画（詳細）

### 1. 実験準備
- [ ] 実験IDをタイムスタンプ形式で生成（`exp[timestamp]_keyword_tfidf_lr`）
- [ ] `experiments/exp[timestamp]_keyword_tfidf_lr/` ディレクトリを作成
- [ ] `results/exp[timestamp]_keyword_tfidf_lr/` ディレクトリを作成
- [ ] ベースライン実験（exp20260106030720）のコードをベースに、keyword特徴量を追加したバージョンを作成
  - `exp[timestamp]_config.yaml`
  - `exp[timestamp]_train.py`
  - `exp[timestamp]_predict.py`

### 2. データ確認・分析
- [ ] `data/raw/train.csv` のkeywordカラムを確認
  - [ ] keywordのユニーク数
  - [ ] keywordの欠損値数と割合
  - [ ] keywordとtargetの相関（主要なkeywordの災害率）
- [ ] 欠損値処理方針の決定
  - 候補1: 最頻値で補完
  - 候補2: "unknown"として新しいカテゴリとして扱う
  - 候補3: ターゲットエンコーディング時に欠損値も考慮

### 3. 特徴量エンジニアリング方針の決定

#### 3.1 エンコーディング手法の選択
**候補手法**:
1. **ターゲットエンコーディング（Target Encoding）**
   - 各keywordの災害率（target=1の割合）を特徴量として使用
   - メリット: 線形モデル（LogisticRegression）と相性が良い、情報量が多い
   - デメリット: 過学習のリスク（CVで適切に処理する必要がある）
   - 実装: `sklearn.preprocessing.TargetEncoder` または手動実装

2. **ワンホットエンコーディング（One-Hot Encoding）**
   - 各keywordをバイナリ特徴量に変換
   - メリット: シンプル、解釈しやすい
   - デメリット: keyword数が多い場合、特徴量数が増えすぎる可能性
   - 実装: `pandas.get_dummies()` または `sklearn.preprocessing.OneHotEncoder`

3. **頻度エンコーディング（Frequency Encoding）**
   - 各keywordの出現頻度を特徴量として使用
   - メリット: シンプル、過学習のリスクが低い
   - デメリット: 情報量が少ない可能性

**推奨**: **ターゲットエンコーディング**を最初に試す
- EDAでkeywordとtargetの相関が強いことが確認されている
- LogisticRegressionは線形モデルなので、ターゲットエンコーディングと相性が良い
- CVで適切に実装すれば過学習を防げる

#### 3.2 実装方針
- **train.py**:
  1. データ読み込み
  2. keywordの欠損値処理（"unknown"として扱う、または最頻値で補完）
  3. **ターゲットエンコーディング**:
     - StratifiedKFoldの各フォールドで、trainデータのみを使ってkeywordの災害率を計算
     - testデータ（各フォールドのvalidationデータ）には、trainデータで計算したエンコーディングを適用
     - これにより、データリークを防ぐ
  4. TF-IDF特徴量の作成（ベースラインと同じ）
  5. keyword特徴量とTF-IDF特徴量を結合（`scipy.sparse.hstack` または `numpy.hstack`）
  6. モデル学習・評価

- **predict.py**:
  1. 学習済みモデルとエンコーダーを読み込み
  2. testデータのkeywordに対して、学習時に計算したターゲットエンコーディングを適用
  3. TF-IDF特徴量を作成
  4. 特徴量を結合して予測

### 4. config.yamlの編集
- [ ] `experiment.id`: 実験ID（タイムスタンプ）を設定
- [ ] `experiment.name`: `keyword_tfidf_lr`
- [ ] `experiment.description`: "text + keyword + TF-IDF(1-2gram) + LogisticRegression"
- [ ] `experiment.parent_experiment`: `exp20260106030720`（ベースライン実験）
- [ ] `feature_engineering` セクションにkeywordエンコーディングの設定を追加:
  ```yaml
  feature_engineering:
    type: "tfidf_keyword"
    keyword_encoding:
      method: "target_encoding"  # or: one_hot, frequency
      missing_value_strategy: "unknown"  # or: mode
      smoothing: 1.0  # ターゲットエンコーディングの平滑化パラメータ（オプション）
  ```
- [ ] その他の設定はベースラインと同じ（前処理、TF-IDF、モデル、CV）

### 5. 実装（train.py）

#### 5.1 データ読み込み・前処理
- [ ] データ読み込み（`train.csv`, `test.csv`）
- [ ] textの前処理（ベースラインと同じ: lowercase、URL除去、メンション除去）
- [ ] keywordの欠損値処理

#### 5.2 keyword特徴量エンジニアリング
- [ ] ターゲットエンコーディングの実装
  - StratifiedKFoldの各フォールドで:
    1. trainデータ（fold内）でkeywordごとの災害率を計算
    2. validationデータ（fold外）にエンコーディングを適用
    3. 未知のkeyword（validationにのみ存在）は全体平均で補完
  - 全データで学習する際は、全trainデータでエンコーディングを計算
- [ ] エンコーダーを保存（predict.pyで使用するため）

#### 5.3 TF-IDF特徴量エンジニアリング
- [ ] TF-IDF特徴量の作成（ベースラインと同じ設定）
  - max_features: 20000
  - ngram_range: (1, 2)
  - min_df: 2

#### 5.4 特徴量の結合
- [ ] keyword特徴量（1次元配列）とTF-IDF特徴量（スパース行列）を結合
  - `scipy.sparse.hstack([keyword_features, tfidf_features])` を使用

#### 5.5 モデル学習・評価
- [ ] StratifiedKFoldでCV評価（F1スコア）
- [ ] 全データで学習（最終モデル）
- [ ] Train F1スコアの計算
- [ ] 結果の保存
  - `exp[timestamp]_metrics.json`
  - `exp[timestamp]_cv_results.json`
  - `exp[timestamp]_model.pkl`（モデル、ベクトライザー、エンコーダーを含む）

### 6. 推論・提出ファイル作成（predict.py）
- [ ] 学習済みモデル、ベクトライザー、エンコーダーを読み込み
- [ ] testデータのkeywordに対してエンコーディングを適用
- [ ] testデータのtextに対してTF-IDF特徴量を作成
- [ ] 特徴量を結合して予測
- [ ] `submission.csv` を作成
- [ ] `exp[timestamp]_submission.csv` として保存

### 7. 提出・結果記録
- [ ] Kaggleに `exp[timestamp]_submission.csv` を提出
- [ ] Public LBの結果を取得
- [ ] `exp[timestamp]_metrics.json` にPublic LBスコアを追記
- [ ] `exp[timestamp]_report.md` に実験内容・結果を記録
  - 実験ID、実施日、目的
  - 仮説、実装内容（keywordエンコーディング、TF-IDF、モデル、CV）
  - ハイパーパラメータ
  - 結果（Train F1、CV Mean、CV Std、Public LB）
  - ベースラインとの比較
  - 学んだこと、次のステップ

### 8. プロジェクトノートへの反映
- [ ] プロジェクトノート `project_kaggle_disaster_tweets_baseline_improvement.md` の「状態メモ」に実験ログを追加
- [ ] Public LBスコアと学びをプロジェクトノートに追記

## 実現可能性の検討

### ✅ 揃っているもの
- **データ**: `data/raw/train.csv`, `data/raw/test.csv` が存在
- **ベースラインコード**: `experiments/exp20260106030720_baseline_tfidf_lr/` が存在
- **改善案**: `disaster_tweets_baseline_improvement_ideas_20260112162435.md` に詳細が記載されている
- **技術要素**: 標準ライブラリで実装可能
  - ターゲットエンコーディング: `sklearn.preprocessing.TargetEncoder` または手動実装
  - 特徴量結合: `scipy.sparse.hstack`
  - その他はベースラインと同じ

### ⚠️ 実装時の注意点

#### データリークの防止
- **重要**: CVでターゲットエンコーディングを計算する際、**validationデータの情報を使ってはいけない**
- 各フォールドで、trainデータ（fold内）のみを使ってエンコーディングを計算し、validationデータ（fold外）に適用する
- 全データで学習する際は、全trainデータでエンコーディングを計算し、testデータに適用する

#### 未知のkeywordの処理
- testデータにtrainデータに存在しないkeywordが含まれる可能性がある
- その場合は、全体平均（trainデータ全体の災害率）で補完する

#### 特徴量の結合
- keyword特徴量は1次元配列（または2次元配列）
- TF-IDF特徴量はスパース行列
- `scipy.sparse.hstack` を使用して結合する必要がある

#### エンコーダーの保存
- predict.pyで使用するため、エンコーダーもモデルと一緒に保存する必要がある
- `pickle` で `{'model': model, 'vectorizer': vectorizer, 'keyword_encoder': encoder}` として保存

### ✅ 結論
**実装可能**: ベースラインコードをベースに、keyword特徴量の追加は技術的に問題なく実装可能。データリークに注意して、適切にCVで実装すれば、期待される性能向上が得られる可能性が高い。

## 期待される結果

### ベースラインとの比較
- **ベースライン**: CV F1=0.7425、Public LB=0.80079
- **期待値**: CV F1 +0.01-0.04程度（CV F1が0.75-0.80程度まで向上）
- **目標**: CV F1 0.78-0.80、Public LB 0.82-0.84（短期目標）

### 成功の判断基準
- CV F1がベースライン（0.7425）より向上している
- Public LBがベースライン（0.80079）より向上している
- 過学習が顕著でない（Train F1とCV F1の差が適切）

## 参考資料
- 改善案ノート: [[disaster_tweets_baseline_improvement_ideas_20260112162435|ベースラインからの改善案]]
- ベースライン実験レポート: [[exp20260106030720_report|exp20260106030720_report]]
- EDA結果: [[disaster_tweets_eda_20260105180000|Disaster Tweets - EDA結果]]
- プロジェクトノート: [[project_kaggle_disaster_tweets_baseline_improvement|project: kaggle_disaster_tweets_baseline_improvement]]
- 親プロジェクト: [[project_kaggle_disaster_tweets|project: kaggle_disaster_tweets]]

## 結果（実施報告）
- 実験ID: exp20260112174906
- CV F1 Score: 0.7416 (+/- 0.0139)
- Train F1 Score: 0.8335
- **Public LB F1 Score: 0.77965**
- ベースラインとの比較:
  - CV F1: ほぼ同等（-0.0009）
  - Public LB: **低下**（-0.02114、ベースライン: 0.80079）
- 実験レポート: `results/exp20260112174906_keyword_tfidf_lr/exp20260112174906_report.md`

## 学び
- **期待した性能向上は得られなかった**: keyword特徴量を追加したが、CV F1はほぼ同等、Public LBは低下
- **keyword情報が既にtextに含まれている可能性**: TF-IDF特徴量が既にkeywordの情報を捉えている可能性
- **過学習の緩和**: Train F1が低下（0.8542 → 0.8335）し、Train F1とCV F1の差が縮小
- **ターゲットエンコーディングの調整が必要**: 平滑化パラメータの調整や、ワンホットエンコーディングの試行が必要
- **CVスコアとPublic LBスコアの関係**: CVスコアが向上しても、Public LBが向上するとは限らない

## 次のアクション
- 次の改善案を検討:
  1. ターゲットエンコーディングの平滑化パラメータ調整
  2. ワンホットエンコーディングの試行
  3. ハイパーパラメータチューニング（LogisticRegressionのC値調整）
  4. 閾値調整
  5. 非線形モデルの導入（XGBoost、LightGBMなど）

<!-- AUTO:project:start -->
- [[project_kaggle_disaster_tweets_baseline_improvement|project: kaggle_disaster_tweets_baseline_improvement]]
<!-- AUTO:project:end -->

