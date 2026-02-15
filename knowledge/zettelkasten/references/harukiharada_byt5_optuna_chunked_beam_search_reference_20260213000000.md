---
id: 20260213000000
title: harukiharada - ByT5 + Optuna + Chunked Beam Search リファレンス
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - byt5
  - optuna
  - baseline
links:
  - byt5_overview_architecture_deeppast_20260214120000
  - harukiharada_preprocessor_postprocessor_code_20260213000000
  - harukiharada_metrics_fallback_code_20260213000002
  - harukiharada_eda_code_20260213000003
  - harukiharada_model_load_code_20260213000004
  - harukiharada_dataset_sampler_code_20260213000005
  - harukiharada_optuna_validation_scoring_code_20260213000006
  - harukiharada_inference_chunked_beam_search_code_20260213000007
  - harukiharada_submission_code_20260213000008
  - deep_past_competition_overview_20260210120000
  - akkadian_mt_preprocessing_ensemble_reference_20260211130000
  - deep_past_preprocessing_20260211130000
  - deep_past_eda_results_20260211140000
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - ByT5 + Optuna + Chunked Beam Search リファレンス

## 概要

Deep Past Challenge において **スコア 35.1、Bronze メダル** を獲得したノートブック。AnthonyTherrien のアンサンブルスクリプトをベースに ByT5 + Optuna ハイパーパラメータチューニング + Chunked Beam Search を組み合わせた実装。

- **URL**: https://www.kaggle.com/code/harukiharada/byt5-optuna-tuning-chunked-beam-search
- **スコア**: 35.1（幾何平均 GM）
- **メダル**: Bronze

---

## ノートブック内の説明（コンペ・データ・評価）

### コンペの焦点

The Deep Past Challenge は、約 4,000 年前（紀元前 1950–1750 年頃）の古アッシリア楔形文字テキストの機械翻訳に焦点を当てる。これらは古代都市カネシュ（現トルコ・キュルテペ）で発見された商取引記録であり、アッシリア商人間の商業活動を記録している。

### カラム定義

| Column | Description | Type | Notes |
|--------|-------------|------|-------|
| id | 各テキストの一意の識別子 | Integer | 提出時のマッチングに使用 |
| transliteration | 楔形文字のローマ字転写 | Text (Input) | 特殊文字（ḫ、下付き数字）、欠損マーカー（x, ...）、括弧注釈を含む |
| translation | テキストの英訳 | Text (Target) | train.csv のみ。予測対象 |

### 主要な課題

- **古代言語**: アッカド語（古アッシリア方言）— 母語話者が存在しない
- **損傷した粘土板**: 多くのテキストに粘土板の破損箇所を示す `x` や `...` でマークされた欠損がある
- **ドメイン固有語彙**: 青銅器時代の商業用語、固有名詞、地名
- **可変テキスト長**: 短い断片から長い複数節の契約まで

### 評価

提出物は BLEU と chrF++ の幾何平均でスコアリングされる:

- **BLEU**: 単語レベルの n-gram 重複を測定（精度寄り）
- **chrF++**: 文字レベルの F-score を測定（形態変化にロバスト）
- **Score** = sqrt(BLEU × chrF++): 両方のメトリクスが強くないと高スコアにならない

---

## 技術スタック

| 要素 | 内容 |
|------|------|
| ベースモデル | ByT5（byte-level, token-free） |
| ハイパーパラメータ | Optuna によるチューニング |
| デコーディング | Chunked Beam Search |
| 元ネタ | AnthonyTherrien のアンサンブルスクリプト |

## ByT5 の利点（このタスク向け）

> 詳細な解説（概要・アーキテクチャ・開発経緯・コンペ適合性）→ [[byt5_overview_architecture_deeppast_20260214120000|ByT5 概要・アーキテクチャ・開発経緯と Deep Past Challenge への適合性]]

- **バイトレベル**: トークナイザ不要で任意の言語・書記体系に対応
- **ノイズ耐性**: 古代テキストの欠損・書記記号・表記ゆれに強い
- **低リソース向き**: ファインチューニングデータが少ない場合でも mT5 より有利（論文: Are Character-level Translations Worth the Wait?）
- **特殊文字**: アッカド語の š, ṣ, ṭ, ḫ などサブワード分割の影響を受けにくい

