---
id: 20260213000007
title: harukiharada - 本番推論・Chunked Beam Search 完全コード
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - byt5
  - chunked-beam-search
  - inference
links:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
  - harukiharada_preprocessor_postprocessor_code_20260213000000
  - harukiharada_optuna_validation_scoring_code_20260213000006
  - harukiharada_submission_code_20260213000008
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - 本番推論・Chunked Beam Search 完全コード

harukiharada 氏のノートブック「ByT5 + Optuna Tuning + Chunked Beam Search」の**本番 test 推論**まわり。**推論設定（test_dataset, collate_fn）**と**Chunked Beam Search Phase 1**（長文の節境界チャンキング翻訳）の完全コード。Phase 2 までを記載。提出は [[harukiharada_submission_code_20260213000008|提出（Submission）完全コード]] を参照。

- **元ノート**: [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000]]
- **前提**: [[harukiharada_optuna_validation_scoring_code_20260213000006|Optuna チューニングと検証評価]]で固定パラメータ（best_length_penalty=1.5, best_num_beams=8）を設定済み。[[harukiharada_preprocessor_postprocessor_code_20260213000000]]の split_akkadian, postprocessor を使用。

---

## 本番推論の設定（FULL INFERENCE CONFIG）

- **test 用**の推論設定を chunky_v1_5_0 に合わせ、**AkkadianDataset** と **collate_fn** で DataLoader に渡すバッチを用意する。実際の生成ループ（Chunked Beam Search 等）は次のセル以降で行う想定。

```python
# ============================================================
# FULL INFERENCE CONFIG (exact match: chunky_v1_5_0)
# ============================================================

BATCH_SIZE = 8
MAX_LENGTH = 512
NUM_WORKERS = 4
NUM_BUCKETS = 4

print(f"Inference config: length_penalty={best_length_penalty}, num_beams={best_num_beams}")
print(f"Test samples: {len(df_test)}")

test_dataset = AkkadianDataset(df_test, preprocessor)

def collate_fn(batch):
    ids = [s[0] for s in batch]
    texts = [s[1] for s in batch]
    tokenized = tokenizer(texts, max_length=MAX_LENGTH, padding=True, truncation=True, return_tensors='pt')
    return ids, tokenized

print(f"Dataset ready: {len(test_dataset)} samples")
```

### 補足（本番推論設定）

| 項目 | 内容 |
|------|------|
| BATCH_SIZE / MAX_LENGTH | 8 と 512。検証時の translate_batch_with_params の内部 batch_size=4 より大きく、本番用 |
| NUM_WORKERS / NUM_BUCKETS | DataLoader の並列数と BucketBatchSampler のバケット数（ここではサンプラーはまだ使っていないが、後続で DataLoader に渡す際の設定候補） |
| best_length_penalty, best_num_beams | 直前の「固定パラメータ」で設定した 1.5 と 8。推論時も同じ値を使う |
| test_dataset | `AkkadianDataset(df_test, preprocessor)` で test の転写を前処理・プレフィックス付与。`__getitem__` は (id, input_text) |
| collate_fn | バッチを (ids, tokenized) にまとめる。ids は提出用 ID のリスト、tokenized は tokenizer の出力（input_ids, attention_mask 等）。DataLoader の `collate_fn=collate_fn` で使用 |

### 実行結果（実例）

```
Inference config: length_penalty=1.5, num_beams=8
Test samples: 4
Dataset created: 4 samples
Dataset ready: 4 samples
```

- 使用パラメータは lp=1.5, beams=8（Proven）。test は 4 件（Kaggle のダミー test やローカル確認用の小さい test の想定）。本番コンペでは test 件数はこれより多い。

---

## PHASE 1: 長文のチャンキング翻訳（Chunked Beam Search）

- **単語数が CHUNK_THRESHOLD 超**の test だけ、[[harukiharada_preprocessor_postprocessor_code_20260213000000|split_akkadian]] で節境界チャンクに分割し、チャンクごとにビームサーチで翻訳してから結合・後処理する。短い文は Phase 2 でまとめて処理する想定。

```python
# ============================================================
# PHASE 1: CHUNK LONG TEXTS (exact match: chunky_v1_5_0)
# Fixed num_beams for chunked texts
# ============================================================

results = []
chunked_ids = set()

gen_config_chunk = {
    'num_beams': best_num_beams,
    'max_new_tokens': 512,
    'length_penalty': best_length_penalty,
    'early_stopping': True,
    'use_cache': True,
}

print("Phase 1: Translating long texts with clause-boundary chunking...")

with torch.inference_mode():
    for idx in range(len(test_dataset)):
        sample_id, input_text = test_dataset[idx]
        raw_text = input_text.replace('translate Akkadian to English: ', '')
        
        if len(raw_text.split()) > CHUNK_THRESHOLD:
            chunks = split_akkadian(raw_text)
            prefix = 'translate Akkadian to English: '
            chunk_translations = []
            
            for chunk in chunks:
                inputs = tokenizer(prefix + chunk, return_tensors='pt',
                                  max_length=MAX_LENGTH, truncation=True).to(device)
                if torch.cuda.is_available():
                    with autocast():
                        outputs = model.generate(
                            input_ids=inputs.input_ids,
                            attention_mask=inputs.attention_mask,
                            **gen_config_chunk
                        )
                else:
                    outputs = model.generate(
                        input_ids=inputs.input_ids,
                        attention_mask=inputs.attention_mask,
                        **gen_config_chunk
                    )
                translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
                chunk_translations.append(translation.strip())
            
            full_translation = ' '.join(chunk_translations)
            cleaned = postprocessor.postprocess_batch([full_translation])[0]
            results.append((sample_id, cleaned))
            chunked_ids.add(idx)

print(f"Chunked {len(chunked_ids)} long texts")
```

