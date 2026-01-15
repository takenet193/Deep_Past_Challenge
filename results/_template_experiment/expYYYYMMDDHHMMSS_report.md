---
id: YYYYMMDDHHMMSS
title: [Experiment Title]
author: takeikumi
type: experiment_report
experiment_id: expYYYYMMDDHHMMSS
project: [project_name]
form: report
description: [1行で実験の説明]
parent_experiment: [親実験ID or null]
related_task: task-XXXXXXXXX
tags: [tag1, tag2, tag3, experiment, report]
status: completed
metrics:
  train_f1: 0.0000
  cv_mean: 0.0000
  cv_std: 0.0000
  public_lb: null
model:
  type: [ModelType]
  features: [feature_type]
links:
  - [related_note1]
  - [related_note2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [Experiment Title]

## 実験概要

| 項目 | 値 |
|:---|:---|
| 実験ID | expYYYYMMDDHHMMSS（タイムスタンプ形式） |
| 実施日 | YYYY-MM-DD |
| 目的 | （1行で） |
| 親実験 | （派生元があれば） |
| 関連タスク | task-XXXXXXXXX |

## 仮説

- （何を試すか、なぜ効くと思うか）

## 実装内容

### 前処理
- 

### 特徴量
- 

### モデル
- 

### CV方式
- 

## ハイパーパラメータ

```yaml
model:
  type: 
  params:
    
seed: 42
cv_folds: 5
```

## 結果

### 評価指標

| Metric | Train | CV Mean | CV Std | Public LB |
|:---|:---:|:---:|:---:|:---:|
| F1 Score |  |  |  |  |

### CV詳細（各フォールド）
- Fold 0: 
- Fold 1: 
- Fold 2: 
- Fold 3: 
- Fold 4: 

### 特徴量
- 

## 学んだこと

- 

## 次のステップ

- [ ] 
- [ ] 

## ファイル一覧

```
experiments/expYYYYMMDDHHMMSS_[description]/
├── expYYYYMMDDHHMMSS_config.yaml       # 設定ファイル
├── expYYYYMMDDHHMMSS_train.py          # 学習スクリプト
└── expYYYYMMDDHHMMSS_predict.py        # 推論スクリプト

results/expYYYYMMDDHHMMSS_[description]/
├── expYYYYMMDDHHMMSS_report.md         # このファイル（実験レポート）
├── expYYYYMMDDHHMMSS_metrics.json      # 評価指標
├── expYYYYMMDDHHMMSS_cv_results.json   # CV結果
├── expYYYYMMDDHHMMSS_submission.csv    # 提出ファイル
└── expYYYYMMDDHHMMSS_model.pkl         # モデルファイル
```