## Chunked Beam Search の狙い

- 長文入力（文書単位では平均 57.5 語、95%ile 124 語）を扱うため
- モデルの最大入力長を超えるテキストをチャンクに分割し、チャンクごとにビームサーチ
- メモリ制約下での長文翻訳に対応

---

## 実装詳細：ライブラリ・インポート・評価指標

**完全コード** → [[harukiharada_metrics_fallback_code_20260213000002|harukiharada - ライブラリ・インポート・評価指標フォールバック 完全コード]]

### 環境変数

- `OMP_NUM_THREADS`, `MKL_NUM_THREADS`: 4
- `CUDA_LAUNCH_BLOCKING`: 0, `TORCH_CUDNN_V8_API_ENABLED`: 1
- `TOKENIZERS_PARALLELISM`: true（トークナイザの並列処理を有効化）

### 主要なインポート

| カテゴリ | ライブラリ |
|----------|------------|
| 基本 | `re`, `random`, `math`, `pathlib`, `typing`, `collections`, `dataclasses` |
| データ | `numpy`, `pandas` |
| 可視化 | `matplotlib`, `seaborn`（banner_palette で茶・金系のカラーパレット） |
| 深層学習 | `torch`, `torch.utils.data` (Dataset, DataLoader, Sampler), `torch.cuda.amp` (autocast) |
| モデル | `transformers`: `AutoTokenizer`, `AutoModelForSeq2SeqLM` |
| その他 | `tqdm.auto` |

### 評価指標：sacrebleu + 純 Python フォールバック

- **USE_SACREBLEU**: デフォルト `False`。sacrebleu が利用可能なら `True` に切り替え
- sacrebleu が無い場合、pip でインストールを試行
- それでも失敗した場合、**純 Python 実装**を使用

#### フォールバック関数

| 関数 | 役割 |
|------|------|
| `_corpus_bleu_fallback(hypotheses, references, max_n=4)` | コーパス BLEU（簡易版、平滑化なし、Brevity Penalty 付き） |
| `_chrf_pp_fallback(hypotheses, references, n_char=6, n_word=2, beta=2)` | chrF++（文字 n-gram + 単語 n-gram の F-score） |
| `_sentence_bleu_fallback(hypothesis, reference, max_n=4)` | 文レベル BLEU（add-1 smoothing 付き） |

※ Kaggle 本番（インターネットオフ）でも評価できるよう、sacrebleu 無しでの動作を想定した設計。

### Optuna

- インポート失敗時は `pip install optuna` を試行
- それでも失敗した場合は `ImportError` で停止（必須ライブラリ）

### 実行時の出力（動作確認済み）

Kaggle 本番環境（インターネットオフ）での実出力:

| 項目 | 結果 |
|------|------|
| sacrebleu | インストール失敗（DNS/ネットワークエラー）→ **純 Python フォールバックで動作** |
| optuna | ロード成功 |
| PyTorch | 2.8.0+cu126 |
| CUDA | 有効 |
| GPU | Tesla P100-PCIE-16GB（17.1 GB VRAM） |

- sacrebleu の pip インストールはネットワーク不可のため失敗するが、フォールバックにより **sacrebleu なしでも評価は実行可能**
- **GPU 16GB** で動作しているため、ByT5-base 程度であればローカル再現も同程度の VRAM で可能と推測

---

## 実装詳細：モデル読込

**完全コード** → [[harukiharada_model_load_code_20260213000004|harukiharada - モデル読込 完全コード]]

### 概要

- **MODEL_PATH**: `/kaggle/input/final-byt5/byt5-akkadian-optimized-34x`（Kaggle 入力にマウントした ByT5 アッカド語向けファインチューニング済みモデル）
- **読込**: `AutoTokenizer.from_pretrained(MODEL_PATH)` と `AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)` でトークナイザとモデルを同一パスからロード
- **デバイス**: `torch.cuda.is_available()` で CUDA を判定し、`model.to(device).eval()` で推論モードに
- **パラメータ数**: 全パラメータの `numel()` 合計を表示（ByT5-base 規模の確認用）
- **BetterTransformer**: `optimum.bettertransformer` で推論を最適化。利用不可の場合は `try/except` でスキップし処理継続

