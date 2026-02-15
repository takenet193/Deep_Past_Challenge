---
type: task
id: task-20260210100003
title: ベースラインを作成する
author: takeikumi
status: active
priority: high
project: baseline
mode: implementation
due_date: null
context: []
tags:
  - baseline
  - kaggle
  - machine-translation
related_notes:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
assignee: null
assigned_agent: null
dependencies:
  - task-20260210100002
created: 2026-02-10
updated: 2026-02-10
---

# タスク: ベースラインを作成する

**対象**: Developer エージェントがこのタスクを読み、実装する。  
**準拠**: 実験・成果物の形式は必ず `.cursor/developer_experiment_rules.mdc` に従う。

---

## 1. 目的と成果物

- **目的**: 機械翻訳のベースラインを実装し、コンペに提出できる状態にする。
- **成果物**:
  - 本番推論のみの Kaggle 用ノート 1 本（EDA・Optuna を含まない）
  - 実験ディレクトリ `experiments/exp[timestamp]_byt5_baseline_inference/`（ノート・config・report）
  - 結果ディレクトリ `results/exp[timestamp]_byt5_baseline_inference/`（submission.csv 等）

---

## 2. 実装前に読むドキュメント

| 順 | ドキュメント | 用途 |
|----|--------------|------|
| 1 | `.cursor/developer_experiment_rules.mdc` | 実験ID・experiments/results の分離・ファイル名ルール・config の扱い |
| 2 | `knowledge/zettelkasten/references/harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000.md` | 処理の全体像・コードノートへのリンク |
| 3 | コードノート（上記リファレンス内のリンク先） | 処理 1〜8 のコードの写し元。パス: `knowledge/zettelkasten/references/`。ファイル名: `harukiharada_metrics_fallback_code_20260213000002.md`, `harukiharada_preprocessor_postprocessor_code_20260213000000.md`, `harukiharada_model_load_code_20260213000004.md`, `harukiharada_dataset_sampler_code_20260213000005.md`, `harukiharada_inference_chunked_beam_search_code_20260213000007.md`, `harukiharada_submission_code_20260213000008.md` |

依存: `requirements-baseline.txt`（torch, transformers, optuna, sacrebleu, sentencepiece 等）。環境変数は metrics_fallback のコードノートに従う。

---

## 3. 前提条件・制約

- **含める処理**: データ読込 → 前処理・チャンキング・後処理（chunky_v1_5_0）→ モデル読込 → AkkadianDataset・BucketBatchSampler → 本番推論 Phase1/2（固定パラメータ）→ submission.csv 作成。
- **含めない処理**: EDA（可視化・分析）、Optuna の探索。
- **固定パラメータ**: length_penalty=1.5, num_beams=8。データは train.csv / test.csv を文書単位のまま使用（Sentences 文単位分割は使わない）。
- **設定の二重管理**: Kaggle ノートは experiments/ の config を読めない。そのため (A) ノート内に「設定セル」を 1 つ置き、パス・パラメータを変数で定義する。(B) 同じ内容を `experiments/exp[timestamp]_byt5_baseline_inference/exp[timestamp]_config.yaml` に記録用として写す。ノートは (A) のみ参照する。
- **ディレクトリ**: `scripts/kaggle_notebooks/` が存在しなければ、実装の最初に作成する。

---

## 4. 実装手順（実行順）

### Step 1: 作業ディレクトリの準備

- `scripts/kaggle_notebooks/` が存在するか確認する。存在しなければ作成する（例: `mkdir -p scripts/kaggle_notebooks`）。

### Step 2: 本番推論用ノートの作成

- **配置先**: `scripts/kaggle_notebooks/` に、本番推論のみを行う 1 本のノート（.ipynb）を用意する。
- **作成方法のどちらか**:
  - (A) リファレンスのコードノートから、処理 1〜8 のコードを順にコピーし、1 本のノートのセルとして並べる。
  - (B) `kaggle kernels pull harukiharada/byt5-optuna-tuning-chunked-beam-search -p scripts/kaggle_notebooks/` で取得した .ipynb を開き、EDA・Optuna に相当するセルを削除し、本番推論のみ残す。
- **ノートの先頭に「設定」セルを 1 つ置く**。以下を変数で定義する（Kaggle 実行用。ノートはこのセルのみ参照し、外部 config は読まない）。

```python
COMPETITION_DIR = "/kaggle/input/deep-past-initiative-machine-translation"
MODEL_PATH = "/kaggle/input/final-byt5/byt5-akkadian-optimized-34x"
TRAIN_CSV = f"{COMPETITION_DIR}/train.csv"
TEST_CSV = f"{COMPETITION_DIR}/test.csv"
FIXED_LENGTH_PENALTY = 1.5
FIXED_NUM_BEAMS = 8
BATCH_SIZE = 8
MAX_LENGTH = 512
```

- リファレンスに記載の CHUNK_THRESHOLD 等も、必要に応じて同じセルに定義する。
- **処理 1〜8 の対応**: 下表の順でセルを並べる。各セルのコードは、対応するコードノートのコードブロックから取得する。変数・インポートの受け渡し（例: `preprocessor`, `tokenizer`, `model`, `df_test`）が前のセルで定義されている前提で繋がるよう、並べたあとで通し実行して確認する。

