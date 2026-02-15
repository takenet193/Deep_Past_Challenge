---
id: 20260213000004
title: harukiharada - モデル読込 完全コード
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - byt5
  - bettertransformer
links:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - モデル読込 完全コード

harukiharada 氏のノートブック「ByT5 + Optuna Tuning + Chunked Beam Search」で使用されている、ByT5 モデル・トークナイザの読込と BetterTransformer 適用の**完全なコード**。

- **元ノート**: [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000]]
- **モデル**: Kaggle 入力 `/kaggle/input/final-byt5/byt5-akkadian-optimized-34x`（ByT5 アッカド語向けファインチューニング済み）

---

## コード

```python
MODEL_PATH = "/kaggle/input/final-byt5/byt5-akkadian-optimized-34x"

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device).eval()

num_params = sum(p.numel() for p in model.parameters())
print(f"Model loaded: {num_params:,} parameters on {device}")

# Apply BetterTransformer if available
try:
    from optimum.bettertransformer import BetterTransformer
    model = BetterTransformer.transform(model)
    print("BetterTransformer applied")
except Exception as e:
    print(f"BetterTransformer skipped: {e}")
```

---

## 補足

| 項目 | 内容 |
|------|------|
| MODEL_PATH | Kaggle の Add Data でマウントしたデータセット内のパス。ローカル再現時は `data/models/byt5-akkadian-optimized-34x` 等に置き換え |
| トークナイザ | `AutoTokenizer.from_pretrained(MODEL_PATH)` で同一ディレクトリから読込 |
| モデル | `AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)`（Seq2Seq 生成用） |
| デバイス | CUDA 利用可能なら `cuda`、そうでなければ `cpu`。`.to(device).eval()` で推論モードに |
| パラメータ数 | 全パラメータの `numel()` 合計を表示（ByT5-base 規模の目安確認用） |
| BetterTransformer | `optimum.bettertransformer` で推論を最適化。未インストール・エラー時はスキップし処理継続 |

---

## 実行時の出力（実例）

```
Loading model and tokenizer...
2026-02-08 11:39:57.488068: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:467] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
E0000 00:00:1770550797.678040      25 cuda_dnn.cc:8579] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered
E0000 00:00:1770550797.737655      25 cuda_blas.cc:1407] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered
W0000 00:00:1770550798.257134      25 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1770550798.257185      25 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1770550798.257189      25 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
W0000 00:00:1770550798.257192      25 computation_placer.cc:177] computation placer already registered. Please check linkage and avoid linking the same target more than once.
Model loaded: 581,653,248 parameters on cuda
BetterTransformer skipped: No module named 'optimum'
```

- **有効な結果**: `Model loaded: 581,653,248 parameters on cuda` → 約 5.8 億パラメータ（ByT5-base 規模）、CUDA でロード済み。
- **BetterTransformer**: `optimum` が未インストールのためスキップ。推論は通常の PyTorch で実行される。
- **cuFFT / cuDNN / cuBLAS / computation placer のメッセージ**: XLA まわりの重複登録警告。動作には影響せず無視してよい。