### 実出力（動作確認済み）

| 項目 | 結果 |
|------|------|
| パラメータ数 | 581,653,248（約 5.8 億、ByT5-base 規模） |
| デバイス | cuda |
| BetterTransformer | スキップ（`No module named 'optimum'`） |

- cuFFT / cuDNN / cuBLAS / computation placer の E/W メッセージは XLA まわりの重複登録警告で、動作には影響しない。無視してよい。
- 詳細なログ全文は [[harukiharada_model_load_code_20260213000004|モデル読込 完全コード]] の「実行時の出力」を参照。

### ローカル再現時

- Kaggle の `/kaggle/input/final-byt5/...` は、ローカルでは `data/models/byt5-akkadian-optimized-34x` 等にダウンロードしたパスに置き換える。pascalledesma のデータセットや自前ファインチューニング済みチェックポイントを指定可能。

---

## 実装詳細：Dataset と BucketBatchSampler

**完全コード** → [[harukiharada_dataset_sampler_code_20260213000005|harukiharada - Dataset と BucketBatchSampler 完全コード]]

### 概要

- **AkkadianDataset**: `transliteration` 列を持つ DataFrame と前処理オブジェクト（[[harukiharada_preprocessor_postprocessor_code_20260213000000|OptimizedPreprocessor]]）を受け、`preprocess_batch` で転写を正規化したうえで `'translate Akkadian to English: ' + t` を付与。`__getitem__` は `(sample_id, input_text)` を返す。
- **BucketBatchSampler**: 各サンプルのテキスト長（単語数）でソートし、`num_buckets` 個のバケットに分割。バケット内を `batch_size` ずつ yield し、長さの近いサンプルを同一バッチにまとめてパディングを削減。
- **利用**: `DataLoader(dataset, batch_sampler=BucketBatchSampler(dataset, batch_size=..., num_buckets=4))` のように組み合わせる。DataLoader には `batch_size` を渡さない。

---

## 実装詳細：Optuna 用検証分割と翻訳・スコア関数

**完全コード** → [[harukiharada_optuna_validation_scoring_code_20260213000006|harukiharada - Optuna チューニングと検証評価 完全コード]]

### 概要

- **検証分割**: `df_train` から `VAL_SIZE=100` 件を seed=42 で重複なしランダム抽出し `df_val` を作成。Optuna の試行ごとに「この 100 件を翻訳 → スコア」で目的関数を評価し、試行時間を抑える。
- **translate_batch_with_params(texts, length_penalty, num_beams, max_new_tokens=512)**: 転写リストを前処理・プレフィックス付与 → トークナイザでバッチ化（内部 batch_size=4, max_length=512）→ `model.generate`（num_beams, length_penalty, early_stopping, autocast）→ デコード後に後処理して返す。Optuna で `length_penalty` と `num_beams` を変えながら呼ぶ想定。
- **スコア関数**: `compute_bleu` / `compute_chrf` は USE_SACREBLEU に応じて sacrebleu または [[harukiharada_metrics_fallback_code_20260213000002|built-in フォールバック]] を使用。`compute_competition_score` は BLEU と chrF++ の幾何平均（0 以下は 0.0）を返し、コンペの公式スコアに合わせている。

### Optuna Study（目的関数・最適化・結果表示）

- **PROVEN_PARAMS**: 公開ノートで 35.1 を出した既知の良い組み合わせ 2 つ（length_penalty=1.5 & num_beams=8、1.3 & 8）。`study.enqueue_trial(params)` で最初の 2 試行として必ず評価する。
- **objective(trial)**: `length_penalty` を 0.8〜2.0、`num_beams` を 4〜12 でサジェスト。df_val を `translate_batch_with_params` で翻訳し、`compute_competition_score` を返す。
- **最適化**: `optuna.create_study(direction='maximize')` のあと enqueue した 2 試行 + `study.optimize(objective, n_trials=20, timeout=7200)` で最大 2 時間まで探索。
- **結果**: 最良スコア・最良パラメータを表示し、全試行をスコア降順で上位 10 件表示。PROVEN の試行は `[PROVEN BASELINE]` でタグ付け。完全コードは [[harukiharada_optuna_validation_scoring_code_20260213000006|Optuna チューニングと検証評価 完全コード]] の「Optuna Study」セクションを参照。

