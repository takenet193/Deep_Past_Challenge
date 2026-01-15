---
type: task
id: task-20260112182239
title: 'Disaster Tweets: LogisticRegressionのC値チューニング'
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
created: 2026-01-12
updated: 2026-01-12
tags:
- kaggle
- kaggle_disaster_tweets
- improvement
- hyperparameter
- logistic-regression
- experiment
---

# タスク: Disaster Tweets - LogisticRegressionのC値チューニング

#kaggle_disaster_tweets

## 目的

ベースライン実験（exp20260106030720、CV F1=0.7425、Public LB=0.80079）を起点に、**LogisticRegressionのC値をチューニング**して性能を改善する。

**期待効果（アイデアノートより）**:
- CV F1が+0.01〜0.02程度向上し、0.75〜0.77程度まで上がる可能性

## 背景・前提

- 現在の設定:
  - C: 1.0（デフォルト）
  - max_iter: 2000
  - solver: 'lbfgs'（sklearnのデフォルト）
- ベースライン結果:
  - CV Mean F1: 0.7425
  - CV Std F1: 0.0137
  - Train F1: 0.8542
  - Public LB: 0.80079
- keyword特徴量追加実験（exp20260112174906）ではPublic LBが悪化したため、**一旦textのみ + TF-IDF + LRのベースライン構成に戻して、C値のチューニングに集中する。**

## 方針

1. **ベースライン構成を固定**:
   - データ: `train.csv`, `test.csv`
   - 特徴量: textのみ + TF-IDF(1,2), max_features=20000, min_df=2
   - モデル: LogisticRegression（solverは基本的に'lbfgs'）
   - CV: StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

2. **C値グリッドサーチ（手動スイープ）**:
   - 候補: `[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]`
   - まずはsolver='lbfgs'固定でCのみを変化させる
   - CV F1とTrain F1の両方を記録し、**汎化性能と過学習のバランス**を評価

3. **拡張オプション（後続候補）**:
   - solverの変更: 'lbfgs' vs 'liblinear' vs 'saga'
   - `class_weight='balanced'`の有無
   - ただし、最初のタスクではC値のみをチューニングし、solver/クラス重みは別タスクに分離する。

## 実施計画（チェックリスト）

### 1. 実験設計の整理
- [ ] ベースライン設定（exp20260106030720）の再確認（configとtrain.py）
- [ ] C値のグリッド: `[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]` を採用することを明文化
- [ ] 比較軸を定義:
  - CV Mean F1
  - CV Std
  - Train F1
  - Public LB（ベストCのみ提出）

### 2. 実験ディレクトリの準備
- [ ] 新しい実験IDをタイムスタンプ形式で決定（例: `exp20260112xxxxxx_lr_c_tuning`）
- [ ] `experiments/exp[timestamp]_lr_c_tuning/` ディレクトリを作成
- [ ] `results/exp[timestamp]_lr_c_tuning/` ディレクトリを作成
- [ ] ベースラインの`config.yaml`と`train.py`/`predict.py`をコピーし、実験IDに合わせてリネーム
  - `exp[timestamp]_config.yaml`
  - `exp[timestamp]_train.py`
  - `exp[timestamp]_predict.py`

### 3. config.yamlの設計
- [ ] `experiment.id`: 新しい実験IDを設定
- [ ] `experiment.name`: `lr_c_tuning_text_only`
- [ ] `experiment.description`: "textのみ + TF-IDF + LogisticRegression (C値グリッドサーチ)"
- [ ] `experiment.parent_experiment`: `exp20260106030720`
- [ ] `model.params`にC値の候補リストを追加（コード側で読み取る想定）:
  ```yaml
  model:
    type: "LogisticRegression"
    params:
      C: 1.0           # デフォルト（ベースライン値）
      max_iter: 2000
      random_state: 42
    c_grid: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
  ```

### 4. train.pyの拡張（C値スイープ）

