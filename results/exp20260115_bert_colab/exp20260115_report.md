---
id: 20260115
title: Disaster Tweets - BERT (Colab実行)
author: takeikumi
type: experiment_report
experiment_id: exp20260115_bert_colab
project: kaggle_disaster_tweets
form: report
description: BERT (bert-base-uncased) + Linear + Dropout, 25エポック, Google Colab上で実行
parent_experiment: exp20260106030720
related_task: task-20260114141258
tags: [kaggle, kaggle_disaster_tweets, bert, deep-learning, transformers, colab, experiment, report]
status: completed
metrics:
  train_loss_final: 0.015667
  cv_mean: null
  cv_std: null
  public_lb: 0.81060
model:
  type: BERT (bert-base-uncased)
  features: text_only
links:
  - project_kaggle_disaster_tweets_baseline_improvement
  - task-20260114141258
  - exp20260106030720_report
created: 2026-01-15
updated: 2026-01-15
---

# Disaster Tweets - BERT (Colab実行)

## 実験概要

| 項目 | 値 |
|:---|:---|
| 実験ID | exp20260115_bert_colab |
| 実施日 | 2026-01-15 |
| 目的 | ディスカッションから取得したBERTモデルをColab上で実行し、ベースライン（TF-IDF + LogisticRegression）との性能比較を実施 |
| 親実験 | exp20260106030720（ベースライン） |
| 関連タスク | task-20260114141258 |
| 実行環境 | Google Colab (GPU: Tesla T4) |

## 仮説

- 深層学習モデル（BERT）による性能向上を期待
- 転移学習の効果により、シンプルなTF-IDF + LogisticRegressionを上回る性能が得られる
- ベースライン（Public LB=0.80079）を上回る結果を目標

## 実装内容

### 前処理

- トークナイザー: `AutoTokenizer.from_pretrained('bert-base-uncased')`
- 最大長: 128
- パディング: `max_length`
- トランケーション: `True`
- 前処理（lowercase、URL除去など）: 実施せず（BERTトークナイザーが自動処理）

### 特徴量

- 使用列: `text` のみ
- トークン化: BERTトークナイザーによる自動トークン化
- 入力形式: `input_ids`, `attention_mask`, `token_type_ids`

### モデル

- **ベースモデル**: BERT (bert-base-uncased)
- **分類ヘッド**: 
  - Linear(768 → 2)
  - Dropout(0.5)
- **モデルアーキテクチャ**: 
  - BERTの最終層出力 → Dropout → Linear層 → 分類（2クラス）

### CV方式

- **CV評価**: スキップ（動作確認・学習時間短縮のため）
- 実行時間短縮のため、最初の実験ではCV評価を行わず、直接学習→推論→提出を実施

## ハイパーパラメータ

```yaml
model:
  type: BERT (bert-base-uncased)
  classification_head:
    hidden_size: 768
    num_classes: 2
    dropout: 0.5
training:
  epochs: 25
  batch_size: 64  # GPUメモリ制約により256から変更
  learning_rate: 2e-5
  weight_decay: 1e-2
  optimizer: AdamW
  loss: CrossEntropyLoss
tokenizer:
  max_length: 128
  padding: max_length
  truncation: true
seed: 42
```

## 結果

### 評価指標

| Metric | Train Loss (Final) | CV Mean | CV Std | Public LB |
|:---|:---:|:---:|:---:|:---:|
| F1 Score | - | - | - | **0.81060** |

- **Train Loss (最終エポック)**: 0.015667
- **実行時間**: 約50分（25エポック）
- **Public LB F1 Score**: **0.81060**
- **Public LB 順位**: **263位/717チーム**（約36.7%）

### ベースラインとの比較

| 実験 | モデル | Public LB | 比較 |
|:---|:---|:---:|:---|
| ベースライン (exp20260106030720) | TF-IDF + LogisticRegression | 0.80079 | - |
| 本実験 (exp20260115_bert_colab) | BERT (bert-base-uncased) | **0.81060** | **+0.00981 (+1.22%)** |

### 特徴量

- 入力特徴量: BERTトークン化されたテキスト（最大128トークン）
- 埋め込み次元: 768（BERT-base）
- 特徴量重要度: 深層学習モデルのため直接取得不可

## 学んだこと

- **BERTモデルによる性能向上を確認**: ベースライン（TF-IDF + LogisticRegression, Public LB=0.80079）を**+0.00981（約1.2%向上）**で上回る結果を達成
- **GPUメモリ制約**: 初期設定（batch_size=256）ではTesla T4のGPUメモリ不足が発生。batch_size=64に削減することで解決
- **学習時間**: 25エポックで約50分（Colab GPU環境）
- **Colab実行の課題**: ローカル環境と異なる実行環境での実験管理の課題を認識（実行コードがローカルに存在しない）
- **CV評価の重要性**: 今回の実験ではCV評価をスキップしたが、今後の実験ではCV評価を実施し、より堅牢な性能評価を行う必要がある

## 次のステップ

- [ ] CV評価を追加してより堅牢な性能評価を実施
- [ ] ハイパーパラメータチューニング（学習率、エポック数、ドロップアウト率など）
- [ ] 他のBERTモデル（RoBERTa、DistilBERTなど）の実験
- [ ] アンサンブル手法の検討（BERT + TF-IDF + LogisticRegressionなど）
- [ ] 外部GPU実行環境（Colab、Kaggle）の統一的な管理方法の実装（memo_external_gpu_execution_workflow_20260115060219参照）

## ファイル一覧

```
experiments/exp20260115_bert_colab/
├── README.md                    # 実験説明（Colab実行のためコードファイルなし）
└── bert.ipynb                   # 参考資料（Kaggleディスカッションから取得したオリジナル）

results/exp20260115_bert_colab/
├── exp20260115_report.md        # このファイル（実験レポート）
├── exp20260115_metrics.json     # 評価指標
├── exp20260115_submission.csv   # 提出ファイル
└── README.md                    # 結果サマリー

注意: この実験はGoogle Colab上で実行されたため、実際の学習コード（train.py, predict.py）や
モデルファイル（.pkl）はローカルには存在しません。実験コードはColabノートブック上で実行され、
結果ファイル（submission.csv）はGoogle Driveからローカルにコピーしています。
```

