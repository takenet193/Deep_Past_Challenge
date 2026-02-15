---
id: 20260213000006
title: harukiharada - Optuna チューニングと検証評価 完全コード
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - optuna
  - bleu
  - chrf
  - byt5
links:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
  - harukiharada_preprocessor_postprocessor_code_20260213000000
  - harukiharada_metrics_fallback_code_20260213000002
  - harukiharada_inference_chunked_beam_search_code_20260213000007
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - Optuna チューニングと検証評価 完全コード

harukiharada 氏のノートブック「ByT5 + Optuna Tuning + Chunked Beam Search」の**Optuna ハイパーパラメータ探索**と**検証評価**まわりの完全コード。検証分割・翻訳・スコア関数・Optuna Study・固定パラメータ検証・可視化・サンプル表示まで。本番推論（test 用設定・Chunked Beam Search・提出）は [[harukiharada_inference_chunked_beam_search_code_20260213000007|本番推論・Chunked Beam Search 完全コード]] を参照。

- **元ノート**: [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000]]
- **依存**: [[harukiharada_preprocessor_postprocessor_code_20260213000000]]（preprocessor, postprocessor）、[[harukiharada_metrics_fallback_code_20260213000002]]（USE_SACREBLEU, フォールバック）、`tokenizer`, `model`, `device`, `autocast`

---

## コード

```python
# ============================================================
# VALIDATION SPLIT FOR OPTUNA
# ============================================================

# Use a small sample for fast tuning
VAL_SIZE = 100
np.random.seed(42)
val_indices = np.random.choice(len(df_train), size=min(VAL_SIZE, len(df_train)), replace=False)
df_val = df_train.iloc[val_indices].reset_index(drop=True)
print(f"Validation set: {len(df_val)} samples for Optuna tuning")


def translate_batch_with_params(texts, length_penalty, num_beams, max_new_tokens=512):
    """Translate a list of texts with specific generation parameters."""
    preprocessed = preprocessor.preprocess_batch(texts)
    prefixed = ['translate Akkadian to English: ' + t for t in preprocessed]
    
    translations = []
    batch_size = 4
    
    with torch.inference_mode():
        for i in range(0, len(prefixed), batch_size):
            batch = prefixed[i:i + batch_size]
            inputs = tokenizer(batch, max_length=512, padding=True, truncation=True, return_tensors='pt')
            input_ids = inputs.input_ids.to(device)
            attention_mask = inputs.attention_mask.to(device)
            
            with autocast():
                outputs = model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    num_beams=num_beams,
                    max_new_tokens=max_new_tokens,
                    length_penalty=length_penalty,
                    early_stopping=True,
                    use_cache=True,
                )
            
            decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            translations.extend(decoded)
    
    cleaned = postprocessor.postprocess_batch(translations)
    return cleaned


def compute_bleu(predictions, references):
    """Corpus BLEU score."""
    if USE_SACREBLEU:
        return sacrebleu.corpus_bleu(predictions, [references]).score
    return _corpus_bleu_fallback(predictions, references)


def compute_chrf(predictions, references):
    """Corpus chrF++ score."""
    if USE_SACREBLEU:
        return sacrebleu.corpus_chrf(predictions, [references], word_order=2).score
    return _chrf_pp_fallback(predictions, references)


def compute_sentence_bleu(hypothesis, reference):
    """Sentence-level BLEU."""
    if USE_SACREBLEU:
        return sacrebleu.sentence_bleu(hypothesis, [reference]).score
    return _sentence_bleu_fallback(hypothesis, reference)


def compute_competition_score(predictions, references):
    """Compute geometric mean of BLEU and chrF++."""
    bleu_score = compute_bleu(predictions, references)
    chrf_score = compute_chrf(predictions, references)
    
    if bleu_score <= 0 or chrf_score <= 0:
        return 0.0
    
    return math.sqrt(bleu_score * chrf_score)


print("Translation and scoring functions ready.")
print(f"Metrics backend: {'sacrebleu' if USE_SACREBLEU else 'built-in fallback'}")
```

---

## 補足

### 検証分割（Optuna 用）