- [ ] 既存のベースライン`train.py`をベースに、以下を追加:
  1. `c_grid`をconfigから読み込む
  2. forループでCを回し、各Cで以下を実施:
     - モデル定義: `LogisticRegression(C=C, ...)`
     - StratifiedKFoldでCV評価（F1）
     - 全データで学習し、Train F1を計算
     - 結果をリストに格納（C, Train F1, CV Mean, CV Std, CVスコア配列）
  3. 全Cの結果を`results/exp[timestamp]_c_search.json`として保存
  4. **ベストCの選択基準**:
     - CV Mean F1が最大のC
     - 同点の場合は、より小さいC（より強い正則化）を優先
  5. ベストCで最終モデルを再学習し、`metrics.json`にベストC情報を含めて保存:
     - `best_C`, `best_cv_mean`, `best_cv_std`, `best_train_f1`

- [ ] ログ出力:
  - 各CのCVスコアとTrain F1をprint
  - ベストCのサマリーをprint

### 5. predict.pyの確認

- [ ] 既存のベースライン`predict.py`を流用（Cは学習済みモデルに含まれるため変更不要）
- [ ] 新しい実験IDとディレクトリに合わせてパスだけ調整

### 6. 提出と結果取得

- [ ] `exp[timestamp]_train.py`を実行し、ベストCを含むモデルと`submission.csv`を生成
- [ ] `exp[timestamp]_predict.py`を実行（必要なら）し、提出ファイルを確認
- [ ] Kaggleに提出（APIまたはWeb UI）
- [ ] Public LBスコアを取得し、`metrics.json`に追記

### 7. レポート・プロジェクトノートへの反映

- [ ] `results/exp[timestamp]_lr_c_tuning/exp[timestamp]_report.md` を作成
  - Cグリッドと各Cの結果一覧
  - ベストCとベースラインとの比較（Train/CV/Public LB）
  - 過学習の度合いの変化
  - 次に試すべきハイパーパラメータ（solver、class_weightなど）
- [ ] プロジェクトノート `project_kaggle_disaster_tweets_baseline_improvement.md` の「状態メモ」に実験ログを追加

## 実現可能性

### ✅ 揃っているもの

- ベースラインコード一式（`exp20260106030720_baseline_tfidf_lr`）
- 安定したCV設定（StratifiedKFold, random_state=42）
- C値候補のリスト（アイデアノートで既に定義済み）

### ⚠️ 注意点

- Cを大きくしすぎると過学習が悪化する可能性があるため、**Train F1とCV F1の差**を常に確認する
- solverやclass_weightを同時に動かすと、何が効いたのか分かりづらくなるため、**このタスクではCだけに絞る**

## 成功の判断基準

- CV Mean F1がベースライン（0.7425）より有意に高い（目安: +0.005〜0.01以上）
- Public LBがベースライン（0.80079）以上
- Train F1とCV F1の差が適度に小さい（過学習が悪化していない）

## 結果（実施報告）
- 実験ID: exp20260112201310
- C値グリッドサーチ: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
- ベストC: 5.0
- CV Mean F1: 0.7469（ベースライン: 0.7425、+0.0044）
- CV Std: 0.0100（ベースライン: 0.0137、改善）
- Train F1: 0.9408（ベースライン: 0.8542、+0.0866）
- **Public LB F1: 0.80202**（ベースライン: 0.80079、**+0.00123**）
- 実験レポート: `results/exp20260112201310_lr_c_tuning/exp20260112201310_report.md`

## 学び
- **C値チューニングの効果**: C値を最適化（C=5.0）することで、CV F1とPublic LBの両方が向上
- **過学習と汎化性能のバランス**: Train-CV Gapが大きくなっても（0.1117 → 0.1940）、Public LBが向上する場合がある
- **CV Stdの重要性**: CV Stdが改善（0.0100）することで、予測の安定性が向上し、Public LB向上に寄与
- **C値の選択基準**: CV Mean F1が最大のCを選択するのが基本だが、過学習が大きい場合は代替案（C=2.0）も検討する価値がある

## 次のアクション
- 次の改善案を検討:
  1. C=2.0での再実験（過学習が少ない、汎化性能が高い可能性）
  2. 閾値調整（予測確率の閾値を調整してF1スコアを最適化）
  3. solverの変更（'lbfgs' vs 'liblinear' vs 'saga'）
  4. class_weightの調整（`class_weight='balanced'`）
  5. 非線形モデルの導入（XGBoost、LightGBMなど）

<!-- AUTO:project:start -->
- [[project_kaggle_disaster_tweets_baseline_improvement|project: kaggle_disaster_tweets_baseline_improvement]]
<!-- AUTO:project:end -->
