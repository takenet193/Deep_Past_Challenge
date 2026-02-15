---
id: 20260213000005
title: harukiharada - Dataset と BucketBatchSampler 完全コード
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - pytorch
  - dataset
  - sampler
links:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
  - harukiharada_preprocessor_postprocessor_code_20260213000000
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - Dataset と BucketBatchSampler 完全コード

harukiharada 氏のノートブック「ByT5 + Optuna Tuning + Chunked Beam Search」で使用されている、PyTorch 用の **AkkadianDataset** と **BucketBatchSampler** の**完全なコード**。

- **元ノート**: [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000]]
- **前処理**: [[harukiharada_preprocessor_postprocessor_code_20260213000000]] の `OptimizedPreprocessor` をコンストラクタで受け取り、転写をプレフィックス付きで返す

---

## コード

```python
class AkkadianDataset(Dataset):
    def __init__(self, dataframe: pd.DataFrame, preprocessor):
        if 'id' in dataframe.columns:
            self.sample_ids = dataframe['id'].tolist()
        else:
            self.sample_ids = list(range(len(dataframe)))
        raw_texts = dataframe['transliteration'].tolist()
        preprocessed = preprocessor.preprocess_batch(raw_texts)
        self.input_texts = ['translate Akkadian to English: ' + t for t in preprocessed]
        print(f"Dataset created: {len(self.sample_ids)} samples")
    
    def __len__(self):
        return len(self.sample_ids)
    
    def __getitem__(self, index):
        return self.sample_ids[index], self.input_texts[index]


class BucketBatchSampler(Sampler):
    def __init__(self, dataset, batch_size: int, num_buckets: int = 4):
        lengths = [len(text.split()) for _, text in dataset]
        sorted_indices = sorted(range(len(lengths)), key=lambda i: lengths[i])
        bucket_size = max(1, len(sorted_indices) // num_buckets)
        self.buckets = []
        for i in range(num_buckets):
            start = i * bucket_size
            end = None if i == num_buckets - 1 else (i + 1) * bucket_size
            self.buckets.append(sorted_indices[start:end])
        self.batch_size = batch_size
    
    def __iter__(self):
        for bucket in self.buckets:
            for i in range(0, len(bucket), self.batch_size):
                yield bucket[i:i + self.batch_size]
    
    def __len__(self):
        return sum((len(b) + self.batch_size - 1) // self.batch_size for b in self.buckets)

print("Dataset and Sampler classes ready.")
```

---

## 補足

### AkkadianDataset

| 項目 | 内容 |
|------|------|
| 入力 | `dataframe`: `transliteration` 列（および任意で `id` 列）を持つ DataFrame。`preprocessor`: `preprocess_batch(texts)` を持つ前処理オブジェクト |
| sample_ids | `id` 列があればその値のリスト、なければ 0..len-1 のインデックス |
| 前処理 | `preprocessor.preprocess_batch(raw_texts)` で転写を一括正規化（欠損マーカー等） |
| プレフィックス | 各転写に `'translate Akkadian to English: ' + t` を付与（ByT5 のタスク指定） |
| __getitem__ | `(sample_id, input_text)` のタプルを返す。DataLoader でバッチ化する想定 |

### BucketBatchSampler

| 項目 | 内容 |
|------|------|
| 目的 | 長さの近いサンプルを同じバッチにまとめ、パディング量を減らして効率化 |
| lengths | データセット各要素の 2 番目（テキスト）を `text.split()` で単語数に |
| ソート | 単語数で昇順ソートしたインデックスを `num_buckets` 個のバケットに均等分割 |
| __iter__ | バケットごとに `batch_size` ずつインデックスのリストを yield（Sampler のためインデックスのリストを返す） |
| 依存 | `dataset` は `(id, text)` を返すイテラブルである必要がある（`AkkadianDataset` と組み合わせて使用） |

### DataLoader での利用例

- `DataLoader(dataset, batch_sampler=BucketBatchSampler(dataset, batch_size=..., num_buckets=4))` のように `batch_sampler` に渡す。`batch_size` は Sampler 側で指定するため、DataLoader には `batch_size=` を渡さない。