| 項目 | 内容 |
|------|------|
| VAL_SIZE | 100。チューニングを速くするため train の一部のみを検証に使用 |
| サンプリング | `np.random.seed(42)` で再現性を固定。`np.random.choice(..., replace=False)` で重複なしに 100 件のインデックスを取得 |
| df_val | `df_train.iloc[val_indices]` で検証用 DataFrame を作成。Optuna の目的関数内で「この df_val を翻訳 → スコア計算」に使う |

### translate_batch_with_params

| 項目 | 内容 |
|------|------|
| 引数 | `texts`: 転写のリスト。`length_penalty`, `num_beams`: 生成パラメータ（Optuna で探索）。`max_new_tokens`: 最大生成トークン数（デフォルト 512） |
| 前処理 | `preprocessor.preprocess_batch(texts)` → プレフィックス `'translate Akkadian to English: ' + t` を付与 |
| バッチ | 内部で `batch_size=4` に固定。`tokenizer(..., max_length=512, padding=True, truncation=True)` でパディング・切り詰め |
| 生成 | `torch.inference_mode()` と `autocast()` 内で `model.generate(num_beams=..., length_penalty=..., early_stopping=True, use_cache=True)` |
| 後処理 | `tokenizer.batch_decode(..., skip_special_tokens=True)` のあと `postprocessor.postprocess_batch(translations)` で整形して返す |

### スコア関数

| 関数 | 役割 |
|------|------|
| compute_bleu | コーパス BLEU。USE_SACREBLEU なら sacrebleu、そうでなければ built-in _corpus_bleu_fallback |
| compute_chrf | コーパス chrF++。sacrebleu の場合は word_order=2。そうでなければ _chrf_pp_fallback |
| compute_sentence_bleu | 文単位 BLEU（1 文 vs 1 文） |
| compute_competition_score | BLEU と chrF++ の幾何平均。0 以下は 0.0 として扱い sqrt(bleu * chrf) を返す |

※ コンペの公式スコアは BLEU と chrF++ の幾何平均のため、Optuna の目的関数は `compute_competition_score` を最大化する形で使う。

---

## Optuna Study（目的関数・最適化・結果表示）

```python
# ============================================================
# OPTUNA STUDY (seeded with proven baselines)
# ============================================================

# Known good parameters from top public notebooks
PROVEN_PARAMS = [
    {'length_penalty': 1.5, 'num_beams': 8},   # chunky_v1_5_0 → 35.1
    {'length_penalty': 1.3, 'num_beams': 8},   # adaptive-beams → 35.1
]

def objective(trial):
    length_penalty = trial.suggest_float('length_penalty', 0.8, 2.0)
    num_beams = trial.suggest_int('num_beams', 4, 12)
    
    source_texts = df_val['transliteration'].tolist()
    reference_texts = df_val['translation'].tolist()
    
    predictions = translate_batch_with_params(
        source_texts,
        length_penalty=length_penalty,
        num_beams=num_beams,
    )
    
    score = compute_competition_score(predictions, reference_texts)
    return score


study = optuna.create_study(direction='maximize')

# Enqueue proven baselines so they are always evaluated first
for params in PROVEN_PARAMS:
    study.enqueue_trial(params)

study.optimize(objective, n_trials=20, timeout=3600 * 2)

# Compare Optuna best vs proven baselines
print("\n" + "=" * 60)
print("OPTUNA RESULTS")
print("=" * 60)
print(f"Best Score (geometric mean): {study.best_value:.2f}")
print(f"Best params: {study.best_params}")

# Show all trial results sorted by score
print("\nAll trials (sorted by score):")
trials_sorted = sorted(study.trials, key=lambda t: t.value if t.value is not None else 0, reverse=True)
for t in trials_sorted[:10]:
    tag = ""
    if t.params in PROVEN_PARAMS:
        tag = " [PROVEN BASELINE]"
    print(f"  Trial {t.number}: score={t.value:.2f}, lp={t.params['length_penalty']:.3f}, beams={t.params['num_beams']}{tag}")
print("=" * 60)
```

### 補足（Optuna Study）

