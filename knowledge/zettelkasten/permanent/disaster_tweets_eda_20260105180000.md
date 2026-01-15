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

#kaggle_disaster_tweets

## 内容

Disaster Tweetsコンペの探索的データ分析（EDA）結果。ベースライン設計の意思決定に必要な要点をまとめる。

## 基本統計

- **train**: 7613行、5列（`id, keyword, location, text, target`）
- **test**: 3263行、4列（`id, keyword, location, text`）
- **train/test重複（id）**: 0件（重複なし）

## 欠損値

- **keyword**: trainで61件（0.8%）、testで26件（0.8%）→ 欠損は少ない
- **location**: trainで2533件（33.3%）、testで1105件（33.9%）→ **欠損が多い**
- **text**: 欠損なし（全件で利用可能）
- **target**: 欠損なし

## target分布

- **0（非災害）**: 4342件（57.0%）
- **1（災害）**: 3271件（43.0%）
- **評価**: 軽度の不均衡だが、StratifiedKFoldで対応可能

## テキストの特徴

### 文字数分布

- **train**: 平均101文字、中央値107文字、最小7文字、最大157文字
- **test**: 平均102文字、中央値109文字、最小5文字、最大151文字
- **評価**: train/testで分布がほぼ同じ。ツイートなので短い（最大157文字）

### URL/メンション/ハッシュタグ

- **URL含む**: 3971件（52.2%）→ 約半数にURLあり
- **メンション含む**: 2009件（26.4%）
- **ハッシュタグ含む**: 1743件（22.9%）

### 典型例

**災害（target=1）の例**:
- "Our Deeds are the Reason of this #earthquake May ALLAH Forgive us all"
- "Forest fire near La Ronge Sask. Canada"
- "All residents asked to 'shelter in place' are being notified by officers..."

**非災害（target=0）の例**:
- "What's up man?"
- "I love fruits"
- "Summer is lovely"

## keyword分析

- **ユニーク数**: 221種類
- **欠損**: 61件（0.8%）
- **頻度上位**: fatalities(45), deluge(42), armageddon(42), sinking(41), damage(41) など
- **targetとの相関**: **非常に強い**
  - 例: `debris`=100%災害、`wreckage`=100%災害、`derailment`=100%災害
  - `outbreak`=97.5%災害、`oil%20spill`=97.4%災害、`typhoon`=97.4%災害
- **評価**: keywordは強いシグナルだが、ベースラインでは`text`のみでまず試す（改善時に追加検討）

## location分析

- **欠損**: trainで33.3%、testで33.9%と多い
- **ユニーク数**: trainで3341、testで1602（自由記述でノイズが多い可能性）
- **評価**: **ベースラインでは使わない方針**（欠損が多く、ノイズが多いため）

## ベースライン方針の決定

### 使用する特徴量
- **text**: 使用（主特徴量）
- **keyword**: ベースラインでは使わない（改善時に検討）
- **location**: 使わない（欠損33%と多いため）

### 前処理
- lowercase: 実施
- URL除去: 検討（52%にURLあり、除去の効果を確認）
- メンション/ハッシュタグ除去: 検討（ただしハッシュタグは意味を持つ可能性あり）

### 特徴量エンジニアリング
- **TF-IDF**: 使用
  - ngram_range: `(1, 2)`（テキストが短いため、1-3gramは過剰かも）
  - max_features: 初期値20000（調整可能）

### モデル
- **LogisticRegression**: 採用（`predict_proba`で閾値調整しやすいため）

### CV戦略
- **StratifiedKFold**: 採用（クラス比が軽度不均衡のため）
- **n_splits**: 5
- **seed**: 42（再現性のため固定）

## 学び

- keywordは強いシグナルだが、まずは`text`のみでベースラインを構築し、改善時にkeywordを追加する方針が良い
- locationは欠損が多くノイズが多いため、ベースラインでは使わない
- テキストが短い（平均100文字）ため、TF-IDFのngram範囲は1-2gramが適切
- URL/メンション/ハッシュタグの除去は効果を確認しながら判断

## 関連ノート

- [[project_kaggle_disaster_tweets|プロジェクト: Disaster Tweets]]





