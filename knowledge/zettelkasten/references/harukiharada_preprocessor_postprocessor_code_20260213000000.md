---
id: 20260213000001
title: harukiharada - 前処理・チャンキング・後処理 完全コード（chunky_v1_5_0）
author: takeikumi
type: reference
tags:
  - kaggle
  - machine-translation
  - deep-past
  - preprocessing
  - postprocessing
  - chunking
links:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
created: 2026-02-13
updated: 2026-02-13
---

# harukiharada - 前処理・チャンキング・後処理 完全コード（chunky_v1_5_0）

harukiharada 氏のノートブック「ByT5 + Optuna Tuning + Chunked Beam Search」で使用されている、前処理・アッカド語節境界チャンキング・後処理の**完全な実装**。バージョン表記はノートブック内の `chunky_v1_5_0` に準拠。

- **元ノート**: [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000]]
- **依存**: `re`, `pandas`, `List` (typing)

---

## コード

```python
# ============================================================
# PREPROCESSOR (exact match: chunky_v1_5_0)
# ============================================================

class OptimizedPreprocessor:
    def __init__(self):
        self.patterns = {
            'big_gap': re.compile(r'(\.{3,}|…+|……)'),
            'small_gap': re.compile(r'(xx+|\s+x\s+)'),
        }

    def preprocess_input_text(self, text: str) -> str:
        if pd.isna(text):
            return ""
        text = str(text)
        text = self.patterns['big_gap'].sub('<big_gap>', text)
        text = self.patterns['small_gap'].sub('<gap>', text)
        return text

    def preprocess_batch(self, texts: List[str]) -> List[str]:
        s = pd.Series(texts).fillna('').astype(str)
        s = s.str.replace(self.patterns['big_gap'], '<big_gap>', regex=True)
        s = s.str.replace(self.patterns['small_gap'], '<gap>', regex=True)
        return s.tolist()


# ============================================================
# AKKADIAN CLAUSE-BOUNDARY CHUNKING (exact match: chunky_v1_5_0)
# ============================================================

CHUNK_MIN_WORDS = 15
CHUNK_MAX_WORDS = 30
CHUNK_THRESHOLD = 50

CLAUSE_MARKERS = [
    r'KIŠIB\s+',
    r'IGI\s+',
    r'um-ma\s+',
    r'a-na\s+\S+\s+qí-bi',
    r'šu-ma\s+',
    r'\.\s+',
    r'\[\.\.\.\]\s*',
]
CLAUSE_PATTERN = re.compile('|'.join(CLAUSE_MARKERS), re.IGNORECASE)


def split_akkadian(text: str, max_words: int = CHUNK_MAX_WORDS, min_words: int = CHUNK_MIN_WORDS) -> List[str]:
    words = text.split()
    if len(words) <= CHUNK_THRESHOLD:
        return [text]

    chunks, current_chunk = [], []
    for word in words:
        current_chunk.append(word)
        chunk_text = ' '.join(current_chunk)
        chunk_len = len(current_chunk)
        is_break = bool(CLAUSE_PATTERN.search(chunk_text + ' '))

        if chunk_len >= min_words and is_break:
            chunks.append(chunk_text.strip())
            current_chunk = []
        elif chunk_len >= max_words:
            chunks.append(chunk_text.strip())
            current_chunk = []

    if current_chunk:
        last_chunk = ' '.join(current_chunk).strip()
        if last_chunk:
            chunks.append(last_chunk)

    return chunks if chunks else [text]


# ============================================================
# POSTPROCESSOR (exact match: chunky_v1_5_0)
# ============================================================

def remove_phrase_repeats(text: str) -> str:
    """Remove repeated phrases of 3-8 words using sliding window."""
    if not text:
        return text
    words = text.split()
    if len(words) < 6:
        return text
    for phrase_len in range(8, 2, -1):
        i = 0
        result_words = []
        while i < len(words):
            if i + phrase_len * 2 <= len(words):
                phrase = words[i:i + phrase_len]
                next_phrase = words[i + phrase_len:i + phrase_len * 2]
                if phrase == next_phrase:
                    result_words.extend(phrase)
                    j = i + phrase_len
                    while j + phrase_len <= len(words) and words[j:j + phrase_len] == phrase:
                        j += phrase_len
                    i = j
                    continue
            result_words.append(words[i])
            i += 1
        words = result_words
    return ' '.join(words)


def trim_trailing_fragment(text: str) -> str:
    """Trim trailing incomplete word or sentence fragment."""
    if not text:
        return text
    text = text.rstrip()
    if not text:
        return text
    if len(text) > 100 and text[-1].isalpha():
        for i in range(len(text) - 1, -1, -1):
            if text[i] in '.?!':
                return text[:i + 1]
            if text[i] in "'" and i > 0 and text[i - 1] in '.?!':
                return text[:i + 1]
    return text


class VectorizedPostprocessor:
    def __init__(self, aggressive: bool = True):
        self.aggressive = aggressive
        self.patterns = {
            'gap': re.compile(r'(\[x\]|\(x\)|\bx\b)', re.I),
            'big_gap': re.compile(r'(\.{3,}|…|\[\.+\])'),
            'annotations': re.compile(r'\((fem|plur|pl|sing|singular|plural|\?|!)\..\s*\w*\)', re.I),
            'repeated_words': re.compile(r'\b(\w+)(?:\s+\1\b)+'),
            'whitespace': re.compile(r'\s+'),
            'punct_space': re.compile(r'\s+([.,:])'),
            'repeated_punct': re.compile(r'([.,])\1+'),
        }
        self.subscript_trans = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')
        self.special_chars_trans = str.maketrans('ḫḪ', 'hH')
        self.forbidden_chars = '!?()"——<>⌈⌋⌊[]+ʾ/;'
        self.forbidden_trans = str.maketrans('', '', self.forbidden_chars)

    def postprocess_batch(self, translations: List[str]) -> List[str]:
        s = pd.Series(translations)
        valid_mask = s.apply(lambda x: isinstance(x, str) and x.strip())
        if not valid_mask.all():
            s[~valid_mask] = ''

        s = s.str.translate(self.special_chars_trans)
        s = s.str.translate(self.subscript_trans)
        s = s.str.replace(self.patterns['whitespace'], ' ', regex=True)
        s = s.str.strip()

        if self.aggressive:
            s = s.str.replace(self.patterns['gap'], '<gap>', regex=True)
            s = s.str.replace(self.patterns['big_gap'], '<big_gap>', regex=True)
            s = s.str.replace('<gap> <gap>', '<big_gap>', regex=False)
            s = s.str.replace('<big_gap> <big_gap>', '<big_gap>', regex=False)
            s = s.str.replace(self.patterns['annotations'], '', regex=True)

            s = s.str.replace('<gap>', '\x00GAP\x00', regex=False)
            s = s.str.replace('<big_gap>', '\x00BIG\x00', regex=False)
            s = s.str.translate(self.forbidden_trans)
            s = s.str.replace('\x00GAP\x00', ' <gap> ', regex=False)
            s = s.str.replace('\x00BIG\x00', ' <big_gap> ', regex=False)

            # Fractions (exact match: chunky_v1_5_0 — only ½, ¼, ¾)
            s = s.str.replace(r'(\d+)\.5\b', r'\1½', regex=True)
            s = s.str.replace(r'\b0\.5\b', '½', regex=True)
            s = s.str.replace(r'(\d+)\.25\b', r'\1¼', regex=True)
            s = s.str.replace(r'\b0\.25\b', '¼', regex=True)
            s = s.str.replace(r'(\d+)\.75\b', r'\1¾', regex=True)
            s = s.str.replace(r'\b0\.75\b', '¾', regex=True)

            # Remove repeated words/n-grams
            s = s.str.replace(self.patterns['repeated_words'], r'\1', regex=True)
            for n in range(4, 1, -1):
                pattern = r'\b((?:\w+\s+){' + str(n - 1) + r'}\w+)(?:\s+\1\b)+'
                s = s.str.replace(pattern, r'\1', regex=True)

            # Sliding-window phrase dedup
            s = s.apply(remove_phrase_repeats)

            s = s.str.replace(self.patterns['punct_space'], r'\1', regex=True)
            s = s.str.replace(self.patterns['repeated_punct'], r'\1', regex=True)
            s = s.str.replace(self.patterns['whitespace'], ' ', regex=True)
            s = s.str.strip().str.strip('-').str.strip()

            # Trim trailing incomplete fragments
            s = s.apply(trim_trailing_fragment)

        return s.tolist()


preprocessor = OptimizedPreprocessor()
postprocessor = VectorizedPostprocessor(aggressive=True)
print("Preprocessor and Postprocessor initialized (chunky_v1_5_0 exact match).")
```

---

## 関連ノート

- [[harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000|harukiharada ByT5 + Optuna + Chunked Beam Search リファレンス]]
