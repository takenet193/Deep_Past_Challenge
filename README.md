# Kaggle Competition Sandbox

Kaggleコンペ参加のための効率的な開発環境

## ディレクトリ構造

```
.
├── .cursor/              # Cursor設定
├── mcp_setup/            # MCP設定
├── data/
│   ├── raw/              # Kaggleからの生データ
│   └── processed/        # 加工済みデータ
├── docs/                 # ドキュメント
└── src/                  # 実行可能なスクリプト
```

## 使い方

1. Kaggleからデータをダウンロードして `data/raw/` に配置
2. データの前処理スクリプトを `src/` に作成
3. 加工済みデータを `data/processed/` に保存

