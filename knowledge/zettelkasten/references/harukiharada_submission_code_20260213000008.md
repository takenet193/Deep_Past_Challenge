---
id: 20260213000008
title: harukiharada - 提出（Submission）完全コード
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - submission
  - byt5
links:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
  - harukiharada_inference_chunked_beam_search_code_20260213000007
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - 提出（Submission）完全コード

harukiharada 氏のノートブック「ByT5 + Optuna Tuning + Chunked Beam Search」の**提出用 CSV の組み立てと保存**。Phase 1・Phase 2 で得た `results`（(id, translation) のリスト）を DataFrame 化し、検証したうえで `submission.csv` に出力する。

- **元ノート**: [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000]]
- **前提**: [[harukiharada_inference_chunked_beam_search_code_20260213000007|本番推論・Chunked Beam Search]] の Phase 1・Phase 2 が完了し、`results` に全 test の (id, translation) が入っていること。

---

## コード

```python
# Build submission
submission = pd.DataFrame(results, columns=['id', 'translation'])
submission = submission.sort_values('id').reset_index(drop=True)

# Validation checks
assert len(submission) == len(df_test), f"Expected {len(df_test)} rows, got {len(submission)}"
empty_count = submission['translation'].str.strip().eq('').sum()
print(f"Submission shape: {submission.shape}")
print(f"Empty translations: {empty_count}")
print(f"Translation length range: [{submission['translation'].str.len().min()}, {submission['translation'].str.len().max()}]")

submission.to_csv('submission.csv', index=False)
print(f"\nSaved submission.csv")
submission.head(10)
```

---

## 補足

| 項目 | 内容 |
|------|------|
| results | Phase 1 と Phase 2 で蓄えた (sample_id, translation) のリスト。全 test 分が 1 件ずつ入っている想定 |
| DataFrame | 列は `id`, `translation`。コンペの提出形式に合わせる |
| sort_values('id') | 提出用に id で昇順ソート。評価側で id と照合するため順序を揃える |
| assert | 行数が df_test と一致することを確認。不足・重複があればここで失敗する |
| empty_count | 訳文が空白のみの行数。0 であることが望ましい |
| Translation length range | 各訳文の文字数の min/max。空や異常に短い訳の有無を確認する用 |
| to_csv | `submission.csv` に index なしで保存。Kaggle ではこのファイルを提出する |
