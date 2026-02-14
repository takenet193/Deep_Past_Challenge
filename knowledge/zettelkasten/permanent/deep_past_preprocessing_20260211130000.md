---
id: 20260211130000
title: Deep Past Challenge - 前処理ガイド（実データ確認済み）
author: takeikumi
type: permanent
tags:
  - kaggle
  - machine-translation
  - deep-past
  - data
  - preprocessing
links:
  - deep_past_dataset_overview_20260211121000
  - deep_past_competition_overview_structure_20260210110000
  - deep_past_competition_evaluation_submission_20260210130000
created: 2026-02-11
updated: 2026-02-11
---

# Deep Past Challenge - 前処理ガイド（実データ確認済み）

公式 Dataset Instructions と実データ（`train.csv`, `test.csv`）を突き合わせて整理した、前処理の実践ガイド。

## 1. 最重要：train と test の粒度の違い

| | train.csv | test.csv |
|---|---|---|
| 粒度 | **文書単位**（1行 = 粘土板まるごと） | **文単位**（1行 = 数行分の文） |
| 件数 | 約 1,561 件 | ダミー 4 件（本番 約 4,000 文 / 約 400 文書） |
| 翻訳 | あり | なし（これを予測する） |

### 対処

- `Sentences_Oare_FirstWord_LinNum.csv` を使い、**train を文単位に分割してから学習する**のが基本方針。
  - このファイルには `text_uuid`（≒ oare_id）、`sentence_uuid`、`translation`（文単位の英訳）、`first_word_spelling`、`line_number` が含まれる。
  - train の文書テキストを、この情報をキーにして文単位にスライスできる。
- 文書単位のまま学習すると、test の文単位出力と粒度が合わず、スコアが伸びにくい。

## 2. 転写テキスト（transliteration）の前処理

### 2.1 必須（優先度：高）

#### Ḫ/ḫ → H/h の置換

- **理由**: 公式明言「test data has only H h」。train には `Ḫ ḫ` が残っている。
- **実例**: `ḫa-muš-tim` → `ha-muš-tim`, `Ḫa-nu-ú` → `Ha-nu-ú`
- アッカド語に H は 1 種類しかないため、単純置換で OK。

#### 書記記号の除去

公式推奨の除去対象：

| 記号 | 意味 | 処理 |
|---|---|---|
| `!` | 確実な読解 | 除去 |
| `?` | 不確実な読解 | 除去 |
| `/` | 行の継ぎ目 | 除去 |
| `:` or `.` | 語区切り（注意: `:` は `KÙ.BABBAR` の `.` と区別） | 語区切りの `:` のみ除去 |
| `< >` | 書記の挿入。**括弧だけ除去し、中身は残す** | `<abc>` → `abc` |
| `<< >>` | 誤字マーク。**括弧ごと除去** | `<<abc>>` → 除去 |
| `˹ ˺` | 部分欠損マーク | 除去（転写テキストから） |
| `[ ]` | 明らかな欠損。**括弧だけ除去し、中身は残す** | `[KÙ.BABBAR]` → `KÙ.BABBAR` |

#### determinatives の統一

- 実データでは `(d)IM`, `(ki)`, `a-lim(ki)` のように**丸括弧**表記が混在。
- 公式は `{d}`, `{ki}` のように**波括弧**を推奨。
- train / test 間で表記を統一する。

### 2.2 推奨（優先度：中）

#### 欠損・ブレイクの統一

| パターン | 置換先 |
|---|---|
| `[x]` | `<gap>`（1文字の欠損） |
| `…` | `<big_gap>`（大きな欠損） |
| `[… …]` | `<big_gap>` |

- 実データで `[...]`, `…`, `[x]` が実際に出現することを確認済み。

#### 下付き数字の正規化

- `il₅` → `il5`, `qí-bi₄-ma` → `qí-bi4-ma` のように ASCII 化。
- 下付き Unicode（₀-₉, ₓ）を通常の数字に変換。
- **注意**: シュメログラム内の下付き（`SIG₅` など）も対象。

### 2.3 検討（優先度：低）

#### アクセント付き母音

| CDLI | ORACC | 意味 |
|---|---|---|
| `á` | `a2` / `a₂` | 母音の第2形 |
| `à` | `a3` / `a₃` | 母音の第3形 |
| 同様に `é è í ì ú ù` | | |

- train と test で表記が統一されているなら、そのまま残しても問題ない。
- 統一されていない場合は、ORACC 形式（`a2` など）か CDLI 形式（`á` など）のどちらかに揃える。

## 3. 翻訳テキスト（translation）の前処理

### 3.1 引用符の正規化

- train の翻訳に `"""` のような多重引用符が出現。
- 提出時に余計な引用符が混ざると n-gram が狂う可能性がある。
- 最低限、引用符のスタイルを統一（例: すべて `"` に）。

### 3.2 固有名詞

- 翻訳でも固有名詞が多い（`Šalim-Aššur`, `Kanesh` など）。
- 公式辞書 `OA_Lexicon_eBL.csv` に固有名詞の正規化形があるので、これをルックアップテーブルとして利用できる。
- 固有名詞は BLEU / chrF++ の両方でスコアに直結するため、**参照と同じ表記にする**ことが重要。

### 3.3 `...`（欠損部分）

- 翻訳側でも転写が壊れている箇所は `...` と省略されている。
- 実例: `... he did not give you a textile.`

## 4. 実データで確認した具体例

### 転写の例

```
KIŠIB ma-nu-ba-lúm-a-šur DUMU ṣí-lá-(d)IM KIŠIB šu-(d)EN.LÍL
```

- `KIŠIB`: シュメログラム（全大文字）
- `ma-nu-ba-lúm-a-šur`: ハイフン区切りの音節（固有名詞、頭大文字なし）
- `(d)IM`: determinative `{d}` + シュメログラム `IM`（= 神 Adad）
- `DUMU`: シュメログラム（= son）

### 翻訳の例

```
Seal of Mannum-balum-Aššur son of Ṣilli-Adad, seal of Šu-Illil son of Mannum-kī-Aššur
```

- 固有名詞がそのまま音写で残る（`Aššur`, `Ṣilli-Adad`）
- 英語と混在する形式

## 5. 前処理チェックリスト（優先度順）

- [ ] **train の文単位分割**（`Sentences_Oare_FirstWord_LinNum.csv` 利用）
- [ ] **Ḫ/ḫ → H/h** 置換
- [ ] **書記記号の除去**（`! ? / : < > ˹ ˺ [ ]`）
- [ ] **determinatives の統一**（`(d)` → `{d}` など）
- [ ] **欠損マーカーの統一**（`[x]` → `<gap>`, `…` → `<big_gap>`）
- [ ] **下付き数字の ASCII 化**（`₅` → `5` など）
- [ ] **翻訳の引用符正規化**
- [ ] **アクセント付き母音の統一**（必要に応じて）

## 関連ノート

- [[deep_past_dataset_overview_20260211121000|データセット概要と前処理ガイド]]
- [[deep_past_competition_overview_structure_20260210110000|コンペ概要ストラクチャーノート]]
- [[deep_past_competition_evaluation_submission_20260210130000|評価と提出方法]]
- [[evaluation_strategy_geometric_mean_20260211120000|評価指標（幾何平均）を伸ばす戦略]]
- [[akkadian_mt_preprocessing_ensemble_reference_20260211130000|Akkadian MT 前処理 & アンサンブル実装リファレンス]]