| 項目 | 内容 |
|------|------|
| PROVEN_PARAMS | 公開ノートで実績のある組み合わせ。chunky_v1_5_0 と adaptive-beams の 2 セット（いずれもスコア 35.1）。最初の試行として必ず評価するために enqueue する |
| objective(trial) | `length_penalty` を 0.8〜2.0 の連続値、`num_beams` を 4〜12 の整数でサジェスト。df_val の転写を `translate_batch_with_params` で翻訳し、正解との `compute_competition_score` を返す |
| create_study | `direction='maximize'` でスコア最大化。サンプラーはデフォルト（TPESampler） |
| enqueue_trial | PROVEN_PARAMS の各組をキューに積み、最初の 2 試行として実行。ランダム探索より先に既知の良い点を評価できる |
| optimize | `n_trials=20`、`timeout=3600*2`（2 時間）で探索。先に enqueue した 2 試行 + 最大 18 試行の TPESampler 提案 |
| 結果表示 | 最良スコア・最良パラメータ、および全試行をスコア降順で上位 10 件表示。PROVEN_PARAMS に含まれる試行は `[PROVEN BASELINE]` でタグ付け |

---

## Optuna 結果の可視化

```python
# Visualize Optuna results
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Trial scores
trial_numbers = [t.number for t in study.trials]
trial_values = [t.value for t in study.trials]
axes[0].plot(trial_numbers, trial_values, 'o-', color='#8b6914', markersize=8)
axes[0].axhline(study.best_value, color='#d4a843', linestyle='--', label=f'Best: {study.best_value:.2f}')
axes[0].set_xlabel('Trial Number')
axes[0].set_ylabel('Score (Geometric Mean)')
axes[0].set_title('Optuna Trial Scores', fontweight='bold')
axes[0].legend()

# Parameter importance - length_penalty vs score
lp_values = [t.params['length_penalty'] for t in study.trials]
axes[1].scatter(lp_values, trial_values, c='#8b6914', s=60, edgecolors='#2c1810')
axes[1].set_xlabel('length_penalty')
axes[1].set_ylabel('Score')
axes[1].set_title('length_penalty vs Score', fontweight='bold')

plt.tight_layout()
plt.show()
```

### 補足（可視化）

| 左図（Trial Scores） | 試行番号を横軸、スコア（幾何平均）を縦軸に折れ線プロット。破線で最良スコアの水準線を表示。試行の推移と最良値の位置が分かる |
| 右図（length_penalty vs Score） | 横軸に length_penalty、縦軸にスコアの散布図。num_beams は色分けしていないが、lp とスコアの傾向（例: 1.6〜2.0 付近で高めなど）を確認する用 |
| 色 | 茶・金系（#8b6914, #d4a843, #2c1810）で EDA 等のノートブック内パレットと統一 |

### 実行時の可視化の例

- **左図（Optuna Trial Scores）**: 試行 0〜19 のスコアが折れ線で並び、Trial 5 付近で一度低下（約 23.2）したあと回復し、Trial 13・15・16・17 などで最良付近（25.97 の水準線）に達している。破線が Best: 25.97 を示す。
- **右図（length_penalty vs Score）**: lp が 0.8〜1.0 付近ではスコアが低く、1.6〜2.0 で高スコアが集中。特に 1.7〜1.8 付近に最良スコアの点が集まり、それ以上に lp を上げてもスコアは頭打ち〜やや低下する傾向。length_penalty の感度と有望域が把握できる。

---

## 固定生成パラメータと検証評価

- Optuna の結果は**分析・探索用**とし、**test 推論では chunky_v1_5_0 で実績のあるパラメータを固定**して使う。このブロックでその固定値で検証セットを評価し、BLEU / chrF++ / 幾何平均を表示する。

