# Results Template: expYYYYMMDDHHMMSS - [description]

このディレクトリは、実験結果ファイルのテンプレートです。

## ファイル構成

```
results/expYYYYMMDDHHMMSS_[description]/
├── expYYYYMMDDHHMMSS_report.md         # 実験レポート（Validatorが作成、実験IDをファイル名に含める）
├── expYYYYMMDDHHMMSS_metrics.json      # 評価指標（実験IDをファイル名に含める）
├── expYYYYMMDDHHMMSS_cv_results.json   # CV結果（実験IDをファイル名に含める）
├── expYYYYMMDDHHMMSS_submission.csv    # 提出ファイル（実験IDをファイル名に含める）
└── expYYYYMMDDHHMMSS_model.pkl         # モデルファイル（実験IDをファイル名に含める）
```

## 各ファイルの説明

### expYYYYMMDDHHMMSS_report.md
- **作成者**: Validatorエージェント
- **内容**: 実験の詳細レポート（YAMLフロントマター + Markdown）
- **用途**: 実験結果の記録、知識ベースへの反映

### expYYYYMMDDHHMMSS_metrics.json
- **作成者**: Developerエージェント（train.py実行時）
- **内容**: 評価指標（train_f1, cv_mean, cv_std, public_lb等）
- **用途**: 実験結果の比較、Git管理対象

### expYYYYMMDDHHMMSS_cv_results.json
- **作成者**: Developerエージェント（train.py実行時）
- **内容**: 各フォールドのCVスコア
- **用途**: CV結果の詳細分析

### expYYYYMMDDHHMMSS_submission.csv
- **作成者**: Developerエージェント（predict.py実行時）
- **内容**: Kaggle提出用の予測結果
- **用途**: Kaggleへの提出

### expYYYYMMDDHHMMSS_model.pkl
- **作成者**: Developerエージェント（train.py実行時）
- **内容**: 学習済みモデル
- **用途**: 推論時のモデル読み込み（Git管理対象外）

## 注意事項

- **ファイル名**: 全てのファイルに同じタイムスタンプ（実験ID）を付与する
- **Git管理**: `metrics.json`, `cv_results.json`, `submission.csv`, `report.md` はGit管理対象
- **Git除外**: `model.pkl` は大容量のため `.gitignore` で除外

## テンプレートファイル

- `expYYYYMMDDHHMMSS_report.md` - 実験レポートのテンプレート（Validatorが作成）
- `expYYYYMMDDHHMMSS_metrics.json` - metrics.jsonのテンプレート（train.pyで自動生成）
- `expYYYYMMDDHHMMSS_cv_results.json` - cv_results.jsonのテンプレート（train.pyで自動生成）
- `expYYYYMMDDHHMMSS_c_search.json` - ハイパーパラメータ探索結果のテンプレート（オプション、train.pyで自動生成）

これらのテンプレートをコピーして、実際の実験IDに置き換えて使用してください。

**注意**: `metrics.json`、`cv_results.json`、`c_search.json` は通常、`train.py` の実行時に自動生成されます。テンプレートは参考用です。

