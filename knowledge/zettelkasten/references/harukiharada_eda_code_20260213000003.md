---
id: 20260213000003
title: harukiharada - EDA 完全コード
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - eda
links:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - EDA 完全コード

harukiharada 氏のノートブック「ByT5 + Optuna Tuning + Chunked Beam Search」で使用されている、データ読込・基本確認・欠損・長さ統計・可視化・Gap 分析・頻出語・サンプル表示・外れ値分析の**完全なコード**。

- **元ノート**: [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000]]
- **前提**: `df_train`, `df_test` は未定義の場合は先に train.csv / test.csv を読んでおく。長さ・Gap などの列は本コード内で作成される。

---

## 1. データ読込・基本確認

```python
df_train = pd.read_csv("/kaggle/input/deep-past-initiative-machine-translation/train.csv")
df_test = pd.read_csv("/kaggle/input/deep-past-initiative-machine-translation/test.csv")

print("- The train set's shape is", df_train.shape[0], "rows and", df_train.shape[1], "columns.")
print("- The test set's shape is", df_test.shape[0], "rows and", df_test.shape[1], "columns.")
df_train.head()
```

## 2. 欠損・重複の確認

```python
print('Missing values per column:')
print(df_train.isnull().sum(), '\n')
print('Duplicate count:', df_train.duplicated().sum(), '\n')
```

## 3. テキスト長（単語数・文字数）の計算

```python
df_train['src_word_count'] = df_train['transliteration'].fillna('').apply(lambda x: len(x.split()))
df_train['tgt_word_count'] = df_train['translation'].fillna('').apply(lambda x: len(x.split()))
df_train['src_char_count'] = df_train['transliteration'].fillna('').str.len()
df_train['tgt_char_count'] = df_train['translation'].fillna('').str.len()
df_test['src_word_count'] = df_test['transliteration'].fillna('').apply(lambda x: len(x.split()))
df_test['src_char_count'] = df_test['transliteration'].fillna('').str.len()

print("Source (transliteration) word count stats:")
print(df_train['src_word_count'].describe())
print("\nTarget (translation) word count stats:")
print(df_train['tgt_word_count'].describe())
```

## 4. 長さ分布の可視化（2×2 ヒストグラム）

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0, 0].hist(df_train['src_word_count'], bins=50, color='#8b6914', alpha=0.7, edgecolor='#2c1810')
axes[0, 0].axvline(df_train['src_word_count'].mean(), color='#d4a843', linestyle='--', linewidth=2, label=f"Mean: {df_train['src_word_count'].mean():.1f}")
axes[0, 0].axvline(df_train['src_word_count'].median(), color='#f0d68a', linestyle='-.', linewidth=2, label=f"Median: {df_train['src_word_count'].median():.1f}")
axes[0, 0].set_title('Source (Transliteration) Word Count', fontweight='bold')
axes[0, 0].legend()

axes[0, 1].hist(df_train['tgt_word_count'], bins=50, color='#5c4a2a', alpha=0.7, edgecolor='#2c1810')
axes[0, 1].axvline(df_train['tgt_word_count'].mean(), color='#d4a843', linestyle='--', linewidth=2, label=f"Mean: {df_train['tgt_word_count'].mean():.1f}")
axes[0, 1].axvline(df_train['tgt_word_count'].median(), color='#f0d68a', linestyle='-.', linewidth=2, label=f"Median: {df_train['tgt_word_count'].median():.1f}")
axes[0, 1].set_title('Target (Translation) Word Count', fontweight='bold')
axes[0, 1].legend()

axes[1, 0].hist(df_train['src_char_count'], bins=50, color='#8b6914', alpha=0.7, edgecolor='#2c1810')
axes[1, 0].set_title('Source Character Count', fontweight='bold')

axes[1, 1].hist(df_train['tgt_char_count'], bins=50, color='#5c4a2a', alpha=0.7, edgecolor='#2c1810')
axes[1, 1].set_title('Target Character Count', fontweight='bold')

plt.tight_layout()
plt.show()
```

## 5. Train vs Test の分布比較（KDE）

```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.kdeplot(df_train['src_word_count'], ax=axes[0], label='Train', fill=True, alpha=0.5, color='#8b6914')
sns.kdeplot(df_test['src_word_count'], ax=axes[0], label='Test', fill=True, alpha=0.3, color='#d4a843')
axes[0].set_title('Source Word Count: Train vs Test')
axes[0].legend()