| 順 | 処理内容 | 参照コードノート（ファイル名） |
|----|----------|--------------------------------|
| 1 | 環境変数・インポート・評価指標（sacrebleu フォールバック） | harukiharada_metrics_fallback_code_20260213000002.md |
| 2 | 前処理・節境界チャンキング・後処理（chunky_v1_5_0） | harukiharada_preprocessor_postprocessor_code_20260213000000.md |
| 3 | モデル・トークナイザ読込（BetterTransformer は任意） | harukiharada_model_load_code_20260213000004.md |
| 4 | AkkadianDataset・BucketBatchSampler | harukiharada_dataset_sampler_code_20260213000005.md |
| 5 | 本番推論設定（test_dataset, collate_fn） | harukiharada_inference_chunked_beam_search_code_20260213000007.md |
| 6 | Phase 1: 長文のチャンク翻訳 | 同上 |
| 7 | Phase 2: 短い文のバッチ翻訳（adaptive beams） | 同上 |
| 8 | submission.csv の組み立て・検証・保存 | harukiharada_submission_code_20260213000008.md |

### Step 3: 実験IDの発行と実験ディレクトリの作成

- `.cursor/developer_experiment_rules.mdc` に従い、実験ID を `expYYYYMMDDHHMMSS` 形式で発行する（例: 実験開始時の現在時刻）。
- 次の 2 つを作成する:
  - `experiments/exp[timestamp]_byt5_baseline_inference/`
  - `results/exp[timestamp]_byt5_baseline_inference/`
- 以下を配置する:
  - `scripts/kaggle_notebooks/` に用意したノートを、**実験ID付きファイル名**で `experiments/exp[timestamp]_byt5_baseline_inference/` にコピーする。例: `exp20260215120000_inference.ipynb`。
  - `experiments/exp[timestamp]_byt5_baseline_inference/exp[timestamp]_config.yaml` を作成する。中身は「記録用」として、ノートの設定セルと同じ値を YAML で書く（ノートはこのファイルを読まない）。最低限のキーは以下とする。

```yaml
experiment:
  id: "expYYYYMMDDHHMMSS"
  name: "byt5_baseline_inference"
  created_at: "YYYY-MM-DDTHH:MM:SS"
inference:
  model_path: "/kaggle/input/final-byt5/byt5-akkadian-optimized-34x"
  competition_dir: "/kaggle/input/deep-past-initiative-machine-translation"
  length_penalty: 1.5
  num_beams: 8
  batch_size: 8
  max_length: 512
```

- `experiments/exp[timestamp]_byt5_baseline_inference/exp[timestamp]_report.md` を作成する。テンプレートは `experiments/_template_experiment/README.md` をコピーしてリネームしてもよい。実施前は空または仮でよい。

### Step 4: Kaggle での実行（手順）

- ノートを Kaggle にアップロードするか、harukiharada のノートを Fork して本番推論のみの形に編集する。
- Add Data で次を追加する: コンペ「Deep Past Initiative Machine Translation」、ByT5 モデル（Kaggle で「final-byt5」または byt5-akkadian-optimized で検索。モデルは `byt5-akkadian-optimized-34x` 等のサブディレクトリ。パスは `/kaggle/input/final-byt5/byt5-akkadian-optimized-34x` に合わせる）。
- ノート内のパスが上記と一致するか確認する。
- GPU をオンにして Run All する。本番 test は約 4,000 件のため、推論のみでおおよそ 2 時間前後を想定する。
- `/kaggle/working/submission.csv` をコンペに提出する。

### Step 5: 結果の保存と記録

- Kaggle の Output から `submission.csv` をダウンロードし、`results/exp[timestamp]_byt5_baseline_inference/exp[timestamp]_submission.csv` として保存する。
- `exp[timestamp]_config.yaml` に、ノートで実際に使ったパス・パラメータが反映されているか確認する。未記入なら写して記入する。
- `exp[timestamp]_report.md` に、実施内容・提出スコア（分かれば）を記録する。

---

## 5. 環境・データ・モデル（参照用）

- **依存**: `pip install -r requirements.txt -r requirements-baseline.txt`。環境変数は metrics_fallback のコードノートに従う（`OMP_NUM_THREADS`=4, `TOKENIZERS_PARALLELISM`=true 等）。
- **データ**: Kaggle では `/kaggle/input/deep-past-initiative-machine-translation/train.csv`, `test.csv`。本番 test は約 4,000 件。
- **モデル**: Kaggle では `/kaggle/input/final-byt5/byt5-akkadian-optimized-34x`。ローカルで検証する場合は `data/models/` を新規作成し、同構成で配置する。

---

## 6. 結果（実施報告）/ 学び / 次のアクション

- **結果**: （未実施）
- **学び**: （記入する）
- **次のアクション**: （記入する）

> 注: タスク完了時（`status: completed` に変更時）は、必ずこのセクションに実施報告を記載する。

<!-- AUTO:project:start -->
- [[project_baseline|project: baseline]]
<!-- AUTO:project:end -->