### 固定生成パラメータと検証評価

- **方針**: Optuna は分析・探索用とし、**test 推論では chunky_v1_5_0 実績の固定パラメータ**（FIXED_LENGTH_PENALTY=1.5, FIXED_NUM_BEAMS=8）を使う。
- **処理**: Optuna 最良と Proven を print で比較したあと、df_val を lp=1.5, beams=8 で `translate_batch_with_params` し、`compute_bleu` / `compute_chrf` で BLEU・chrF++・幾何平均を算出して表示。本番提出前の検証確認用。完全コードは上記ノートの「固定生成パラメータと検証評価」を参照。

### 本番推論の設定（FULL INFERENCE CONFIG）

- chunky_v1_5_0 準拠で **test 用**の推論設定を定義。BATCH_SIZE=8, MAX_LENGTH=512, NUM_WORKERS=4, NUM_BUCKETS=4。`test_dataset = AkkadianDataset(df_test, preprocessor)` で test を前処理・プレフィックス付与し、`collate_fn(batch)` で (ids, tokenized) を返す形にまとめる。後続の DataLoader と生成ループ（Chunked Beam Search 等）で使用。完全コードは [[harukiharada_inference_chunked_beam_search_code_20260213000007|本番推論・Chunked Beam Search 完全コード]] の「本番推論の設定」を参照。

### Chunked Beam Search Phase 1（長文のチャンキング翻訳）

- 単語数が **CHUNK_THRESHOLD 超**の test のみ、[[harukiharada_preprocessor_postprocessor_code_20260213000000|split_akkadian]] で節境界チャンクに分割。各チャンクに `gen_config_chunk`（num_beams, length_penalty, max_new_tokens=512 等）で `model.generate` を実行し、デコード結果を空白で結合してから後処理し、`(sample_id, cleaned)` を `results` に追加。`chunked_ids` に対象 idx を記録。短い文は Phase 2 で処理。完全コードは [[harukiharada_inference_chunked_beam_search_code_20260213000007|本番推論・Chunked Beam Search 完全コード]] の「PHASE 1」を参照。

### Chunked Beam Search Phase 2（短い文のバッチ翻訳）

- Phase 1 で処理しなかった**短い転写**（chunked_ids に含まれない idx）を対象に、DataLoader でバッチ化して翻訳。chunked_ids が空なら test_dataset 全体、そうでなければ Subset で短い文だけを [[harukiharada_dataset_sampler_code_20260213000005|BucketBatchSampler]]（サンプル数 ≥ NUM_BUCKETS のとき）または固定 batch_size の DataLoader で処理。**Adaptive beams**: バッチ内の入力トークン長が 100 未満なら num_beams=4（または best_num_beams//2）、100 以上なら best_num_beams（8）。各バッチで generate → batch_decode → postprocess し、`(batch_ids, cleaned)` を `results` に extend。Phase 1 と合わせて提出用リストを完成。完全コードは [[harukiharada_inference_chunked_beam_search_code_20260213000007|本番推論・Chunked Beam Search 完全コード]] の「PHASE 2」を参照。

---

## 実装詳細：提出（Submission）

**完全コード** → [[harukiharada_submission_code_20260213000008|harukiharada - 提出（Submission）完全コード]]

Phase 1・Phase 2 で得た **results**（(id, translation) のリスト）を、列 `id` と `translation` の DataFrame にし、id で昇順ソート。行数が df_test と一致することを assert で確認し、空訳の件数・訳文長の min/max を表示したうえで `submission.csv` に保存。Kaggle ではこの CSV を提出する。

### 実出力（動作確認済み）

| 項目 | 結果 |
|------|------|
| 検証セット | 100 samples for Optuna tuning |
| Metrics backend | built-in fallback（sacrebleu 未使用） |
| Optuna 最良スコア（検証 100 件） | 25.97（幾何平均） |
| Optuna 最良パラメータ | length_penalty≈1.79, num_beams=6 |
| PROVEN Trial 0 (lp=1.5, beams=8) | 25.58 |
| PROVEN Trial 1 (lp=1.3, beams=8) | 25.38 |
| 固定パラメータ検証（lp=1.5, beams=8） | BLEU 15.59, chrF++ 41.97, 幾何平均 25.58 |

