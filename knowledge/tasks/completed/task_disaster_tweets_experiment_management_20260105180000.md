---
type: task
id: task-20260105180000
title: "Disaster Tweets: 実験管理方法を確定する"
author: takeikumi
status: completed
completed_date: 2026-01-05
priority: high
project: kaggle_disaster_tweets
mode: setup
context:
  - project_kaggle_disaster_tweets
  - disaster_tweets_eda_20260105180000
dependencies:
  - task-20260105170000
related_notes:
  - project_kaggle_disaster_tweets
  - disaster_tweets_eda_20260105180000
created: 2026-01-05
updated: 2026-01-05
tags: [kaggle, kaggle_disaster_tweets, experiment, management]
---

# タスク: Disaster Tweets: 実験管理方法を確定する

#kaggle_disaster_tweets

## 目的
- 最初のモデル実装前に、実験コード・結果・ログの管理方法を確定し、再現性と追跡可能性を確保する
- プロジェクトノートに「実験データ管理」の運用方針をSSOTとして明記する

## 成果物（このタスクの完了条件）
- プロジェクトノート `project_kaggle_disaster_tweets.md` の `## 実験データ管理` に、確定した運用方針が追記されている
- 最初の実験（ベースライン）で使うディレクトリ構造・命名規則・保存形式が決まっている

## 実施計画（チェックリスト）

### ディレクトリ構造・命名規則
- [x] 実験コードの置き場を確定（`experiments/` の使い方）
  - ✅ 決定: **タイムスタンプ式** - `exp20260105180000_baseline_tfidf_lr/` のような形式
  - 理由: 二人で作業するため、番号（exp001）だと衝突する可能性がある
  - 形式: `expYYYYMMDDHHMMSS_[description]/`（例: `exp20260105180000_baseline_tfidf_lr/`）
  - **重要**: 同じディレクトリ内の全てのファイルに同じタイムスタンプを付与
    - 例: `exp20260105180000_config.yaml`, `exp20260105180000_train.py`, `exp20260105180000_README.md`
  - `config.yaml` の `experiment.id` も同じタイムスタンプを使用
- [x] 結果の置き場を確定（`results/` の使い方）
  - ✅ 決定: **分離型** - `experiments/exp20260105180000_baseline_tfidf_lr/` に実験コード、`results/exp20260105180000_baseline_tfidf_lr/` に結果を分離
  - 利点: 実験コードと結果を明確に分離できる、結果だけを一括管理しやすい
  - 構造: `experiments/exp[timestamp]_[description]/` (コード) / `results/exp[timestamp]_[description]/` (結果)
- [x] モデルファイルの保存方針（`models/` を使うか、実験ディレクトリ内か）
  - ✅ 決定: **`results/exp[timestamp]_[description]/` に保存**（結果の一部として）
  - 利点: 実験ごとに結果とモデルがまとまる、分離型の方針と整合、`config.yaml` の `output.results_dir` と整合
  - 構造: `results/exp20260105180000_baseline_tfidf_lr/exp20260105180000_model.pkl` など
  - **重要**: resultsディレクトリ内の全てのファイルにも実験IDを付与
    - 例: `exp20260105180000_metrics.json`, `exp20260105180000_submission.csv`, `exp20260105180000_model.pkl`
- [x] **前処理済みデータの整理方針（重要）**
  - ✅ 決定: `data/processed/` の下は**前処理パイプラインごと**に整理
  - 命名規則: `text_only_basic/`, `text_only_no_url/`, `text_keyword/` など、前処理内容を反映
  - 利点: 複数の実験で同じ前処理データを共有しやすい、前処理の違いが分かりやすい
  - `config.yaml` で `train_path: "data/processed/text_only_basic/train.csv"` のように指定

### 設定ファイル・ログ
- [x] `config.yaml` の使い方を確定（`experiments/_template_experiment/config.yaml` をベースに）
  - ✅ 決定: テンプレートをコピーし、実験ID（タイムスタンプ）と設定を編集
  - ✅ リポジトリルート基準の相対パスを使用
  - ✅ EDAで決めたベースライン方針を反映した初期configを作る
- [x] 実行ログの保存形式（`.log` ファイル / `metrics.json` / 両方）
  - ✅ 決定: `metrics.json`（評価指標）、`cv_results.json`（各フォールド詳細）、`.log`（オプション、Git除外）
- [x] seed固定の運用（全実験で `random_state=42` を統一するか）
  - ✅ 決定: 全実験で `random_state=42` を統一（再現性のため）

### 実験ノートとの連携
- [x] 各実験のREADME（`experiments/exp[timestamp]_[description]/README.md`）に何を書くか
  - ✅ 決定: `experiments/_template_experiment/README.md` テンプレートを使用
  - ✅ 必須項目: 実験ID、実施日、目的、仮説、実装内容、ハイパーパラメータ、結果、学んだこと、次のステップ
- [x] 実験結果をzettelkasten/permanentノートにどう反映するか（form: report を使うか）
  - ✅ 決定: `form: report` を使用（既にEDAで使用済み）
- [x] プロジェクトノートの「ベースライン実験ログ」にどうリンクするか
  - ✅ 決定: 各実験のREADMEへのリンクを追記

### Git管理方針
- [x] 実験コードはGitに載せるか（推奨: 載せる）
  - ✅ 決定: コミットする（`.py`, `config.yaml`, `README.md`）
- [x] 結果ファイル（`submission.csv`, `metrics.json` など）はGitに載せるか
  - ✅ 決定: 軽量なもの（`metrics.json`, `submission.csv`）はコミットする
- [x] モデルファイル（`.pkl` など）はGitに載せるか（推奨: 載せない、`.gitignore` で除外）
  - ✅ 決定: コミットしない（`.gitignore` で除外）

## 参考資料
- `experiments/_template_experiment/config.yaml`（実験設定テンプレート）
- `experiments/_template_experiment/README.md`（実験READMEテンプレート）
- `docs/project_architecture.md`（大枠の設計）
- `knowledge/zettelkasten/permanent/disaster_tweets_eda_20260105180000.md`（EDA結果、ベースライン方針）

## 結果（実施報告）
- 実験管理方法を確定し、Developer実験運用ルール（`.cursor/developer_experiment_rules.mdc`）を作成
- ディレクトリ構造・命名規則・設定ファイル・ログ・Git管理方針・実験ノートとの連携を全て決定
- プロジェクトノート `project_kaggle_disaster_tweets.md` の「実験データ管理」セクションに運用方針を追記
- テンプレート（`config.yaml`, `README.md`）をタイムスタンプ形式に更新

## 学び
- 二人で作業する場合、タイムスタンプ形式の実験IDが衝突回避に有効
- 全ファイルに実験IDを付与することで、ファイル名から実験の所属が明確になる
- Developer実験運用ルールを明文化することで、一貫性のある実験管理が可能になる

<!-- AUTO:project:start -->
- [[project_kaggle_disaster_tweets|project: kaggle_disaster_tweets]]
<!-- AUTO:project:end -->


