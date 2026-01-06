---
type: task
id: task-20260105121000
title: "Disaster Tweets: コンペ内容（ルール/評価基準/提出形式）を調べて確定する"
author: takeikumi
status: completed
completed_date: 2026-01-05
priority: high
project: kaggle_disaster_tweets
mode: review
context:
  - project_kaggle_disaster_tweets
dependencies: []
related_notes:
  - project_kaggle_disaster_tweets
created: 2026-01-05
updated: 2026-01-05
tags: [kaggle, kaggle_disaster_tweets]
---

# タスク: Disaster Tweets: コンペ内容（ルール/評価基準/提出形式）を調べて確定する

#kaggle_disaster_tweets

## 目的
- ベースライン実装の前提（ルール/評価指標/提出形式）を確定し、プロジェクトノートをSSOTとして埋める

## 手順
- [ ] コンペページの **Rules** を読み、重要点をプロジェクトノートに箇条書きで整理
- [ ] **評価指標**（指標名・最適化方向・注意点）をプロジェクトノートに明記
- [ ] **提出形式**（`submission.csv` の列名/行数/ID列/サンプル提出）をプロジェクトノートに明記

## メモ（公式ページから抜粋）
- Description要点:
  - NLP入門向けの “Getting Started” コンペ
  - 目的: ツイートが実災害に関するものかどうかを分類
  - データ: 手分類されたツイート約10,000件
  - 注意: 不適切な表現を含む可能性あり（Profane/Vulgar/Offensive）
- Competition Rules要点:
  - 1人1アカウント
  - チーム外への私的共有は禁止（公開共有は可）
  - チーム最大10人 / チームマージ可（条件あり）
  - 提出: 1日10回まで / 最終提出2件まで
  - Hand-labelingは禁止 / AutoMLは条件付きで可
- Evaluation:
  - 指標: F1（高いほど良い）
- Submission File:
  - `submission.csv`（列: `id`, `target`）
  - `target`: 実災害=1 / 非災害=0

## 結果
- プロジェクトノートに以下をSSOTとして反映した:
  - ルール（要点）
  - 評価指標（F1）
  - 提出形式（`submission.csv`: `id,target` / `target` は 0/1）

## 学び
- 評価指標と提出形式が確定すると、ベースライン実装の判断が速くなる

<!-- AUTO:project:start -->
- [[project_kaggle_disaster_tweets|project: kaggle_disaster_tweets]]
<!-- AUTO:project:end -->


