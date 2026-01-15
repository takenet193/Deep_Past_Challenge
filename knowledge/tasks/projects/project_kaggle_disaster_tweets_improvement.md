---
type: project
id: project-kaggle_disaster_tweets_improvement
title: Kaggle Disaster Tweets - 改善実装プロジェクト
project: kaggle_disaster_tweets_improvement
created: 2026-01-12
updated: 2026-01-12
tags:
  - project
  - kaggle
  - kaggle_disaster_tweets
  - improvement
links:
  - disaster_tweets_baseline_improvement_ideas_20260112162435
  - project_kaggle_disaster_tweets
  - exp20260106030720_report
---

# Project: kaggle_disaster_tweets_improvement

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
- [[disaster_tweets_eda_20260105180000|EDA結果]]

<!-- AUTO:tasks:start -->
<!-- AUTO:tasks:end -->




