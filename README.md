# Kaggle Competition Development Platform

Kaggleコンペ参加のための統合的な開発環境。
知識管理（Obsidian/Zettelkasten/GTD）、マルチエージェントシステム、実験管理を統合したワークフローを提供します。

## クイックスタート

### 1. セットアップ

```bash
# 依存関係のインストール
pip install -r requirements.txt

# ディレクトリの作成
mkdir -p knowledge/{inbox,zettelkasten/{permanent,references,structure,index},tasks/{active,waiting,someday,completed,archive,projects/{archive}},templates}
mkdir -p tasks experiments results data/{raw,processed} scripts

# Obsidianの設定
# knowledge/ ディレクトリをObsidianのVaultとして開く
```

### 2. 最初の実験を実行する

1. 実験テンプレートをコピー:
   ```bash
   cp -r experiments/_template_experiment experiments/exp$(date +%Y%m%d%H%M%S)_my_first_experiment
   ```

2. 設定ファイルを編集:
   - `experiments/exp[timestamp]_my_first_experiment/exp[timestamp]_config.yaml` を編集

3. 実験を実行:
   ```bash
   cd experiments/exp[timestamp]_my_first_experiment
   python exp[timestamp]_train.py
   ```

詳細は [ワークフローガイド](docs/workflow_guide.md) を参照してください。

## ドキュメント

プロジェクトの詳細設計や運用方法は以下のドキュメントを参照してください。

- **[システム概要・アーキテクチャ](docs/system_overview.md)**: システム全体の構成図、ディレクトリ構造、設計思想。
- **[ロードマップ](docs/roadmap.md)**: 実装状況と今後の計画。
- **[ワークフローガイド](docs/workflow_guide.md)**: 実験の進め方、タスク管理、ベストプラクティス。
- **[スクリプトガイド](docs/scripts_guide.md)**: 各種スクリプト（タスク変換、Kaggle提出など）の使い方。
- **[将来実装機能の詳細設計](docs/future_features.md)**: 将来の実装計画詳細。

## ディレクトリ構成

- `knowledge/`: 知識ベース（Obsidian Vault）
- `tasks/`: エージェント用タスクJSON
- `experiments/`: 実験コード
- `results/`: 実験結果
- `scripts/`: ユーティリティスクリプト
- `docs/`: ドキュメント
- `.cursor/`: AIエージェント定義ファイル

詳細なディレクトリ構造は [システム概要・アーキテクチャ](docs/system_overview.md) を参照してください。