- 検証は 100 件のみのためスコアは本番リーダーボード（35.1）より低い。本番提出時は Proven (1.5, 8) を全 test に適用。
- 詳細なログ・全試行一覧は [[harukiharada_optuna_validation_scoring_code_20260213000006|Optuna チューニングと検証評価 完全コード]] の「実行時の出力」を参照。

---

## 実装詳細：データセットの読込・基本確認

**EDA 完全コード** → [[harukiharada_eda_code_20260213000003|harukiharada - EDA 完全コード]]

### データパス・基本確認

- **Kaggle**: `/kaggle/input/deep-past-initiative-machine-translation/train.csv`, `test.csv`
- 行数・列数の print、`df_train.head()` で先頭 5 行を表示

### 実出力（shape）

```
- The train set's shape is 1561 rows and 3 columns.
- The test set's shape is 4 rows and 5 columns.
```

### train.csv の列構成とサンプル

| 列 | 説明 |
|----|------|
| oare_id | 文書の一意 ID（UUID） |
| transliteration | アッカド語転写 |
| translation | 英訳 |

**df_train.head() の例**:

- **転写の例**: `KIŠIB ma-nu-ba-lúm-a-šur DUMU ṣí-lá-(d)IM KIŠIB šu-(d)EN.LÍL...` — ロゴグラム（KIŠIB, DUMU）、ハイフン区切り音節、決定詞 `(d)`
- **翻訳の例**: `Seal of Mannum-balum-Aššur son of Ṣilli-Adad...` — 固有名詞が音写で残る
- 欠損表現: `... he did not give you a textile.` のように `...` で省略されている行あり

※ harukiharada ノートブックは **train.csv をそのまま文書単位で使用**。`Sentences_Oare_FirstWord_LinNum.csv` による文単位分割は行っていない。

### EDA：欠損・重複の確認

- 各列の NULL 数、完全重複行の件数を表示

**実出力**:
```
Missing values per column:
oare_id            0
transliteration    0
translation        0
dtype: int64 

Duplicate count: 0 
```
→ **train.csv** は欠損なし・重複なし。そのまま学習に使用可能。

**補足（プロジェクト EDA との比較）**: harukiharada は `df_train`（train.csv）のみ確認。当プロジェクトの EDA（`deep_past_eda_results_20260211140000`）では **Sentences_Oare_FirstWord_LinNum.csv** に欠損あり（translation: 10, first_word_transcription: 1,247）。文単位分割で Sentences を使う場合は、これら欠損の扱いを要検討。

### EDA：テキスト長（単語数・文字数）の計算

- train に `src_word_count`, `tgt_word_count`, `src_char_count`, `tgt_char_count` を追加。test は転写のみ。`describe()` で分布を出力

**実出力**:
```
Source (transliteration) word count stats:
count    1561.000000
mean       57.531710
std        37.025067
min         3.000000
25%        28.000000
50%        49.000000
75%        84.000000
max       187.000000
Name: src_word_count, dtype: float64

Target (translation) word count stats:
count    1561.000000
mean       90.497758
std        85.203641
min         1.000000
25%        31.000000
50%        68.000000
75%       125.000000
max       744.000000
Name: tgt_word_count, dtype: float64
```
→ 転写の中央値 49 語・最大 187 語、翻訳の中央値 68 語・最大 744 語。当プロジェクト EDA（`deep_past_eda_results_20260211140000`）とほぼ一致。

### EDA：長さ分布の可視化（2×2 ヒストグラム）

- 2×2 サブプロットで転写/翻訳の単語数・文字数ヒストグラム。平均・中央値の縦線あり。茶・金系カラーパレット

### EDA：Train vs Test の分布比較（KDE）

- 転写の単語数・文字数を KDE で Train vs Test 比較。ダミー test は 4 行のため本番では再確認推奨

### EDA：転写 vs 翻訳の長さ関係（散布図・トレンド線・相関）

- 散布図 + 1 次トレンド線 + ピアソン相関。長さ比約 1.47、入力長から出力長の目安に利用