```python
# ============================================================
# FIXED GENERATION PARAMS (exact match: chunky_v1_5_0)
# ============================================================
# Use proven parameters for test inference regardless of Optuna results.
# Optuna above is for analysis/exploration only.

FIXED_LENGTH_PENALTY = 1.5
FIXED_NUM_BEAMS = 8

# Show Optuna comparison
print("Optuna best vs proven baseline:")
print(f"  Optuna:  lp={study.best_params['length_penalty']:.3f}, beams={study.best_params['num_beams']}, score={study.best_value:.2f}")
print(f"  Proven:  lp={FIXED_LENGTH_PENALTY}, beams={FIXED_NUM_BEAMS}")

# Evaluate proven params on validation
best_length_penalty = FIXED_LENGTH_PENALTY
best_num_beams = FIXED_NUM_BEAMS

val_predictions = translate_batch_with_params(
    df_val['transliteration'].tolist(),
    length_penalty=best_length_penalty,
    num_beams=best_num_beams,
)
val_references = df_val['translation'].tolist()

bleu_score = compute_bleu(val_predictions, val_references)
chrf_score = compute_chrf(val_predictions, val_references)
geo_mean = math.sqrt(bleu_score * chrf_score) if bleu_score > 0 and chrf_score > 0 else 0.0

print(f"\nValidation Results (proven params: lp={best_length_penalty}, beams={best_num_beams}):")
print(f"  BLEU:  {bleu_score:.2f}")
print(f"  chrF++: {chrf_score:.2f}")
print(f"  Geometric Mean: {geo_mean:.2f}")
```

### 補足（固定パラメータ・検証評価）

| 項目 | 内容 |
|------|------|
| FIXED_* | chunky_v1_5_0 と同一: length_penalty=1.5, num_beams=8。本番 test 推論でもこの値を使う方針 |
| Optuna との比較 | 画面上で Optuna 最良（lp, beams, score）と Proven（1.5, 8）を並べて表示。Optuna は参考のみ |
| 検証評価 | df_val の転写を `translate_batch_with_params(..., lp=1.5, beams=8)` で翻訳し、正解と BLEU / chrF++ / 幾何平均を算出して表示。本番前の最終確認用 |

### 固定パラメータ・検証評価の実行結果（実例）

```
Optuna best vs proven baseline:
  Optuna:  lp=1.788, beams=6, score=25.97
  Proven:  lp=1.5, beams=8

Validation Results (proven params: lp=1.5, beams=8):
  BLEU:  15.59
  chrF++: 41.97
  Geometric Mean: 25.58
```

- Proven (1.5, 8) で検証 100 件を評価した幾何平均は **25.58**。Optuna 最良 25.97 よりやや低いが、本番では Proven を採用。BLEU 15.59・chrF++ 41.97 は検証 100 件のみの値。

---

## メトリクス可視化（Validation Metrics）

- 固定パラメータ（lp=1.5, beams=8）で検証した結果を、**コーパス指標の棒グラフ**と**文単位 BLEU のヒストグラム**で可視化する。

```python
# ============================================================
# METRIC VISUALIZATION
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart of metrics
metrics = ['BLEU', 'chrF++', 'Geometric Mean']
values = [bleu_score, chrf_score, geo_mean]
colors = ['#2c1810', '#8b6914', '#d4a843']
bars = axes[0].bar(metrics, values, color=colors, edgecolor='#2c1810', linewidth=1.5)
for bar, val in zip(bars, values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.2f}', ha='center', fontweight='bold', fontsize=12)
axes[0].set_ylabel('Score')
axes[0].set_title('Validation Metrics', fontweight='bold')
axes[0].set_ylim(0, max(values) * 1.2)

# Per-sample BLEU distribution
per_sample_bleu = []
for pred, ref in zip(val_predictions, val_references):
    s = compute_sentence_bleu(pred, ref)
    per_sample_bleu.append(s)

axes[1].hist(per_sample_bleu, bins=30, color='#8b6914', alpha=0.7, edgecolor='#2c1810')
axes[1].axvline(np.mean(per_sample_bleu), color='#d4a843', linestyle='--', linewidth=2,
                label=f'Mean: {np.mean(per_sample_bleu):.1f}')
axes[1].set_xlabel('Sentence BLEU')
axes[1].set_ylabel('Count')
axes[1].set_title('Per-Sample BLEU Distribution', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.show()
```

### 補足（メトリクス可視化）