sns.kdeplot(df_train['src_char_count'], ax=axes[1], label='Train', fill=True, alpha=0.5, color='#8b6914')
sns.kdeplot(df_test['src_char_count'], ax=axes[1], label='Test', fill=True, alpha=0.3, color='#d4a843')
axes[1].set_title('Source Char Count: Train vs Test')
axes[1].legend()

plt.tight_layout()
plt.show()
```

## 6. 転写 vs 翻訳の長さ関係（散布図・トレンド線・相関）

```python
plt.figure(figsize=(10, 6))
plt.scatter(df_train['src_word_count'], df_train['tgt_word_count'], alpha=0.3, color='#8b6914', s=10)
plt.xlabel('Source Word Count (Transliteration)')
plt.ylabel('Target Word Count (Translation)')
plt.title('Source vs Target Length Relationship')

z = np.polyfit(df_train['src_word_count'], df_train['tgt_word_count'], 1)
p = np.poly1d(z)
x_line = np.linspace(0, df_train['src_word_count'].max(), 100)
plt.plot(x_line, p(x_line), color='#d4a843', linewidth=2, linestyle='--', label=f'Trend: y={z[0]:.2f}x + {z[1]:.2f}')
plt.legend()
plt.tight_layout()
plt.show()

print(f"Correlation between source and target word counts: {df_train['src_word_count'].corr(df_train['tgt_word_count']):.3f}")
```

## 7. 欠損マーカー（Gap）の分析

```python
df_train['has_gap'] = df_train['transliteration'].fillna('').str.contains(r'\bx\b|xx|\.\.\.|…', regex=True)
df_test['has_gap'] = df_test['transliteration'].fillna('').str.contains(r'\bx\b|xx|\.\.\.|…', regex=True)

print(f"Train texts with gaps: {df_train['has_gap'].sum()} ({df_train['has_gap'].mean()*100:.1f}%)")
print(f"Test texts with gaps:  {df_test['has_gap'].sum()} ({df_test['has_gap'].mean()*100:.1f}%)")

df_train['gap_count'] = df_train['transliteration'].fillna('').apply(
    lambda x: len(re.findall(r'\bx\b|xx+|\.\.\.|…', x))
)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
counts = df_train['has_gap'].value_counts()
labels = ['No Gaps', 'Has Gaps']
colors = ['#8b6914', '#d4a843']
axes[0].pie(counts, labels=labels, colors=colors, autopct='%1.1f%%',
            textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[0].set_title('Gap Marker Presence in Train', fontweight='bold')

axes[1].hist(df_train[df_train['gap_count'] > 0]['gap_count'], bins=30,
             color='#8b6914', alpha=0.7, edgecolor='#2c1810')
axes[1].set_title('Gap Count Distribution (texts with gaps)', fontweight='bold')
axes[1].set_xlabel('Number of Gap Markers')

plt.tight_layout()
plt.show()
```

## 8. 翻訳側の頻出語（Top 30）

```python
all_target_words = ' '.join(df_train['translation'].fillna('')).lower().split()
word_counts = Counter(all_target_words)
top_30 = word_counts.most_common(30)

plt.figure(figsize=(14, 6))
words, counts_list = zip(*top_30)
plt.bar(words, counts_list, color='#8b6914', edgecolor='#2c1810')
plt.xticks(rotation=45, ha='right')
plt.title('Top 30 Most Common Words in English Translations', fontweight='bold')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
```

## 9. サンプル表示（転写・翻訳の先頭 200 文字）

```python
sample = df_train.sample(5, random_state=42)
for idx, row in sample.iterrows():
    print("=" * 70)
    print(f"Index: {idx}")
    print(f"SRC: {row['transliteration'][:200]}")
    print(f"TGT: {row['translation'][:200]}")
print("=" * 70)
```

## 10. 外れ値分析（IQR 法）と長さ比

```python
for col in ['src_word_count', 'tgt_word_count']:
    Q1 = df_train[col].quantile(0.25)
    Q3 = df_train[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df_train[(df_train[col] < lower_bound) | (df_train[col] > upper_bound)]
    print(f"{col}: Lower={lower_bound:.0f}, Upper={upper_bound:.0f}, Outliers={outliers.shape[0]}")

df_train['length_ratio'] = df_train['tgt_word_count'] / df_train['src_word_count'].clip(lower=1)
print(f"\nLength ratio (target/source) stats:")
print(df_train['length_ratio'].describe())
```

---

## 関連ノート

- [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000|harukiharada ByT5 + Optuna + Chunked Beam Search リファレンス]]
- [[deep_past_eda_results_20260211140000|Deep Past EDA 結果]]（当プロジェクトの EDA との比較用）