**相関係数の実出力**:
```
Correlation between source and target word counts: 0.783
```
→ **0.783** はかなり強い正の相関。転写が長い文書ほど翻訳も長くなる傾向が明確で、入力長から出力長の目安を立てやすい。

### EDA：欠損マーカー（Gap）の分析

- パターン `\bx\b`, `xx`, `\.\.\.`, `…` で has_gap / gap_count を集計。円グラフとヒストグラムで可視化

**実出力**:
```
Train texts with gaps: 668 (42.8%)
Test texts with gaps:  1 (25.0%)
```
→ Train の約 **43%** に欠損マーカーが含まれる。当プロジェクト EDA の `[]`（9.7%）＋`…`（25.2%）と合わせると、同程度の「何らかの欠損」が多数。Test はダミー 4 件中 1 件に Gap。

### EDA：翻訳側の頻出語（Top 30）

- 全翻訳を連結→小文字化→`Counter` で頻度→上位 30 語を棒グラフ。ドメイン語・機能語の傾向確認

**Top 30 の単語リスト**（グラフより）:

| 順位 | 単語 | 頻度(概算) | 順位 | 単語 | 頻度(概算) |
|------|------|------------|------|------|------------|
| 1 | of | 8,600 | 16 | by | 1,200 |
| 2 | the | 6,900 | 17 | he | 1,150 |
| 3 | and | 4,500 | 18 | with | 1,100 |
| 4 | to | 4,250 | 19 | a | 1,050 |
| 5 | silver | 2,400 | 20 | that | 1,000 |
| 6 | -- | 2,400 | 21 | your | 950 |
| 7 | i | 2,000 | 22 | not | 900 |
| 8 | for | 1,950 | 23 | mina | 850 |
| 9 | you | 1,850 | 24 | is | 800 |
| 10 | son | 1,650 | 25 | will | 750 |
| 11 | in | 1,600 | 26 | have | 700 |
| 12 | shekels | 1,550 | 27 | me | 680 |
| 13 | minas | 1,450 | 28 | as | 660 |
| 14 | from | 1,400 | 29 | 1 | 640 |
| 15 | my | 1,350 | 30 | it | 620 |

- **ドメイン語**: silver, son, shekels, minas, mina（銀・息子・シェケル・ミナ）が上位にあり、商業・度量衡の語彙が特徴的
- **機能語**: of, the, and, to, for, in, from などが最上位
- **特記**: `--`（ダッシュ）が 6 位、数字 `1` が 29 位。前処理で正規化するか検討の余地あり

### EDA：サンプル表示（転写・翻訳の先頭 200 文字）

- `random_state=42` で 5 件サンプリングし、SRC/TGT の先頭 200 文字を表示。表記・欠損マーカー・固有名詞の確認用

**実出力例**（random_state=42 で 5 件）:

| Index | SRC（転写の冒頭）の特徴 | TGT（翻訳の冒頭）の特徴 |
|-------|-------------------------|-------------------------|
| 1526 | 10 ma-na KÙ.BABBAR, 銀・度量衡・人名（i-li-a） | 10 minas of refined silver, merchant, Iliya |
| 1026 | 2-ší-ta na-áš-pé-ra-tum, 手紙・人名（Atata, Assur-ennam） | 2 (unopened) letters of Atata, son of... |
| 354 | KIŠIB, 印章・人名（Ennānum, Puzur-Aššur）, (d)IM.GAL | Sealed by Ennānum son of Ali-abum... |
| 669 | 銀・銅・奴隷取引、um-ma 引用 | To Mannum-kī-Aššur... 1 mina refined silver |
| 643 | a-na ... qí-bi-ma um-ma 手紙形式 | To Šalim-Aššur from Šalim-Aššur: I sent you word... |

- 転写: ロゴグラム（KÙ.BABBAR, KIŠIB, DUMU）、ハイフン区切り音節、下付き数字（₄, ₅）、決定詞 `(d)`、人名・地名が混在
- 翻訳: 商業文・手紙形式（To ... from ...）、mina/shekel、固有名詞の音写（Aššur, Iliya, Kanesh）がそのまま

### EDA：外れ値分析（IQR 法）と長さ比

- IQR 法で src_word_count / tgt_word_count の外れ値件数と Lower/Upper を表示。length_ratio = 翻訳÷転写（clip(lower=1)）の describe()