| 左図（Validation Metrics） | BLEU・chrF++・幾何平均を棒グラフで表示。各棒の上に数値をラベル。茶・金系（#2c1810, #8b6914, #d4a843）で統一 |
| 右図（Per-Sample BLEU） | 検証 100 件それぞれについて `compute_sentence_bleu(pred, ref)` を計算し、30 ビンでヒストグラム。破線で平均を表示。文ごとの BLEU のばらつき・外れ値の有無を確認する用 |
| 依存 | 直前の「固定パラメータと検証評価」で得た `bleu_score`, `chrf_score`, `geo_mean`, `val_predictions`, `val_references` を使用 |

---

## サンプル予測 vs 正解（Sample Predictions vs References）

- 検証セットの先頭 5 件について、**転写（SRC）・正解（REF）・モデル予測（PRED）** と **文単位 BLEU** を並べて表示する。品質の確認と失敗例の把握用。

```python
# ============================================================
# SAMPLE PREDICTIONS VS REFERENCES
# ============================================================

print("Sample Predictions vs References:")
for i in range(min(5, len(val_predictions))):
    s_bleu = compute_sentence_bleu(val_predictions[i], val_references[i])
    print("=" * 70)
    print(f"[{i}] BLEU: {s_bleu:.1f}")
    print(f"SRC:  {df_val.iloc[i]['transliteration'][:150]}")
    print(f"REF:  {val_references[i][:150]}")
    print(f"PRED: {val_predictions[i][:150]}")
print("=" * 70)
```

### 補足（サンプル表示）

| 項目 | 内容 |
|------|------|
| 件数 | 先頭 5 件（`min(5, len(val_predictions))`）。検証が 5 件未満なら全件 |
| 表示内容 | 各件ごとに文 BLEU、SRC（転写の先頭 150 文字）、REF（正解の先頭 150 文字）、PRED（予測の先頭 150 文字） |
| 用途 | 翻訳の質の目視確認、固有名詞・数値の誤り、欠損マーカー周りの挙動、低 BLEU の要因の把握 |

### 実行結果（実例）

```
Sample Predictions vs References:
======================================================================
[0] BLEU: 34.7
SRC:  10 ma-na KÙ.BABBAR ṣa-ru-pu-um ni-is-ḫa-sú DIRI ša-du-a-sú ša-bu ša tám-kà-ri-im a-na i-li-a ù ša ki-ma lá-qé-ep ù a-ḫa-ma 0.33333 ma-na KÙ.BABBAR ša 
REF:  10 minas of refined silver, its excise added, his transport fee paid, belonging to the merchant, for Iliya and the representatives of Lā-qēp, and sepa
PRED: 10 minas of refined silver, its import duty added, its transport tariff paid for, belonging to a merchant, to Iliya and the representatives of Lā-qēp,
======================================================================
[1] BLEU: 1.0
SRC:  2-ší-ta na-áš-pé-ra-tum lá pá-tí-a-tum ša a-ta-ta DUMU ma-num-ba-lum-a-šùr a-ṣé-ri-a ú a-ṣé-er a-šùr-e-nam DUMU ku-bi-a 2-ší-ta na-áš-pé-ra-tum ša a-b
REF:  2 (unopened) letters of Atata, son of Mannum-balum-Assur, addressed to me and to Assur-ennam, son of Kubiya; two (unopened) letters of our father to B
PRED: Atata son of Mannum-balum-Aššur to me and to Aššur-ennam son of Kubiya 2 additional letters of our father to Bēlum-bāni son of Šu-Bēlum a tablet with 
======================================================================
[2] BLEU: 63.4
SRC:  KIŠIB en-na-nim DUMU a-lá-bi₄-im KIŠIB a-gi-a DUMU PUZUR₄-a-šùr (d)IM.GAL DUMU bu-zi tap-pá-i-ni a-na a-wa-tim a-ni-a-tim kà-ru-um kà-ni-iš i-dí-ni-a-
REF:  Sealed by Ennānum son of Ali-abum, by Agiya son of Puzur-Aššur; Adad-rabi son of Buzi was our (absent) partner. The Kanesh colony gave us for these pr
PRED: Seal of Ennānum son of Ali-abum, seal of Agiya son of Puzur-Aššur, Adad-rabi son of Buzi, our colleague. The Kanesh colony gave us for these proceedin
======================================================================
[3] BLEU: 6.8
SRC:  a-na ma-nu-ki-a-šùr na-áb-sú-in a-na-na ù da-ra-áš qí-bi-ma um-ma en-nam-a-šur-ma 1 ma-na KÙ.BABBAR ṣa-ru-pá-am ku-nu-ki-a 30 ma-na URUDU SIG₅ ku-nu-k
REF:  To Mannum-kī-Aššur, Nab-Suen, Anna-anna and Daraš from Ennam-Aššur: As to the 1 mina of refined silver under my seal, 30 minas of good copper under my
PRED: To Mannum-kī-Aššur, Nab-Suen, Anna-anna and Daraš from Ennam-Aššur: 1 mina of refined silver under my seal, 30 minas of good copper under my seal, 2 d
======================================================================
[4] BLEU: 5.7
SRC:  a-na ša-lim-a-šur qí-bi-ma um-ma ša-lim-a-šur-ma a-šu-mì ili₅-ba-ni DUMU i-a-a a-dí ší-ni-šu tí-ir-tí i-li-kà-ku-um ki-ma lá-am-ni-iš e-ta-na-pu-šu iš
REF:  To Šalim-Aššur from Šalim-Aššur: I sent you word twice about Ilī-bāni son of Yaya. Since he keeps behaving in an evil manner a message from Aššur-mali
PRED: To Šalim-Aššur from Šalim-Aššur: Concerning Ilī-bāni, son of Yaya, until his first message, a message came to you since he was strict. From Nahriya th
======================================================================
```

