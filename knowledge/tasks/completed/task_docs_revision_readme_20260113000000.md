---
type: task
id: task-20260113000000
title: README.md の改訂
author: takeikumi
status: completed
priority: high
project: docs_revision
mode: documentation
context: []
dependencies: []
related_notes: []
assignee: null
assigned_agent: null
due_date: null
created: 2026-01-13
updated: 2026-01-14
---

# タスク: README.md の改訂

## 目的
- 計画書的な内容を実装内容に合わせて更新
- 実際のディレクトリ構造とファイル名に基づいた正確な説明
- 新規ユーザーが実際のシステムを理解できるようにする

## 手順
- [x] 現在のREADME.mdの内容を確認
- [x] 実装済み機能の確認（task_converter.py, task_loader.py, sync_project_links.py等）
- [x] 実際のディレクトリ構造との整合性確認
- [x] 未実装機能の記載を「将来実装」として明記または削除
- [x] 実際のワークフローに基づいた手順の更新
- [x] ドキュメントへのリンクの確認と更新
- [x] レビューと修正

## 改訂ポイント
- ディレクトリ構造の実際の内容に合わせた更新
- 実装済みスクリプトの説明追加
- 未実装機能（監視スクリプト、MLOpsパイプライン等）の明確化
- 実際のファイル名とパスの確認

## 結果（実施報告）

### 主要な改訂内容

1. **構成の再編成**
   - 概要セクションを追加（プロジェクトの目的、実装状況一覧表）
   - クイックスタートセクションを追加
   - プロジェクト構成を「実装済み」と「将来実装予定」に分離
   - セットアップを「クイックスタート」と「詳細」に分離

2. **実装状況の明確化**
   - 実装状況一覧表を追加（✅実装済み / ⏳未実装）
   - MLOpsパイプラインを「将来実装予定」として明記
   - 各コンポーネントに実装状況を明記

3. **実験ディレクトリの命名規則の修正**
   - `experiment{N}_{description}/` → `exp[YYYYMMDDHHMMSS]_[description]/`（タイムスタンプ形式）
   - 実験ファイル名も同様に修正（`exp[timestamp]_train.py`など）

4. **ディレクトリ構造の完全な更新**
   - `results/` ディレクトリを追加
   - `scripts/` ディレクトリを追加（`workflow/` と `kaggle/` のサブディレクトリ構造）
   - `knowledge/zettelkasten/` のサブディレクトリ（`permanent/`, `references/`, `structure/`, `index/`）を追加
   - `knowledge/templates/` を追加
   - 実験ファイル構成を詳細化

5. **スクリプトの記載追加とディレクトリ統合**
   - `scripts/workflow/sync_project_links.py` を追加
   - `src/` と `scripts/` を統合し、`scripts/workflow/` と `scripts/kaggle/` に再編成
   - 各スクリプトの説明を追加

6. **ドキュメントの記載追加**
   - `docs/scripts_guide.md` を追加
   - `docs/inconsistencies_to_fix.md` を追加
   - `docs/portfolio_evaluation.md` を追加

7. **エージェント指示書の記載追加**
   - `.cursor/developer_experiment_rules.mdc` を追加
   - `.cursor/docs_manager_rules.mdc` を追加
   - `.cursor/version_controller_rules.mdc` を追加

8. **ワークフローの詳細化**
   - プロジェクトリンク同期のステップを追加
   - 実験の作成と実行の手順を追加
   - 各ステップの説明を詳細化

9. **セットアップ手順の充実**
   - クイックスタートセクションを追加
   - Obsidianの推奨プラグインを追加
   - テンプレートの使用方法を追加

10. **可読性の向上**
    - セクション間の明確な区切り
    - コードブロックの整理
    - 重要な情報の強調

### 関連作業

- `docs/readme_revision_analysis.md` を作成し、不一致点をリスト化
- 実際のコードベースと照合して正確性を確認
- `src/` と `scripts/` のディレクトリ統合を実施（scriptsディレクトリ統合計画に基づく）

## 学び

- README.mdは新規ユーザーの最初の入口なので、実装状況を明確に示すことが重要
- クイックスタートセクションがあると、新規ユーザーがすぐに始められる
- ディレクトリ構造は実際の実装に合わせて完全に記載する必要がある
- 実装済みと未実装を明確に分離することで、期待値の管理ができる

## 次のアクション

- なし（このタスクで完了）

<!-- AUTO:project:start -->
- [[project_docs_revision|project: docs_revision]]
<!-- AUTO:project:end -->
