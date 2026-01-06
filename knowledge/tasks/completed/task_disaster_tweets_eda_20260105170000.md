---
type: task
id: task-20260105170000
title: "Disaster Tweets: EDA（データ概観とベースライン設計の当たりを付ける）"
author: takeikumi
status: completed
completed_date: 2026-01-05
priority: high
project: kaggle_disaster_tweets
mode: experiment
context:
  - project_kaggle_disaster_tweets
dependencies: []
related_notes:
  - project_kaggle_disaster_tweets
created: 2026-01-05
updated: 2026-01-05
tags: [kaggle, kaggle_disaster_tweets, eda]
---

# タスク: Disaster Tweets: EDA（データ概観とベースライン設計の当たりを付ける）

#kaggle_disaster_tweets

## 目的
- `train.csv` / `test.csv` の性質（欠損・分布・偏り・ノイズ）を把握し、最初のベースライン（TF-IDF+線形モデル）の設計方針を決める
- 以降の改善で迷わないよう、観測結果をプロジェクトノートにSSOTとして残す

## 成果物（このタスクの完了条件）
- プロジェクトノート `project_kaggle_disaster_tweets.md` の `## データ` / `## ベースライン` に、EDAで分かった「意思決定に必要な要点」が追記されている

## 実施計画（チェックリスト）

### 基本統計
- [ ] train/test件数、重複の有無（`id` など）
- [ ] 欠損率（`keyword` / `location` / `text`）
  - 確認済み: `keyword` は少ない（約0.8%）、`location` は多い（約33%）、`text` は欠損なし
- [ ] `target` のクラス比（0/1）
  - 確認済み: 0が57% / 1が43%（軽度の不均衡、StratifiedKFoldで対応可能）

### テキストの特徴
- [ ] 文字数/単語数の分布（train vs test）
  - 確認済み: 平均約100文字、最大157文字（ツイートなので短い）
- [ ] URL/メンション/ハッシュタグの頻度
- [ ] 典型例（短い/長い/ノイズが強い）を数件サンプリング
- [ ] テキスト長が短いため、**ngram範囲（1-2gram vs 1-3gram）の妥当性**を検討

### keyword/location の扱い判断（重要）
- [ ] `keyword` の種類数・頻度上位
  - 確認済み: 221種類、targetとの相関が強い（例: debris=100%災害、wreckage=100%災害）
- [ ] **keywordをベースラインで使うか判断**（使う場合: カテゴリ特徴量として追加）
- [ ] `location` のノイズ感（自由記述/欠損多い等）を確認
  - 確認済み: 欠損33%と多い → **ベースラインでは使わない方針**を推奨
- [ ] ベースラインでは「使う/使わない」を決め、その理由をメモ

### 分割方針（CV）
- [ ] StratifiedKFold が妥当か（クラス比・リーク懸念）
  - 確認済み: クラス比は軽度不均衡なのでStratifiedKFoldでOK
- [ ] seed固定（例: 42）を採用するか

### ベースライン方針を確定
- [ ] 前処理（最小）: lowercase, URL/mention除去の要否を決める
- [ ] 特徴量: TF-IDF（ngram範囲、max_featuresの初期値）
  - テキストが短いので、**1-2gramが適切か検討**（1-3gramは過剰かも）
- [ ] モデル: LogisticRegression or LinearSVC（どちらから入るか）
  - 推奨: LogisticRegression（`predict_proba`で閾値調整しやすい）

## メモ（事前確認済みの基本情報）
- train: 7613行、test: 3263行
- target分布: 0が4342件(57%)、1が3271件(43%) → 軽度の不均衡
- 欠損: `keyword` 約0.8%、`location` 約33%、`text` なし
- テキスト長: 平均約100文字、最大157文字（ツイートなので短い）
- keyword: 221種類、targetとの相関が強い（例: debris=100%災害、wreckage=100%災害）
- location: 欠損33%と多い → ベースラインでは使わない方針を推奨

## 結果（実施報告）
- 基本統計・欠損・分布・keyword/location分析を実施
- keywordはtargetと相関が強い（221種類、例: debris=100%災害）が、ベースラインでは`text`のみでまず試す方針を決定
- locationは欠損33%と多いため、ベースラインでは使わない方針を決定
- テキストは平均100文字と短いため、TF-IDFは1-2gramを採用
- ベースライン方針を確定: `text`のみ + TF-IDF(1-2gram, max_features=20000) + LogisticRegression + StratifiedKFold(n_splits=5, seed=42)
- EDA詳細ノート: `knowledge/zettelkasten/permanent/disaster_tweets_eda_20260105180000.md` に結果をまとめた

## 学び
- keywordは強いシグナルだが、ベースラインではtextのみでまず試す（改善時に追加検討）
- locationは欠損が多くノイズが多いため、ベースラインでは使わない
- テキストが短い（平均100文字）ため、TF-IDFのngram範囲は1-2gramが適切

<!-- AUTO:project:start -->
- [[project_kaggle_disaster_tweets|project: kaggle_disaster_tweets]]
<!-- AUTO:project:end -->


