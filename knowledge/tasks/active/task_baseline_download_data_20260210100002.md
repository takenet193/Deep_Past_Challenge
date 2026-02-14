---
type: task
id: task-20260210100002
title: データをダウンロードする
author: takeikumi
status: completed
priority: high
project: baseline
mode: setup
due_date: null
context: []
tags:
  - baseline
  - kaggle
  - data
related_notes: []
assignee: null
assigned_agent: null
dependencies:
  - task-20260210100001
created: 2026-02-10
updated: 2026-02-10
---

# タスク: データをダウンロードする

## 目的

コンペで必要なデータをダウンロードし、ローカル環境で利用できる状態にする。

## 手順

- [x] Kaggle API からデータをダウンロードする
- [x] データの配置先を決め、ディレクトリ構造を整える（`data/raw`）
- [x] データの内容を軽く確認する（カラム構成とファイル一覧を確認。詳細なEDAは別タスクで実施予定）

## 結果（実施報告）/ 学び / 次のアクション

- **結果**:
    - Kaggle アカウントで API Token を発行し、PowerShell セッション内の `KAGGLE_API_TOKEN` 環境変数として設定して利用した。
    - `kaggle` CLI をインストールし、`kaggle competitions download -c deep-past-initiative-machine-translation -p "data/raw"` でコンペデータ ZIP をダウンロードした。
    - `C:\Users\ND003\OneDrive\Desktop\Deep_Past_Challenge\data\raw\deep-past-initiative-machine-translation.zip` を `Expand-Archive` で展開し、`train.csv`, `test.csv`, `sample_submission.csv` などが `data/raw` に配置された。
    - 本リポジトリにおける Deep Past 生データの配置先を `data/raw` として整理した。
- **学び**:
    - Kaggle API Token は環境変数 `KAGGLE_API_TOKEN` として一時的に設定しても利用できる（PowerShell セッションを閉じるとクリアされる）。
    - Kaggle CLI の `-p` オプションで、プロジェクト内の任意のディレクトリに直接ダウンロードできるため、最初にディレクトリ構造を決めておくと後片付けが楽になる。
- **次のアクション**:
    - `data/raw/train.csv` / `test.csv` / `sample_submission.csv` のカラム構成とレコード数を確認し、別タスク（ベースライン実装）で使う前提条件を整理する。

> 注: タスク完了時（`status: completed`に変更時）は、必ずこのセクションに実施報告を記載してください。

<!-- AUTO:project:start -->
- [[project_baseline|project: baseline]]
<!-- AUTO:project:end -->
