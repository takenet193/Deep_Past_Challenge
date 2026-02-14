---
id: 20260210130000
title: Deep Past Challenge - 評価と提出方法
author: takeikumi
type: permanent
tags:
  - kaggle
  - machine-translation
  - deep-past
  - evaluation
links:
  - deep_past_competition_overview_structure_20260210110000
  - bleu_metric_explanation_20260210140000
  - chrf_plus_plus_metric_explanation_20260211100000
  - evaluation_strategy_geometric_mean_20260211120000
created: 2026-02-10
updated: 2026-02-10
---

# Deep Past Challenge - 評価と提出方法

## 参照

- [評価・提出ページ](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/overview/evaluation)

## 評価指標（Evaluation）

提出は **BLEU と chrF++ の幾何平均**（Geometric Mean）で評価される。

- **BLEU の詳細**: [[bleu_metric_explanation_20260210140000|BLEU 指標の説明]]
- **chrF++ の詳細**: [[chrf_plus_plus_metric_explanation_20260211100000|chrF++ 指標の説明]]
- **スコアを伸ばす戦略**: [[evaluation_strategy_geometric_mean_20260211120000|評価指標（幾何平均）を伸ばす戦略]]

各スコアの十分統計量はコーパス全体で集約される（つまり、各スコアはマイクロ平均）。

- **実装参考**: [SacreBLEU](https://github.com/mjpost/sacrebleu) ライブラリ
- **Kaggle実装ノートブック**: [Geometric Mean of BLEU and chrF++](https://www.kaggle.com/code/metric/dpi-bleu-chrf)

## 提出ファイル（Submission File）

テストセットの各 `id` に対して、対応するアッカド語の転写（transliteration）の英語翻訳を予測する。各翻訳は1文で構成すること。

- **ヘッダー**: 必須
- **形式**: CSV

```
id,translation
0,Thus Kanesh, say to the -payers, our messenger, every single colony, and the...
1,In the letter of the City (it is written): From this day on, whoever buys meteoric...
2,As soon as you have heard our letter, who(ever) over there has either sold it to...
3,Send a copy of (this) letter of ours to every single colony and to all the trading...
...
```

## 関連ノート

- [[deep_past_competition_overview_structure_20260210110000|コンペ概要ストラクチャーノート（情報ハブ）]]
- [[bleu_metric_explanation_20260210140000|BLEU 指標の説明]]
- [[chrf_plus_plus_metric_explanation_20260211100000|chrF++ 指標の説明]]
- [[evaluation_strategy_geometric_mean_20260211120000|評価指標（幾何平均）を伸ばす戦略]]