---
id: 20260213000002
title: harukiharada - ライブラリ・インポート・評価指標フォールバック 完全コード
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - metrics
  - sacrebleu
  - optuna
links:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - ライブラリ・インポート・評価指標フォールバック 完全コード

harukiharada 氏のノートブック「ByT5 + Optuna Tuning + Chunked Beam Search」の冒頭で使用されている、環境変数・インポート・sacrebleu フォールバック（BLEU / chrF++ 純 Python 実装）・Optuna の**完全なコード**。

- **元ノート**: [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000]]
- **用途**: Kaggle 本番（インターネットオフ）でも sacrebleu が使えない場合に、純 Python で BLEU / chrF++ を計算

---

## コード

```python
import warnings
warnings.filterwarnings("ignore")

import os
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["CUDA_LAUNCH_BLOCKING"] = "0"
os.environ["TORCH_CUDNN_V8_API_ENABLED"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "true"

import re
import random
import math
from pathlib import Path
from typing import List
from collections import Counter
from dataclasses import dataclass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

banner_palette = [
    "#2c1810",  # dark brown
    "#5c4a2a",  # medium brown
    "#8b6914",  # golden brown
    "#d4a843",  # gold
    "#f0d68a"   # light gold
]
sns.set_palette(banner_palette)

import torch
from torch.utils.data import Dataset, DataLoader, Sampler
from torch.cuda.amp import autocast
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm.auto import tqdm

# ============================================================
# METRICS: sacrebleu with pure-Python fallback
# ============================================================
USE_SACREBLEU = False
try:
    import sacrebleu
    USE_SACREBLEU = True
    print("sacrebleu loaded")
except ImportError:
    try:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sacrebleu", "-q"])
        import sacrebleu
        USE_SACREBLEU = True
        print("sacrebleu installed and loaded")
    except Exception:
        print("sacrebleu unavailable — using built-in BLEU/chrF++ implementation")


def _ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def _corpus_bleu_fallback(hypotheses, references, max_n=4):
    """Simplified corpus BLEU (no smoothing, brevity penalty included)."""
    clip_counts = [0] * max_n
    total_counts = [0] * max_n
    hyp_len = 0
    ref_len = 0
    for hyp, ref in zip(hypotheses, references):
        hyp_tok = hyp.split()
        ref_tok = ref.split()
        hyp_len += len(hyp_tok)
        ref_len += len(ref_tok)
        for n in range(1, max_n + 1):
            hyp_ng = Counter(_ngrams(hyp_tok, n))
            ref_ng = Counter(_ngrams(ref_tok, n))
            clipped = {ng: min(c, ref_ng.get(ng, 0)) for ng, c in hyp_ng.items()}
            clip_counts[n-1] += sum(clipped.values())
            total_counts[n-1] += max(len(hyp_tok) - n + 1, 0)
    precisions = []
    for n in range(max_n):
        if total_counts[n] == 0:
            precisions.append(0)
        else:
            precisions.append(clip_counts[n] / total_counts[n])
    if any(p == 0 for p in precisions):
        return 0.0
    log_avg = sum(math.log(p) for p in precisions) / max_n
    bp = 1.0 if hyp_len >= ref_len else math.exp(1 - ref_len / max(hyp_len, 1))
    return bp * math.exp(log_avg) * 100


def _chrf_pp_fallback(hypotheses, references, n_char=6, n_word=2, beta=2):
    """Simplified chrF++ (character n-gram F-score + word n-grams)."""
    total_hyp_ngrams = 0
    total_ref_ngrams = 0
    total_matches = 0
    for hyp, ref in zip(hypotheses, references):
        for n in range(1, n_char + 1):
            hyp_ng = Counter(_ngrams(list(hyp), n))
            ref_ng = Counter(_ngrams(list(ref), n))
            matches = sum(min(hyp_ng[ng], ref_ng[ng]) for ng in hyp_ng if ng in ref_ng)
            total_matches += matches
            total_hyp_ngrams += sum(hyp_ng.values())
            total_ref_ngrams += sum(ref_ng.values())
        for n in range(1, n_word + 1):
            hyp_ng = Counter(_ngrams(hyp.split(), n))
            ref_ng = Counter(_ngrams(ref.split(), n))
            matches = sum(min(hyp_ng[ng], ref_ng[ng]) for ng in hyp_ng if ng in ref_ng)
            total_matches += matches
            total_hyp_ngrams += sum(hyp_ng.values())
            total_ref_ngrams += sum(ref_ng.values())
    precision = total_matches / max(total_hyp_ngrams, 1)
    recall = total_matches / max(total_ref_ngrams, 1)
    if precision + recall == 0:
        return 0.0
    beta_sq = beta ** 2
    f_score = (1 + beta_sq) * precision * recall / (beta_sq * precision + recall)
    return f_score * 100


def _sentence_bleu_fallback(hypothesis, reference, max_n=4):
    """Sentence-level BLEU with add-1 smoothing."""
    hyp_tok = hypothesis.split()
    ref_tok = reference.split()
    precisions = []
    for n in range(1, max_n + 1):
        hyp_ng = Counter(_ngrams(hyp_tok, n))
        ref_ng = Counter(_ngrams(ref_tok, n))
        clipped = sum(min(c, ref_ng.get(ng, 0)) for ng, c in hyp_ng.items())
        total = max(len(hyp_tok) - n + 1, 0)
        precisions.append((clipped + 1) / (total + 1))  # add-1 smoothing
    log_avg = sum(math.log(p) for p in precisions) / max_n
    bp = 1.0 if len(hyp_tok) >= len(ref_tok) else math.exp(1 - len(ref_tok) / max(len(hyp_tok), 1))
    return bp * math.exp(log_avg) * 100


# optuna: try import, fallback to pip install
try:
    import optuna
    print("optuna loaded")
except ImportError:
    try:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "optuna", "-q"])
        import optuna
        print("optuna installed and loaded")
    except Exception:
        raise ImportError("optuna is required but could not be installed. Enable internet or pre-install optuna.")

print(f"\nPyTorch: {torch.__version__} | CUDA: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)} | {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
```

---

## 関連ノート

- [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000|harukiharada ByT5 + Optuna + Chunked Beam Search リファレンス]]
