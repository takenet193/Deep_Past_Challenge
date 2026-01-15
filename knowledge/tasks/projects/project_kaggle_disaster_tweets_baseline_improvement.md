---
type: project
id: project-kaggle_disaster_tweets_baseline_improvement
title: Kaggle Disaster Tweets - ベースライン改善実装プロジェクト
project: kaggle_disaster_tweets_baseline_improvement
created: 2026-01-12
updated: 2026-01-12
tags:
- project
- kaggle
- kaggle_disaster_tweets
- baseline
- improvement
links:
- disaster_tweets_baseline_improvement_ideas_20260112162435
- project_kaggle_disaster_tweets
- exp20260106030720_report
---

# Project: kaggle_disaster_tweets_baseline_improvement

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

## 目的 / 成果物

ベースライン実験（exp20260106030720、CV F1=0.7425、Public LB=0.80079）を起点に、改善案を実装して性能を向上させる。

**目標**:
- **短期目標**: CV F1 0.78-0.80、Public LB 0.82-0.84
- **中期目標**: CV F1 0.82-0.85、Public LB 0.85-0.87
- **長期目標**: CV F1 0.85-0.90、Public LB 0.88-0.92

## 状態メモ

- **ベースライン**: CV F1=0.7425、Public LB=0.80079
- **改善案ノート**: [[disaster_tweets_baseline_improvement_ideas_20260112162435|ベースラインからの改善案]]
- **親プロジェクト**: [[project_kaggle_disaster_tweets|kaggle_disaster_tweets]]

### 実験ログ

#### exp20260112174906: keyword特徴量の追加
- **実施日**: 2026-01-12
- **目的**: keyword特徴量を追加して性能向上を目指す
- **結果**: 
  - CV F1: 0.7416（ベースライン: 0.7425、-0.0009）
  - Public LB: **0.77965**（ベースライン: 0.80079、**-0.02114**）
- **評価**: 期待した性能向上は得られなかった。keyword情報が既にtextに含まれている可能性。
- **レポート**: [[exp20260112174906_report|exp20260112174906_report]]
- **関連タスク**: [[task-20260112173705|task_disaster_tweets_keyword_feature_20260112173705]]

#### exp20260112201310: C値チューニング
- **実施日**: 2026-01-12
- **目的**: LogisticRegressionのC値をチューニングして性能向上を目指す
- **結果**: 
  - ベストC: 5.0
  - CV F1: 0.7469（ベースライン: 0.7425、+0.0044）
  - Public LB: **0.80202**（ベースライン: 0.80079、**+0.00123**）
- **評価**: Public LBが向上し、目標を達成。ただし過学習が悪化（Train-CV Gap: 0.1117 → 0.1940）。
- **レポート**: [[exp20260112201310_report|exp20260112201310_report]]
- **関連タスク**: [[task-20260112182239|task_disaster_tweets_lr_c_tuning_20260112182239]]

#### exp20260115_bert_colab: BERTモデル（Colab実行）
- **実施日**: 2026-01-15
- **目的**: 深層学習モデル（BERT）による性能向上を目指す
- **結果**: 
  - CV評価: スキップ（動作確認・学習時間短縮のため）
  - Public LB: **0.81060**（ベースライン: 0.80079、**+0.00981**）
- **評価**: ベースラインを上回る性能を達成。深層学習モデル（BERT）の効果が確認できた。短期目標（Public LB 0.82-0.84）には届かなかったが、明確な改善が見られた。
- **実行環境**: Google Colab（GPU: Tesla T4）
- **関連タスク**: [[task-20260114141258|task_disaster_tweets_bert_discussion_20260114141258]]

## 改善案の概要

### 優先順位（短期）

1. **keyword特徴量の追加**（最も効果が期待できる）
   - EDAでkeywordとtargetの相関が非常に強いことが確認されている
   - 期待効果: CV F1 +0.01-0.04程度

2. **ハイパーパラメータチューニング**（LogisticRegressionのC値調整）
   - 期待効果: CV F1 +0.01-0.02程度

3. **閾値調整**（簡単に実装できる）
   - 期待効果: CV F1 +0.01-0.02程度

### 優先順位（中期）

4. **XGBoost/LightGBMの導入**（非線形モデル）
   - 期待効果: CV F1 0.80-0.85程度

5. **前処理の効果確認実験**（比較実験）

6. **特徴量の組み合わせ**（text + keyword）

### 優先順位（長期）

7. **深層学習モデル**（BERT、LSTMなど）
   - 期待効果: CV F1 0.85-0.90程度

8. **アンサンブル**（複数モデルの組み合わせ）

## 実装方針

- ベースライン実験の管理方法を継承
- 実験IDはタイムスタンプ形式（`exp[timestamp]_[description]`）
- すべての実験で`random_state=42`を統一
- 各改善案は個別の実験として実装
- 実験結果は親プロジェクトノートにも記録

## 注意点

1. **過学習への注意**: Train F1とCV F1の差が大きいため、正則化を強化する必要がある可能性
2. **Public LB > CV**: testデータの分布が異なる可能性があるため、CVスコアだけで判断しない
3. **計算リソース**: 深層学習モデルは時間とリソースが必要
4. **再現性**: すべての実験で`random_state=42`を統一

## 関連ノート（情報ハブ）

- [[disaster_tweets_baseline_improvement_ideas_20260112162435|ベースラインからの改善案（詳細）]]
- [[project_kaggle_disaster_tweets|親プロジェクト: kaggle_disaster_tweets]]
- [[exp20260106030720_report|ベースライン実験レポート]]
- [[exp20260112174906_report|keyword特徴量追加実験レポート]]
- [[exp20260112201310_report|C値チューニング実験レポート]]
- [[disaster_tweets_eda_20260105180000|EDA結果]]

<!-- AUTO:tasks:start -->
## タスク一覧（AUTO）

### active
- [[task_disaster_tweets_keyword_feature_20260112173705|task-20260112173705: Disaster Tweets: keyword特徴量の追加実験]]
- [[task_disaster_tweets_lr_c_tuning_20260112182239|task-20260112182239: Disaster Tweets: LogisticRegressionのC値チューニング]]
<!-- AUTO:tasks:end -->