**実出力**:
```
src_word_count: Lower=-56, Upper=168, Outliers=5
tgt_word_count: Lower=-110, Upper=266, Outliers=63

Length ratio (target/source) stats:
count    1561.000000
mean        1.474496
std         0.670551
min         0.014706
25%         1.250000
50%         1.476190
75%         1.653333
max        11.000000
Name: length_ratio, dtype: float64
```

- **転写**: 外れ値 5 件（おそらく 168 語超の長文）。下限 −56 は単語数ではあり得ないため実質は「上限超え」のみ
- **翻訳**: 外れ値 63 件（266 語超）。翻訳側に極端に長い文書がより多い
- **length_ratio**: 平均 **1.47**・中央値 1.48 で、当プロジェクト EDA と一致。max 11 は「短い転写に対して非常に長い翻訳」のサンプルが存在することを示す

---

## 前処理・チャンキング・後処理（chunky_v1_5_0 準拠）

ノートブック内では **Preprocessor**（入力転写の正規化）、**Akkadian 節境界チャンキング**（長文分割）、**Postprocessor**（翻訳出力の整形）の 3 つが定義されている。

### 1. OptimizedPreprocessor（前処理）

- **役割**: 転写テキストの欠損マーカーを `<big_gap>` / `<gap>` に統一
- **big_gap**: `\.{3,}` または `…+` または `……` → `<big_gap>`
- **small_gap**: `xx+` または `\s+x\s+`（単独の x）→ `<gap>`
- **メソッド**: `preprocess_input_text(text)`, `preprocess_batch(texts)`（バッチ用）

※ 当プロジェクトの前処理ガイド（Ḫ/ḫ→H/h、書記記号除去など）とは別に、**欠損の正規化のみ**をここで実施。他の前処理は別セルで行っている可能性あり。

### 2. Akkadian 節境界チャンキング（split_akkadian）

- **定数**: `CHUNK_MIN_WORDS=15`, `CHUNK_MAX_WORDS=30`, `CHUNK_THRESHOLD=50`
- **CLAUSE_MARKERS**: 節の切れ目とみなすパターン  
  `KIŠIB `, `IGI `, `um-ma `, `a-na ... qí-bi`, `šu-ma `, `\. `, `\[\.\.\.\]`
- **ロジック**:
  - 単語数が **50 以下**なら 1 チャンクのまま返す
  - 50 超なら、単語を順に積みながら「min_words 以上かつ節マーカーで区切れた」または「max_words に達した」タイミングでチャンクを確定
- **用途**: Chunked Beam Search の「長文をモデル入力長に収まる塊に分割する」部分で使用

### 3. VectorizedPostprocessor（後処理）

- **aggressive=True** で多数の整形を適用
- **文字レベルの正規化**:
  - `ḫ`/`Ḫ` → `h`/`H`（テストデータに合わせる）
  - 下付き数字 `₀-₉` → `0-9`
  - **forbidden_chars**（`!?()"——<>⌈⌋⌊[]+ʾ/;`）を削除
- **欠損の統一**: `[x]`, `(x)`, `\bx\b` → `<gap>`。`\.{3,}`, `…`, `\[\.+\]` → `<big_gap>`。連続する `<gap>` / `<big_gap>` は適宜統合
- **注釈除去**: `(fem)`, `(plur)`, `(pl)`, `(sing)`, `(?...)` などのパターンを削除
- **分数表記**: `0.5`→`½`, `0.25`→`¼`, `0.75`→`¾` および `(\d+)\.5` などを対応する分数記号に
- **重複除去**: 同一単語の連続、同一 n-gram の連続（2〜4 語）、および **remove_phrase_repeats**（3〜8 語の句の繰り返しをスライディングウィンドウで削除）
- **その他**: 空白・句読点の正規化、末尾の不完全文のトリム（**trim_trailing_fragment**）

### コード（抜粋・要約）

