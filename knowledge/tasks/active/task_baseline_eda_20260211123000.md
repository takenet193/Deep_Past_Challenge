---
type: task
id: task-20260211123000
title: ベースライン用 EDA を行う
author: takeikumi
status: completed
priority: high
project: baseline
mode: research
due_date: null
context: []
tags:
  - baseline
  - kaggle
  - data
  - eda
related_notes:
  - deep_past_dataset_overview_20260211121000
  - deep_past_eda_results_20260211140000
assignee: null
assigned_agent: null
dependencies:
  - task-20260210100002  # データダウンロード完了
created: 2026-02-11
updated: 2026-02-11
---
t

# タスク: ベースライン用 EDA を行う

## 目的

Deep Past Challenge のデータ構造と前処理上の特徴を、実データに基づいて把握する。ベースライン実装で最初に採用する前処理・特徴量・モデル設計の方針を決めるための土台を作る。

## どんな EDA をするか（検討メモ）

### 1. 基本構造の把握

- [x] `train.csv` / `test.csv` / `sample_submission.csv` の **件数・カラム・NULL の有無** を確認する。
- [x] `published_texts.csv` / `OA_Lexicon_eBL.csv` など、追加データ系の **レコード数と主キー（ID）の関係** をざっくり見る。

### 2. 長さ・分布の確認

- [x] `train.transliteration` と `train.translation` について、
  - 文字数 / 単語数の分布（平均・中央値・95パーセンタイルなど）
  - 文書ごとの行数（`Sentences_Oare_FirstWord_LinNum.csv` も活用）
  を確認し、
  - **極端に長いサンプルの割合**
  - **転写と訳の長さ比（length ratio）** のざっくりした範囲
  を把握する。
- [x] `test.transliteration` の長さ分布を `train` と比較し、
  - 「train をそのまま文レベルデータにしてもテストと分布が大きくズレないか」を確認する。

### 3. 記号・表記の出現状況

- [x] 転写テキストにおける、以下の記号類の頻度を確認する。
  - `{}`（決定詞）
  - `[]`, `<>`, `…`, `<gap>`, `<big_gap>`（欠損・挿入）
  - `!`, `?`, `/`, `:`, `.`（現代書記記号）
  - 上付き数字や特殊文字（`₀-₉`, `Ḫ`, `š`, `ṣ`, `ṭ` など）
- [x] 決定詞 `{...}` の具体的な中身（`{d}`, `{ki}`, `{m}`, `{mi}`, `{geš}`, ...）の頻度表を作る。
  - → `{PN}`, `{GN}`, `{DN}` などへの **カテゴリー正規化** を検討する際の材料にする。

### 4. 語彙・辞書情報との関係

- [x] `OA_Lexicon_eBL.csv` の `form` と `train.transliteration` の単語を突き合わせ、
  - どの程度カバーされているか（coverage）
  - 固有名詞（`type=PN/GN` など）の割合
  をざっくり見る。
- [x] ロゴグラム（全大文字＋ドット区切り、例: `KÙ.BABBAR`）の頻度リストを作り、
  - 代表的なもの（銀、金、都市名など）がどの程度出るかを把握する。

### 5. 英訳側の特徴

- [x] `train.translation` について、
  - 文長分布（単語数）
  - 大文字開始のトークン（固有名詞）頻度
  - 記号（`, . : ; ? !` など）の頻度
  を見て、
  - **翻訳のスタイル（文語的 / 注釈多め / 数値表現の仕方など）** を掴む。

### 6. ベースライン実装へのフィードバック

- [x] EDA の結果を踏まえて、以下を決める材料にする。
  - 前処理ポリシーのたたき台:
    - どの記号を「必ず削るか」
    - どの情報（決定詞、ロゴグラムなど）を「タグとして残すか」
  - 長さ制御の方針:
    - 典型的な長さ範囲に応じて、モデル入力長・デコード時の長さ制約をどう設定するか
  - 追加データ活用の優先度:
    - `published_texts` / `publications` をすぐ使うか、まず `train` だけでベースラインを作るか

## 結果（実施報告）/ 学び / 次のアクション

### 結果

`scripts/baseline_eda.py` を作成し、以下の分析を実施した：

1. **基本構造**: train 1,561 件（文書単位）、Sentences ファイルで 9,782 文に分割可能
2. **長さ分布**: 転写平均 57.5 語、翻訳平均 90.5 語、length ratio 約 1.47
3. **記号**: train は既にクリーン（`!`, `?`, `/`, `:` はゼロ）、determinatives は `()` 表記（33.8%）
4. **語彙**: カバレッジ 69.8%（11,761 語中 8,205 語が辞書と一致）
5. **翻訳**: 対話形式（引用符 25.2%）、注釈多め（括弧 35.9%）、欠損多め（省略記号 39.9%）

詳細は [[deep_past_eda_results_20260211140000|EDA 結果ノート]] に記載。

**成果物**:
- `scripts/baseline_eda.py`: 実行可能な EDA スクリプト
- `results/eda_output.txt`: 分析結果の標準出力
- `results/figures/`: 長さ分布・相関・箱ひげ図の可視化（PNG 3 枚）
- `knowledge/zettelkasten/permanent/deep_past_eda_results_20260211140000.md`: EDA 結果の永続ノート

### 学び

1. **train と test の粒度が異なる重要性を再確認**: train は文書単位（平均 57.5 語）、test は文単位（推定 13 語程度）
   - `Sentences_Oare_FirstWord_LinNum.csv` で train を文単位に分割する必要がある
   
2. **前処理の優先度が明確になった**:
   - 必須: Ḫ/ḫ → H/h（4,935 回出現）、determinatives の統一、文単位分割
   - 推奨: 欠損マーカーの処理、下付き数字の ASCII 化
   - 低優先度: 翻訳の引用符・括弧正規化

3. **語彙カバレッジは 70% 程度**: 残り 30% は辞書にない語（新造語、誤記、書記の変形など）
   - カバーされていない語への対処（BPE、byte-level tokenization など）が重要

4. **長さ制御の目安**:
   - 文書単位ベースライン: 入力 150 トークン、出力 300 トークン
   - 文単位ベースライン: 入力 50 トークン、出力 75 トークン

5. **翻訳のスタイル特徴**:
   - 対話形式が多い（引用符 25.2%）
   - 注釈・補足が多い（括弧 35.9%）
   - 欠損部分が多い（省略記号 39.9%）
   - → モデルは引用符・括弧・省略記号の使い方を学習する必要がある

### 次のアクション

1. **前処理実装** (優先度: 高):
   - Ḫ/ḫ → H/h の置換スクリプト
   - determinatives の統一（丸括弧 → 波括弧 or そのまま）
   - `Sentences_Oare_FirstWord_LinNum.csv` を使った train の文単位分割

2. **ベースライン設計** (優先度: 高):
   - まず train.csv の文単位データ（9,782 文）でベースラインを構築
   - モデル候補: mBART, mT5, Helsinki-NLP MarianMT など

3. **追加データ活用** (優先度: 中):
   - published_texts.csv（7,953 件）+ publications.csv からの追加学習データ抽出は、ベースライン構築後に検討

4. **評価環境整備** (優先度: 高):
   - BLEU と chrF++ のローカル評価スクリプト
   - 開発・検証データの分割（train の一部を hold-out）

> 次のタスク候補: `task_baseline_preprocessing_implementation`（前処理の実装と検証）

<!-- AUTO:project:start -->
- [[project_baseline|project: baseline]]
<!-- AUTO:project:end -->
