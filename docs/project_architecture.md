# Kaggle Competition Development Platform - アーキテクチャ設計書

## 概要

本プロジェクトは、Kaggleコンペティションに参加するための統合開発プラットフォームです。
知識管理（Zettelkasten + GTD）、JSON形式のタスク管理、マルチエージェントシステム、実験管理の4つの主要コンポーネントが実装済みです。
MLOpsパイプラインは将来実装予定です。

詳細な設計については、以下のドキュメントを参照してください。

## システム設計ドキュメント

### システム概要

- [システム概要](./system_overview.md) - エグゼクティブサマリーとシステム全体構成図

### コンポーネント詳細設計

- [知識・タスクデータベース](./components/knowledge_database.md) - KaggleBase（Obsidian + Zettelkasten + GTD）
- [JSON形式タスク管理システム](./components/task_management.md) - タスク変換とJSON管理
- [マルチエージェントシステム](./components/multi_agent_system.md) - 5つの専門AIエージェント
- [実験・結果管理](./components/experiment_management.md) - 実験ID管理と結果保存

### 実装計画

- [実装ロードマップ](./roadmap.md) - フェーズ別の実装計画と進捗
- [将来実装機能の詳細設計](./future_features.md) - 監視スクリプトシステムとMLOpsパイプライン

## ディレクトリ構造

プロジェクト全体のディレクトリ構造については、[README.md](../README.md#ディレクトリ構造)を参照してください。
各コンポーネントの詳細なディレクトリ構造については、以下のドキュメントを参照してください：

- **知識・タスクデータベース**: [knowledge_database.md](./components/knowledge_database.md#ディレクトリ構造)
- **実験・結果管理**: [experiment_management.md](./components/experiment_management.md#ディレクトリ構造詳細版)
- **スクリプト**: [scripts_guide.md](./scripts_guide.md#ディレクトリ構造)
