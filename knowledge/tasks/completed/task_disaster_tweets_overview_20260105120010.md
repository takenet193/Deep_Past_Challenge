---
type: task
id: task-20260105120010
title: "Disaster Tweets: データをダウンロードして配置を確定する"
author: takeikumi
status: completed
completed_date: 2026-01-05
priority: high
project: kaggle_disaster_tweets
mode: setup
context:
  - project_kaggle_disaster_tweets
dependencies: []
related_notes:
  - project_kaggle_disaster_tweets
created: 2026-01-05
updated: 2026-01-05
tags: [kaggle, kaggle_disaster_tweets, data]
---

# タスク: Disaster Tweets: データをダウンロードして配置を確定する

#kaggle_disaster_tweets

## 目的
- Kaggleからデータを入手し、ローカルの配置方針（どこに置く/どう参照する）を確定する

## 手順
- [x] Kaggleから `train.csv` / `test.csv` をダウンロード
  - 方法A（推奨: Kaggle CLI）:
    - `pip install kaggle`（未導入なら）
    - `~/.kaggle/kaggle.json` を配置（KaggleのAccount設定からAPI Token発行）
    - `kaggle competitions download -c nlp-getting-started -p data/raw -f train.csv`
    - `kaggle competitions download -c nlp-getting-started -p data/raw -f test.csv`
    - `unzip -o data/raw/train.csv.zip -d data/raw`（zipで落ちた場合）
    - `unzip -o data/raw/test.csv.zip -d data/raw`
    - （今回の実施）`kaggle competitions download -c nlp-getting-started -p data/raw` でzip一括DL → `unzip ...` で展開
  - 方法B（手動DL）:
    - KaggleのDataタブから `train.csv` / `test.csv` をDLして `data/raw/` へ配置
- [x] データ配置を確定（このリポジトリの方針）
  - `data/raw/train.csv`
  - `data/raw/test.csv`
  - 注: `data/raw/*` は `.gitignore` 済み（データはGitに載せない）
- [x] 置いたファイルを軽く確認
  - `ls -lh data/raw/` で存在確認
  - `head -n 3 data/raw/train.csv` / `head -n 3 data/raw/test.csv` で列を確認
- [x] `train.csv` / `test.csv` の **列・target定義** をプロジェクトノートに追記

## 結果
- `data/raw/` に以下を配置した
  - `train.csv`, `test.csv`, `sample_submission.csv`
- 列を確認した
  - `train.csv`: `id, keyword, location, text, target`
  - `test.csv`: `id, keyword, location, text`

## 学び
- （完了後に記入）

<!-- AUTO:project:start -->
- [[project_kaggle_disaster_tweets|project: kaggle_disaster_tweets]]
<!-- AUTO:project:end -->


