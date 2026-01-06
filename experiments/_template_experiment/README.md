# Experiment: expYYYYMMDDHHMMSS - [description]

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

### 特徴量重要度 TOP5
1. 
2. 
3. 
4. 
5. 

## 学んだこと

- 

## 次のステップ

- [ ] 
- [ ] 

## ファイル一覧

```
expYYYYMMDDHHMMSS_[description]/
├── expYYYYMMDDHHMMSS_README.md         # このファイル（実験IDをファイル名に含める）
├── expYYYYMMDDHHMMSS_config.yaml       # 設定ファイル（実験IDをファイル名に含める）
├── expYYYYMMDDHHMMSS_train.py          # 学習スクリプト（実験IDをファイル名に含める）
├── expYYYYMMDDHHMMSS_predict.py        # 推論スクリプト（実験IDをファイル名に含める）
└── results/
    ├── expYYYYMMDDHHMMSS_metrics.json  # 評価指標（実験IDをファイル名に含める）
    ├── expYYYYMMDDHHMMSS_cv_results.json  # CV結果（実験IDをファイル名に含める）
    ├── expYYYYMMDDHHMMSS_submission.csv  # 提出ファイル（実験IDをファイル名に含める）
    └── expYYYYMMDDHHMMSS_model.pkl  # モデルファイル（実験IDをファイル名に含める）
```

**注意**: 同じディレクトリ内の全てのファイルに同じタイムスタンプ（実験ID）を付与する


