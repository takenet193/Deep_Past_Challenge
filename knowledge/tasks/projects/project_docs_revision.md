---
type: project
id: project-docs-revision
title: ドキュメント改訂プロジェクト
project: docs_revision
created: 2026-01-13
updated: 2026-01-14
tags:
- project
- docs
- revision
status: active
---

# ドキュメント改訂プロジェクト

## タスク一覧（Dataview）

```dataview
TABLE WITHOUT ID
  default(id, file.name) AS id,
  link(file.path, default(title, file.name)) AS task,
  status,
  priority,
  due_date,
  mode,
  updated
FROM "knowledge/tasks"
WHERE type = "task" AND project = this.project
SORT choice(status="active",0, choice(status="waiting",1, choice(status="someday",2, 3))) ASC,
  choice(priority="critical",0, choice(priority="high",1, choice(priority="medium",2, 3))) ASC,
  due_date ASC,
  updated DESC
```

## 目的 / 成果物

実装が一段落したワークフローシステムに基づき、計画書的な位置付けだったドキュメント群を実際の実装内容に即したものに改訂する。

### 背景

- README.md や docs/project_architecture.md などの比較的詳細な文書が既に存在
- それらに基づいてワークフローシステムの実装が行われた
- 実装が一段落したため、計画書的な内容を実装内容に合わせて更新する必要がある

### 成果物

- 実装内容に即した最新のドキュメント群
- 新規ユーザーが実際のシステムを理解できる正確なドキュメント
- 実装とドキュメントの整合性確保

## 状態メモ

- 開始日: 2026-01-13
- 更新日: 2026-01-14
- 現在の実装状況:
  - タスク管理システム（task_converter.py, task_loader.py）実装済み
  - 実験管理システム（experiments/, results/）運用中
  - 知識管理システム（Zettelkasten + GTD）運用中
  - マルチエージェントシステム（.cursor/）定義済み
  - スクリプト（sync_project_links.py等）実装済み

### 完了したタスク

- ✅ **task-20260113000001**: docs/project_architecture.md の改訂（2026-01-14完了）
  - 実装状況の明確化（実装済み/未実装の分離）
  - 実験ID命名規則の更新（タイムスタンプ形式）
  - ディレクトリ構造の更新
  - Gitコミットメッセージ規約の改訂（Conventional Commits準拠）
  - エージェント指示書の更新
  - Version Controllerルールの新規作成

- ✅ **task-20260113000000**: README.md の改訂（2026-01-14完了）
  - 構成の再編成（概要、クイックスタート、プロジェクト構成の分離）
  - 実装状況の明確化（実装状況一覧表の追加）
  - 実験ディレクトリの命名規則の修正（タイムスタンプ形式）
  - ディレクトリ構造の完全な更新
  - スクリプトディレクトリの統合（`src/` と `scripts/` を `scripts/workflow/` と `scripts/kaggle/` に再編成）
  - ドキュメントとエージェント指示書の記載追加
  - ワークフローとセットアップ手順の詳細化

- ✅ **task-20260113000002**: docs/workflow_guide.md の改訂（2026-01-14完了）
  - 構成の再編成（概要、クイックスタート、詳細なワークフローの分離）
  - タスクID・実験IDの命名規則の修正（タイムスタンプ形式）
  - タスクJSONスキーマの修正（実際の実装に合わせて更新）
  - プロジェクトリンク同期のステップ追加
  - エージェント実行フローの詳細化（実際のフローに合わせて更新）
  - ノートIDの形式修正（14桁形式）
  - タスク・ノートのYAMLフロントマター例の更新
  - 実践例の更新（実際の実験例に基づく）
  - 結果記録の説明更新（experiments/とresults/の分離）
  - トラブルシューティングセクションの追加

