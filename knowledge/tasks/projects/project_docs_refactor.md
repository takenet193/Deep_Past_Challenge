---
type: project
id: project-docs-refactor
title: ドキュメントリファクタリング
project: docs_refactor
created: 2026-01-23
updated: 2026-01-23
tags:
  - project
  - docs
  - refactor
  - obsidian
status: active
---

# ドキュメントリファクタリング

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

マークダウンファイルの整理・最適化を行い、将来的な管理の困難を防ぐための仕組みを構築する。

### 主な目的
- マークダウンファイルの肥大化を防ぐ
- 検索性と可読性の向上
- 不必要・冗長な情報の削除
- 構造と説明の明瞭化・簡素化

### 成果物
- ファイル行数制限（300行以下、できれば150行以下）の遵守
- マークダウン構造の見出しレベル制限（###まで）の遵守
- リンクの修正と統一（相対パス形式への統一）
- ファイル名と内容の一致
- 内容重複・冗長な説明の削除

## 修正ポイント

### 1. リポジトリに含める/含めないの基準
- **リポジトリに必要なもの**
  - プロジェクトの構造や設計方針 (docs 相当)
  - 作業手順 (Skills 相当)
  - 実験記録 (experiments 相当)
  - 基礎知識 (permanent_notes、できれば docs に落とし込んで存在しないのがベター)
- **リポジトリに不要なもの**
  - 個人のメモ (references, structure や思想ノート等)

### 2. ファイル内のコード行数
- 多くても 300 行以下、できれば 150 行以下
- 300 行を超える場合は内容を分割
- 一行が長すぎる（約 100 文字以上）のも避ける

### 3. マークダウン構造
- 見出し3レベル（###）程度までを使用
- それ以上深くなる場合は、内容を分割して別ファイルにする

### 4. リンクの貼り方
- リンク切れの修正
- permanent_notes 内のリンクは同じ permanent_notes 内の他のノートのみを参照
- リンク表記を統一（リポジトリトップからの相対パス形式 `[title](./docs/title.md)` を推奨）

### 5. ファイルの命名と内容の不一致
- ファイル名と内容を一致させる
- 例: `project_architecture.md` からロードマップ、タスク管理、チーム運用などを分割
  - ロードマップ → `roadmap.md`
  - タスク管理 → `task_management.md`
  - チーム運用 → `team_operations.md`

### 6. 内容重複・冗長な説明の削除
- 重複した内容をリンクや別ファイル切り出しで整理
- フォルダ構造の説明は各一回で十分（ページ内リンクで参照）
- gitignore, json, templates, python コードの説明もリンクで参照
- サンプル提示用コードブロックは `_samples.json` 等にまとめてリンクで参照
- **二重管理を避ける**

## 状態メモ

- 2026-01-23: プロジェクト作成。共同開発者からの改善提案をプロジェクト化。

## 関連ノート（情報ハブ）

- [[task_refactor_20260123|改善提案元タスク]]

<!-- AUTO:tasks:start -->
## タスク一覧（AUTO）

### active
- （自動生成されます）
<!-- AUTO:tasks:end -->