- **[0] BLEU 34.7**: 銀・度量衡・人名（Iliya, Lā-qēp）はおおむね一致。REF の "excise" / "transport fee" が PRED では "import duty" / "transport tariff" など言い換えで BLEU が伸び悩む典型。
- **[1] BLEU 1.0**: REF は "2 (unopened) letters of Atata... addressed to me and to Assur-ennam... two (unopened) letters of our father to B..."。PRED は構造がずれ「Atata son of ... to me and to ... 2 additional letters...」となり、語順・表現のずれが大きく低スコア。
- **[2] BLEU 63.4**: 印章・人名・"Kanesh colony" がよく合っている。"(absent) partner" → "colleague" など部分的な言い換えのみ。
- **[3][4] BLEU 6.8 / 5.7**: 手紙形式（To ... from ...）は維持しているが、中身の内容・論理が REF とずれており、文単位では低い。長文・複雑な文で誤りが目立つ例。

---

## 実行時の出力（実例）

```
Validation set: 100 samples for Optuna tuning
Translation and scoring functions ready.
Metrics backend: built-in fallback
```

- 検証セットは 100 件が正しく作成されている。
- 翻訳・スコア関数の定義後、メトリクスは sacrebleu が使えない環境のため **built-in fallback** で動作している（[[harukiharada_metrics_fallback_code_20260213000002|評価指標フォールバック]] の純 Python 実装を使用）。

### Optuna Study の実行結果（実例）

- 20 試行・約 2 時間で探索。Trial 0/1 が PROVEN_PARAMS（lp=1.5 & beams=8 → 25.58、lp=1.3 & beams=8 → 25.38）。最良は Trial 15（lp≈1.79, beams=6）で **25.97**。
- 検証は 100 件のみのため、本番リーダーボードの 35.1 より低い値になる。本番提出時は Optuna で得た最良パラメータ（または PROVEN のどれか）を全 test に適用する。