- ✅ **task-20260113000003**: docs/scripts_guide.md の改訂（2026-01-14完了）
  - 構成の再編成（概要、ワークフロー管理/Kaggle提出の分離）
  - 新規スクリプトの追加（`move_task.py`, `scripts/kaggle/` 配下）
  - 重複チェック機能の説明追加
  - JSONスキーマ例の更新（実際の実装に合わせて更新）
  - `task_loader.py` の説明修正（`load_active_tasks()` を推奨として明記）
  - 実際の出力例の追加
  - ワークフローの更新（`move_task.py` の使用を追加）
  - トラブルシューティングの拡充

- ✅ **task-20260113000004**: .cursor/kaggle_team.mdc の改訂（2026-01-14完了）
  - タスク読み取りのパス修正（`tasks/` → `tasks/current_sprint.json`）
  - タスク読み取りの説明修正（`load_active_tasks()` を推奨として明記）
  - 実験IDの命名規則の明記（タイムスタンプ形式）
  - ディレクトリ構造の説明追加（`experiments/` と `results/` の分離）
  - エージェント間の連携フローの詳細化
  - Validatorのワークフローの詳細化

## 関連ノート（情報ハブ）

## 改訂が必要な文書一覧

### 1. README.md
**場所**: `/README.md`  
**現状**: 計画書的な内容が含まれている  
**改訂内容**:
- 実際のディレクトリ構造に合わせた更新
- 実装済み機能の説明を追加
- 未実装機能の記載を削除または「将来実装」として明記
- 実際のワークフローに基づいた手順の更新

### 2. docs/project_architecture.md
**場所**: `/docs/project_architecture.md`  
**現状**: 設計書・計画書としての内容が多い  
**改訂内容**:
- 実装済みコンポーネントの説明を実装内容に合わせて更新
- 未実装機能（監視スクリプト、MLOpsパイプライン等）を「将来実装」として明確化
- 実際のディレクトリ構造とファイル名に合わせた更新
- 実装済みスクリプトの説明を追加

### 3. docs/workflow_guide.md
**場所**: `/docs/workflow_guide.md`  
**現状**: 基本的なワークフローは記載されているが、実装詳細が不足  
**改訂内容**:
- 実際のスクリプト実行例を追加
- 実際のファイル構造に基づいた説明
- エージェント実行フローの実装状況を反映
- トラブルシューティングの追加

### 4. docs/scripts_guide.md
**場所**: `/docs/scripts_guide.md`  
**現状**: 基本的な説明はあるが、実装内容との整合性確認が必要  
**改訂内容**:
- 実装済みスクリプトの動作確認
- 実際の出力例の追加
- エラーハンドリングの実装状況を反映

### 5. .cursor/kaggle_team.mdc
**場所**: `/.cursor/kaggle_team.mdc`  
**現状**: エージェント定義ファイル  
**改訂内容**:
- 実装済み機能に基づいたエージェントの役割定義の更新
- 実際のワークフローに合わせた動作説明の更新

### 6. .cursor/experiment_flow_instructions.mdc
**場所**: `/.cursor/experiment_flow_instructions.mdc`  
**現状**: 実験フロー指示ファイル  
**改訂内容**:
- 実際の実験ディレクトリ構造に合わせた更新
- 実装済みの実験管理システムに基づいた指示の更新

<!-- AUTO:tasks:start -->
## タスク一覧（AUTO）

### active
- [[task_docs_revision_experiment_flow_20260113000005|task-20260113000005: .cursor/experiment_flow_instructions.mdc の改訂]]

### completed
- [[task_docs_revision_readme_20260113000000|task-20260113000000: README.md の改訂]]
- [[task_docs_revision_project_architecture_20260113000001|task-20260113000001: docs/project_architecture.md の改訂]]
- [[task_docs_revision_workflow_guide_20260113000002|task-20260113000002: docs/workflow_guide.md の改訂]]
- [[task_docs_revision_scripts_guide_20260113000003|task-20260113000003: docs/scripts_guide.md の改訂]]
- [[task_docs_revision_kaggle_team_20260113000004|task-20260113000004: .cursor/kaggle_team.mdc の改訂]]
<!-- AUTO:tasks:end -->

