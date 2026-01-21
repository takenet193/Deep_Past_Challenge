---
type: task
status: inbox
author: takeikumi
created: 2026-01-21
updated: 2026-01-21
tags:
  - task
  - architecture
  - project
  - gtd
project: ""
priority: high
mode: design
context: []
dependencies: []
---

# （タスク候補）親プロジェクトの概念考える

## 目的
- 親プロジェクト→子プロジェクト→タスクの複層的な構造を設計する
- 一つのタスクが複数のプロジェクトに属することができる仕組みを考える

## 完了条件
- 親プロジェクトと子プロジェクトの関係性が明確に定義されている
- タスクが複数のプロジェクトに属することができる仕組みが設計されている
- 実装方法（データ構造、メタデータ、ツール対応）が決まっている
- ドキュメントに反映されている

## 要件
- **複層構造**: 親プロジェクト → 子プロジェクト → タスク
- **多対多関係**: 一つのタスクが複数のプロジェクトに属していてもいい
- **既存システムとの整合性**: 現在のGTD/タスク管理システムとの互換性を保つ

## 手順（ラフでOK）
- [ ] 現在のプロジェクト構造を確認・分析
- [ ] 親プロジェクトの概念と要件を整理
- [ ] データ構造（メタデータ、YAMLフロントマター）を設計
- [ ] ツール（task_converter.py、sync_project_links.py）の対応方法を検討
- [ ] Obsidian/Dataviewでの表示方法を検討
- [ ] 実装方法と移行計画を文書化

## 検討事項
- メタデータでの親子関係の表現方法（`parent_project`, `projects: []`など）
- タスクの複数プロジェクト所属の表現方法
- Dataviewクエリでの親子プロジェクトの表示
- task_converter.pyでの処理方法
- 既存タスクへの影響

## メモ
- 確定したら `knowledge/tasks/{active|waiting|someday}/` にコピーしてSSOT化し、元ファイルは `knowledge/inbox/archive/` へ
- 関連タスク: [[task_dataviewjs_master_prompt_dependencies_20260121170000|DataviewJSでマスタープロンプト用の依存関係ビューを追加する]]


