---
id: 20260211100000
title: chrF++ 指標の説明
author: takeikumi
type: permanent
tags:
  - chrf
  - machine-translation
  - evaluation
  - nlp
links:
  - deep_past_competition_evaluation_submission_20260210130000
  - bleu_metric_explanation_20260210140000
created: 2026-02-11
updated: 2026-02-11
---

# chrF++ 指標の説明

機械翻訳の評価指標 chrF++ の解説。**文字 n-gram** と **単語 n-gram（1-gram, 2-gram）** の F-score で品質を測る。簡単に言うと、文字（と単語）の n-gram の**適合率と再現率の調和平均**（F値）である。語形変化の豊かな言語でも BLEU より人間の判断と相関が高いとされる。

## 1. 概要

- **chrF**: Character n-gram F-score（文字 n-gram の F値）
- **chrF+**: 文字 n-gram + 単語 1-gram
- **chrF++**: 文字 n-gram + 単語 1-gram と 2-gram（単語まで考慮した拡張版）

BLEU は「単語」単位の n-gram だが、chrF++ は「文字」を基本にしつつ、単語の一致も加える。

## 2. なぜ「文字」ベースか

- **語彙外 (OOV)**: 単語ベースだと未知語は 0 扱いになりがち
- **形態素が豊かな言語**: 語尾変化が多いと単語 n-gram が一致しにくい
- **トークナイザ不要**: 言語に依存しない文字 n-gram で比較できる

文字 n-gram なら部分一致（接頭辞・接尾辞の一致）もスコアに反映される。

## 3. F-score（適合率と再現率の調和平均）

BLEU は適合率（precision）中心。chrF は **適合率 P と再現率 R の F値** を使う。

$$
F_\beta = (1 + \beta^2) \cdot \frac{P \cdot R}{\beta^2 \cdot P + R}
$$

- **適合率 P**: 仮説に含まれる n-gram のうち、参照にも含まれる割合
- **再現率 R**: 参照に含まれる n-gram のうち、仮説にも含まれる割合
- **β**: 再現率をどれだけ重視するか。標準は **β = 2**（再現率をやや重視）

β=1 なら通常の F1（P と R の調和平均）。β=2 で再現率を強めに効かせる。

## 4. 文字 n-gram の範囲

- 通常 **1〜6 文字** の n-gram を使う（SacreBLEU のデフォルト: `char_order=6`）
- 各長さの F値 $F_1, \ldots, F_6$ を求め、**算術平均** で統合（BLEU の幾何平均とは異なる）

例: "cat" → 文字 1-gram: c, a, t / 2-gram: ca, at / 3-gram: cat

## 5. chrF++ の「++」：単語 n-gram の追加

- **chrF**: 文字 n-gram のみ
- **chrF+**: 文字 n-gram + **単語 1-gram**
- **chrF++**: 文字 n-gram + **単語 1-gram と 2-gram**

単語 unigram/bigram を足すことで、語順や語選択の一致も評価に取り込み、人間の品質判断との相関が上がることが知られている。

## 6. BLEU との違い（簡易まとめ）

| 観点      | BLEU            | chrF++                |
| ------- | --------------- | --------------------- |
| 単位      | 単語 n-gram       | 文字 n-gram + 単語 n-gram |
| 主に使う量   | 適合率 + BP        | 適合率と再現率の F値           |
| 統合      | 幾何平均            | 算術平均                  |
| 語長ペナルティ | Brevity Penalty | なし（再現率に含まれる）          |

## 7. 実装

- **SacreBLEU**: `sacrebleu` の chrF++ がコンペでも利用される
- スコアは 0〜1（または 0〜100）で、高いほど良い

## 関連ノート

- [[deep_past_competition_evaluation_submission_20260210130000|評価と提出方法（Deep Past Challenge）]]
- [[bleu_metric_explanation_20260210140000|BLEU 指標の説明]]
