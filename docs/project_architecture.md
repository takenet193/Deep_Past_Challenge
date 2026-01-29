# Kaggle Competition Development Platform - アーキテクチャ設計書

> **📊 図の表示について**: このドキュメントにはMermaid図が含まれている場合があります。
> 図が表示されない場合は、**Markdownプレビュー**を開いてください（`Cmd+Shift+V`）。

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

## 設計上の重要な決定事項

### 1. 知識ベース名称: **KaggleBase**
- 理由: シンプルで目的が明確。「Kaggle」と「Knowledge Base」を組み合わせた造語
- 代替案も検討可: CompetitionVault, InsightHub, ML-Zettel

### 2. タグ体系: YAMLフロントマター + フラットなタグ
- 実際の実装では、YAMLフロントマターのフィールド（`type`, `status`, `project`）とフラットなタグ（`tags`フィールド）を組み合わせて管理
- タグは階層構造ではなく、フラットな形式（例: `kaggle`, `nlp`, `experiment`）

### 3. 実験ID: タイムスタンプ形式（実装済み）
- **実装形式**: `exp[YYYYMMDDHHMMSS]_[description]`（例: `exp20260106030720_baseline_tfidf_lr`）
- **理由**: 実験の作成時刻がIDから判別可能で、時系列管理が容易
- **初期設計**: `exp001` 形式を想定していたが、実装ではタイムスタンプ形式を採用

### 4. ディレクトリ分離: experiments/ と results/
- experiments/: コード（Git管理対象）
- results/: 出力（一部Git管理、大容量ファイルはDVC）

### 5. エージェント間の厳密な役割分離
- 各エージェントは自分の専門領域にのみ集中
- 他エージェントの領域に侵入しない = 責任の明確化

### 6. 監視スクリプトによる自動化戦略 🆕
- Markdownファイルを単一の真実の源（Single Source of Truth）とする
- JSON形式は自動生成される派生データとして扱う
- 人間は戦略とコンテンツに集中、ファイル同期は自動化
- フェーズ3（基本ワークフロー確立後）に導入

## よくある質問（FAQ）

### Q1: なぜObsidianを使うのか？
**A**: Zettelkastenとの親和性が高く、Wikilinks、Graph View、タグシステムが充実しているため。Markdown形式でGit管理も容易。

### Q2: current_sprint.jsonとGTDタスクの関係は？
**A**: GTDタスク（Markdown）がSSOTで人間向け、current_sprint.jsonがAIエージェント向けの生成物。`src/task_converter.py` で生成します。

### Q3: 実験の派生関係はどう管理する？
**A**: 各実験のREADME.mdに`parent`フィールドを記載。Obsidianが自動的にGraph Viewで可視化。

### Q4: MLOpsパイプラインとの統合タイミングは？
**A**: フェーズ2でローカルワークフローが安定してから。知人との協議で調整。

### Q5: 複数のコンペを同時に進める場合は？
**A**: YAMLフロントマターの`project`フィールド（例: `project: kaggle_disaster_tweets`）で区別。
`task_converter.py`が自動的に`current_sprint.json`に集約する。

### Q6: 監視スクリプトは必須？ 🆕
**A**: いいえ、オプションです。手動フローでも問題なく動作します。ただし、導入することで以下のメリットがあります:
- Markdownのみ管理すればよい（JSON管理不要）
- 変換し忘れによる不整合を防止
- 保存と同時に自動変換（リアルタイム同期）

推奨: まず手動フローで2-3回の実験を回し、ワークフローを理解した後に導入。

### Q7: 監視スクリプトとValidatorエージェントの違いは？ 🆕
**A**: 
- **監視スクリプト**: 実行**前**のコード品質チェック（構文、Lint、ファイル存在）
- **Validatorエージェント**: 実行**後**のモデル性能評価（RMSE、CV Score）

全く異なる役割で、両方とも重要です。

## 改訂履歴

### v1.2 (2026-01-14)
- **実装内容に合わせた全面改訂**
  - タスクJSONスキーマを実際の実装に合わせて更新
  - 実験ID・タスクIDの命名規則をタイムスタンプ形式に統一
  - config.yamlテンプレートを実際の構造に合わせて更新
  - ディレクトリ構造を実際の実装に合わせて修正
  - 実装済み機能と未実装機能を明確に分離
  - 将来実装機能の詳細設計セクションを新設
- **構造の改善**
  - 各コンポーネントを実装済み/未実装で明確に分離
  - 実装状況一覧表を追加
  - 可読性と保守性の向上

### v1.1 (2026-01-13)
- **監視スクリプトシステム**の章を追加
- 4つの監視スクリプト（task, knowledge, experiment, results）の詳細設計
- Single Source of Truth による二重管理問題の解決方法
- エージェントとの連携フロー図
- FAQ に監視スクリプト関連の質問を追加
- 実装ロードマップを更新（フェーズ3に監視スクリプト追加）

### v1.0 (2024-11-30)
- 初版リリース
- 5つのコンポーネント設計（知識管理、タスク管理、マルチエージェント、実験管理、MLOps）
- マルチエージェントシステムの詳細化
- 実験管理ディレクトリ構造
- 実装ロードマップ

---

**最終更新**: 2026-01-23  
**バージョン**: v2.0（ドキュメント分割版）  
**作成者**: チーム  
**レビュー**: 定期的に実験結果を反映して更新
