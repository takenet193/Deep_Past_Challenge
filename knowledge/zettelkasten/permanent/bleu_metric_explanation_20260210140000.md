---
id: 20260210140000
title: BLEU 指標の説明
author: takeikumi
type: permanent
tags:
  - bleu
  - machine-translation
  - evaluation
  - nlp
links:
  - deep_past_competition_evaluation_submission_20260210130000
created: 2026-02-10
updated: 2026-02-10
---

# BLEU 指標の説明

機械翻訳の評価指標 BLEU（Bilingual Evaluation Understudy）の解説。仮説翻訳と参照翻訳の n-gram の一致度で品質を測る。

## 1. 概要

仮説に含まれる n-gram のうち、参照にも含まれる割合（適合率）を 1〜4-gram で計算し、幾何平均と Brevity Penalty で統合する。

## 2. n-gram

連続する $n$ 語の並び。

例："The cat sat on the mat"
- 1-gram: The, cat, sat, on, the, mat
- 2-gram: The cat, cat sat, sat on, on the, the mat
- 3-gram: The cat sat, cat sat on, sat on the, on the mat
- 4-gram: The cat sat on, cat sat on the, sat on the mat

## 3. 適合率 \(p_n\)

次数 $n$ について、仮説の n-gram のうち参照にも含まれる割合。

$$
p_n = \frac{\displaystyle\sum_{\text{仮説の全 } n\text{-gram}} \min\bigl( \text{Count}_{\text{hyp}}(ng), \, \text{Count}_{\text{ref}}(ng) \bigr)}{\displaystyle\sum_{\text{仮説の全 } n\text{-gram}} \text{Count}_{\text{hyp}}(ng)}
$$

- $\text{Count}_{\text{hyp}}(ng)$: 仮説での出現回数
- $\text{Count}_{\text{ref}}(ng)$: 参照での出現回数
- $\min$ でクリッピング（参照を超える過剰マッチを抑制）

## 4. 幾何平均

各次数の適合率 $p_1, p_2, p_3, p_4$ を幾何平均で統合。いずれかが低いと全体も下がる。

$$
\text{幾何平均} = \sqrt[4]{p_1 \cdot p_2 \cdot p_3 \cdot p_4} = \exp\left( \frac{1}{4} \sum_{n=1}^{4} \ln p_n \right)
$$

## 5. Brevity Penalty（BP）

仮説が参照より短いときにペナルティ。短くしすぎて適合率だけ高めるのを防ぐ。

$$
BP = \begin{cases}
1 & \text{if } c \geq r \\
\exp\left(1 - \dfrac{r}{c}\right) & \text{if } c < r
\end{cases}
$$

- $c$: 仮説の総語数
- $r$: 参照の総語数

## 6. BLEU スコア

$$
\text{BLEU} = BP \times \sqrt[4]{p_1 \cdot p_2 \cdot p_3 \cdot p_4} = BP \times \exp\left( \frac{1}{4} \sum_{n=1}^{4} \ln p_n \right)
$$

## 7. スムージング

$p_n = 0$ のとき対数が未定義になるため、SacreBLEU では小さい正の値で置換するスムージングを適用する。

## 関連ノート

- [[deep_past_competition_evaluation_submission_20260210130000|評価と提出方法（Deep Past Challenge）]]