### 補足（Phase 1）

| 項目 | 内容 |
|------|------|
| CHUNK_THRESHOLD | 前処理ノートの定数（例: 50 語）。これを超える転写のみチャンキング対象 |
| split_akkadian | 節境界（KIŠIB, um-ma, a-na ... qí-bi 等）で分割。チャンク長は CHUNK_MIN_WORDS〜CHUNK_MAX_WORDS で制御 |
| gen_config_chunk | best_num_beams, best_length_penalty（Proven の 8 と 1.5）、max_new_tokens=512, early_stopping, use_cache |
| 流れ | 長文 → チャンク列 → 各チャンクを prefix 付きで tokenize → model.generate → デコード → 空白で結合 → postprocess → (sample_id, cleaned) を results に追加。chunked_ids に idx を記録 |
| 短い文 | 単語数 ≤ CHUNK_THRESHOLD の場合はこのループでは何もせず、Phase 2 で扱う |

### 実行結果（実例）

```
Phase 1: Translating long texts with clause-boundary chunking...
Chunked 0 long texts
```

- test が 4 件かついずれも単語数 ≤ CHUNK_THRESHOLD のため、長文としてチャンキングした件数は 0。`results` は空のまま Phase 2 に進む。本番で test が増え長文が含まれると、ここで 1 以上になる。

---

## PHASE 2: 短い文のバッチ翻訳（Adaptive beams）

- Phase 1 で処理しなかった**短い転写**（chunked_ids に含まれない idx）を、DataLoader でバッチ化して翻訳。**Adaptive beams**: バッチ内の入力長が 100 トークン未満なら num_beams=4（または best_num_beams//2）、100 以上なら best_num_beams（8）を使用。結果を `results` に追加し、Phase 1 と合わせて提出用リストを完成させる。

```python
# ============================================================
# PHASE 2: BATCH TRANSLATE SHORT TEXTS (exact match: chunky_v1_5_0)
# Adaptive beams: 4 for short (<100 tokens), 8 for long
# ============================================================

print("Phase 2: Batch translating remaining texts...")

if chunked_ids:
    short_indices = [i for i in range(len(test_dataset)) if i not in chunked_ids]
    short_dataset = torch.utils.data.Subset(test_dataset, short_indices)
else:
    short_dataset = test_dataset

if len(short_dataset) > 0:
    if len(short_dataset) >= NUM_BUCKETS:
        batch_sampler_short = BucketBatchSampler(short_dataset, BATCH_SIZE, NUM_BUCKETS)
        dataloader_short = DataLoader(
            short_dataset, batch_sampler=batch_sampler_short,
            collate_fn=collate_fn, num_workers=NUM_WORKERS, pin_memory=True,
            prefetch_factor=2, persistent_workers=True if NUM_WORKERS > 0 else False
        )
    else:
        dataloader_short = DataLoader(
            short_dataset, batch_size=BATCH_SIZE, shuffle=False,
            collate_fn=collate_fn, num_workers=NUM_WORKERS, pin_memory=True,
            prefetch_factor=2, persistent_workers=True if NUM_WORKERS > 0 else False
        )
    
    base_gen_config = {
        'max_new_tokens': 512,
        'length_penalty': best_length_penalty,
        'early_stopping': True,
        'use_cache': True,
    }
    
    with torch.inference_mode():
        for batch_idx, (batch_ids, tokenized) in enumerate(tqdm(dataloader_short, desc="Translating")):
            input_ids = tokenized.input_ids.to(device)
            attention_mask = tokenized.attention_mask.to(device)
            
            # Adaptive beams (exact match: chunky_v1_5_0)
            lengths = attention_mask.sum(dim=1)
            beam_sizes = torch.where(
                lengths < 100,
                torch.tensor(max(4, best_num_beams // 2)),
                torch.tensor(best_num_beams),
            )
            adaptive_beams = int(beam_sizes[0].item())
            
            gen_config = {**base_gen_config, 'num_beams': adaptive_beams}
            
            if torch.cuda.is_available():
                with autocast():
                    outputs = model.generate(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        **gen_config
                    )
            else:
                outputs = model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    **gen_config
                )
            
            translations = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            cleaned = postprocessor.postprocess_batch(translations)
            results.extend(zip(batch_ids, cleaned))
            
            if torch.cuda.is_available() and batch_idx % 10 == 0:
                torch.cuda.empty_cache()

print(f"\nTotal translations: {len(results)}")
if torch.cuda.is_available():
    torch.cuda.empty_cache()
```

### 補足（Phase 2）

| 項目 | 内容 |
|------|------|
| short_dataset | chunked_ids が空でなければ「Phase 1 で処理していない idx」だけの Subset、空なら test_dataset 全体。Phase 1 で 0 件のときは全 test がここで処理される |
| DataLoader | サンプル数 ≥ NUM_BUCKETS なら BucketBatchSampler で長さバケット、そうでなければ batch_size=BATCH_SIZE で shuffle=False。collate_fn で (ids, tokenized) |
| Adaptive beams | バッチ内の attention_mask の合計（トークン長）が 100 未満なら num_beams=max(4, best_num_beams//2)（=4）、100 以上なら best_num_beams（=8）。バッチ先頭の長さでバッチ全体の beams を決めている |
| 流れ | 各バッチで gen_config（num_beams を上記で設定）で model.generate → batch_decode → postprocess → (batch_ids, cleaned) を results に extend。10 バッチごとに empty_cache |
| 依存 | [[harukiharada_dataset_sampler_code_20260213000005|BucketBatchSampler]]、collate_fn、tqdm |