```python
# PREPROCESSOR
class OptimizedPreprocessor:
    def __init__(self):
        self.patterns = {
            'big_gap': re.compile(r'(\.{3,}|…+|……)'),
            'small_gap': re.compile(r'(xx+|\s+x\s+)'),
        }
    def preprocess_input_text(self, text: str) -> str: ...
    def preprocess_batch(self, texts: List[str]) -> List[str]: ...

# CHUNKING
CHUNK_MIN_WORDS, CHUNK_MAX_WORDS = 15, 30
CHUNK_THRESHOLD = 50
CLAUSE_MARKERS = [r'KIŠIB\s+', r'IGI\s+', r'um-ma\s+', r'a-na\s+\S+\s+qí-bi', r'šu-ma\s+', r'\.\s+', r'\[\.\.\.\]\s*']
def split_akkadian(text, max_words=CHUNK_MAX_WORDS, min_words=CHUNK_MIN_WORDS) -> List[str]: ...

# POSTPROCESSOR
def remove_phrase_repeats(text): ...   # 3-8語の繰り返し句を削除
def trim_trailing_fragment(text): ...   # 末尾の不完全文をトリム
class VectorizedPostprocessor:
    def __init__(self, aggressive: bool = True): ...
    def postprocess_batch(self, translations: List[str]) -> List[str]: ...

preprocessor = OptimizedPreprocessor()
postprocessor = VectorizedPostprocessor(aggressive=True)
```

※ 完全な実装は別ノートに分離した。**完全コード** → [[harukiharada_preprocessor_postprocessor_code_20260213000000|harukiharada - 前処理・チャンキング・後処理 完全コード（chunky_v1_5_0）]]

### ローカル再現時のパス

- Kaggle の `/kaggle/input/...` は、ローカルでは `data/raw/train.csv`, `data/raw/test.csv` などに置き換える

---

## 関連リソース

### Kaggle Datasets

- **pascalledesma/deep-past-byt5-models**: Deep Past 向け ByT5 ファインチューニング済みモデル
  - コンペ用に事前学習・ファインチューニングされた ByT5 を利用可能

### HuggingFace

- **google/byt5-base**: ベースモデル（未ファインチューニング）
- **google/byt5-large**: 大容量版

### 依存関係（推測）

- `transformers`（T5ForConditionalGeneration / ByT5）
- `torch`
- `optuna`
- `sacrebleu`（評価）
- `pandas`

## 再現時の方針

1. **Kaggle からノートブックを取得**
   - Kaggle CLI: `kaggle kernels pull harukiharada/byt5-optuna-tuning-chunked-beam-search`
   - または手動で Notebook をダウンロード
2. **モデル取得**
   - pascalledesma のデータセットを Kaggle から追加
   - または google/byt5-base を HuggingFace から取得し、自前でファインチューニング
3. **前処理**
   - 既存の [[deep_past_preprocessing_20260211130000]] 方針に従う（Ḫ/ḫ→H/h、書記記号除去等）
4. **データ**
   - train を文単位に分割（[[deep_past_eda_results_20260211140000]] 参照）
   - `Sentences_Oare_FirstWord_LinNum.csv` を利用

## 関連ノート

- [[harukiharada_preprocessor_postprocessor_code_20260213000000|前処理・チャンキング・後処理 完全コード（chunky_v1_5_0）]]
- [[harukiharada_metrics_fallback_code_20260213000002|ライブラリ・インポート・評価指標フォールバック 完全コード]]
- [[harukiharada_eda_code_20260213000003|EDA 完全コード]]
- [[harukiharada_model_load_code_20260213000004|モデル読込 完全コード]]
- [[harukiharada_dataset_sampler_code_20260213000005|Dataset と BucketBatchSampler 完全コード]]
- [[harukiharada_optuna_validation_scoring_code_20260213000006|Optuna チューニングと検証評価 完全コード]]
- [[harukiharada_inference_chunked_beam_search_code_20260213000007|本番推論・Chunked Beam Search 完全コード]]
- [[harukiharada_submission_code_20260213000008|提出（Submission）完全コード]]
- [[akkadian_mt_preprocessing_ensemble_reference_20260211130000|Akkadian MT 前処理 & アンサンブル実装リファレンス]]
- [[deep_past_preprocessing_20260211130000|前処理ガイド（実データ確認済み）]]
- [[deep_past_eda_results_20260211140000|EDA 結果]]
- [[deep_past_competition_evaluation_submission_20260210130000|評価と提出方法]]