```
[I 2026-02-08 11:40:32,431] A new study created in memory with name: no-name-a2fe3c8d-8dbc-4373-a0d0-7dd9ef86422b
[I 2026-02-08 11:43:59,099] Trial 0 finished with value: 25.576987990372732 and parameters: {'length_penalty': 1.5, 'num_beams': 8}. Best is trial 0 with value: 25.576987990372732.
[I 2026-02-08 11:47:23,955] Trial 1 finished with value: 25.381272576017505 and parameters: {'length_penalty': 1.3, 'num_beams': 8}. Best is trial 0 with value: 25.576987990372732.
[I 2026-02-08 11:50:41,941] Trial 2 finished with value: 25.933034374767363 and parameters: {'length_penalty': 1.9410391230400283, 'num_beams': 7}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 11:54:07,068] Trial 3 finished with value: 25.068790062717373 and parameters: {'length_penalty': 1.0763075540193068, 'num_beams': 8}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 11:57:32,303] Trial 4 finished with value: 25.460830725454308 and parameters: {'length_penalty': 1.417257315575548, 'num_beams': 8}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:01:05,801] Trial 5 finished with value: 23.200689487371797 and parameters: {'length_penalty': 0.855589105117315, 'num_beams': 9}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:04:05,932] Trial 6 finished with value: 24.395221964784394 and parameters: {'length_penalty': 1.0460986973680495, 'num_beams': 5}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:07:39,930] Trial 7 finished with value: 25.38004111493745 and parameters: {'length_penalty': 1.5713880696533393, 'num_beams': 9}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:11:12,054] Trial 8 finished with value: 25.20992707293319 and parameters: {'length_penalty': 1.177782943927798, 'num_beams': 9}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:14:35,159] Trial 9 finished with value: 25.211151005188942 and parameters: {'length_penalty': 1.121842259648785, 'num_beams': 8}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:17:34,141] Trial 10 finished with value: 25.58061938050074 and parameters: {'length_penalty': 1.9875136713914134, 'num_beams': 5}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:20:33,480] Trial 11 finished with value: 25.668365016010156 and parameters: {'length_penalty': 1.9428541038579183, 'num_beams': 5}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:23:51,241] Trial 12 finished with value: 25.658023547603364 and parameters: {'length_penalty': 1.9924390704564896, 'num_beams': 4}. Best is trial 2 with value: 25.933034374767363.
[I 2026-02-08 12:27:00,797] Trial 13 finished with value: 25.953272794557634 and parameters: {'length_penalty': 1.7673635393977019, 'num_beams': 6}. Best is trial 13 with value: 25.953272794557634.
[I 2026-02-08 12:31:07,724] Trial 14 finished with value: 25.313138653090927 and parameters: {'length_penalty': 1.665532623802196, 'num_beams': 12}. Best is trial 13 with value: 25.953272794557634.
[I 2026-02-08 12:34:15,526] Trial 15 finished with value: 25.965237888609767 and parameters: {'length_penalty': 1.7879441972316252, 'num_beams': 6}. Best is trial 15 with value: 25.965237888609767.
[I 2026-02-08 12:37:24,197] Trial 16 finished with value: 25.953272794557634 and parameters: {'length_penalty': 1.756056421197431, 'num_beams': 6}. Best is trial 15 with value: 25.965237888609767.
[I 2026-02-08 12:40:33,167] Trial 17 finished with value: 25.965237888609767 and parameters: {'length_penalty': 1.7856074866444467, 'num_beams': 6}. Best is trial 15 with value: 25.965237888609767.
[I 2026-02-08 12:44:28,798] Trial 18 finished with value: 25.64322623654007 and parameters: {'length_penalty': 1.7936878738830513, 'num_beams': 11}. Best is trial 15 with value: 25.965237888609767.
[I 2026-02-08 12:47:46,756] Trial 19 finished with value: 25.91437219947655 and parameters: {'length_penalty': 1.639305745958036, 'num_beams': 4}. Best is trial 15 with value: 25.965237888609767.
============================================================
OPTUNA RESULTS
============================================================
Best Score (geometric mean): 25.97
Best params: {'length_penalty': 1.7879441972316252, 'num_beams': 6}

All trials (sorted by score):
  Trial 15: score=25.97, lp=1.788, beams=6
  Trial 17: score=25.97, lp=1.786, beams=6
  Trial 13: score=25.95, lp=1.767, beams=6
  Trial 16: score=25.95, lp=1.756, beams=6
  Trial 2: score=25.93, lp=1.941, beams=7
  Trial 19: score=25.91, lp=1.639, beams=4
  Trial 11: score=25.67, lp=1.943, beams=5
  Trial 12: score=25.66, lp=1.992, beams=4
  Trial 18: score=25.64, lp=1.794, beams=11
  Trial 10: score=25.58, lp=1.988, beams=5
============================================================
```
