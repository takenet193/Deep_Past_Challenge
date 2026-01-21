---
type: task
status: inbox
author: takeikumi
created: 2026-01-21
updated: 2026-01-21
tags: [task, obsidian, dataview, dataviewjs, gtd, master-note]
project: infrastructure
priority: high
mode: design
context: ["workflow", "gtd"]
dependencies: []
---

# （タスク候補）DataviewJSでマスタープロンプト用の依存関係ビューを追加する

## 目的
- Obsidianのマスターノート（`knowledge/tasks/_MASTER_TASKS.md` 想定）において、DataviewJSを使って **タスク間の依存関係** を表現できるようにする。
- AI向けマスタープロンプトの中で、`dependencies` 情報を活かした「ブロック中 / 着手可能」判定や、プロジェクトの多層構造（親プロジェクト / 子プロジェクト）を分かりやすく説明できるようにする。

## 完了条件
- マスターノートに DataviewJS ブロック（または専用の DataviewJS スニペット）が追加されている。
- `knowledge/tasks/**/*.md` の `dependencies` フィールドをもとに、
  - 依存タスクの有無（blocked / ready）
  - プロジェクト単位の依存関係（複層プロジェクト構造）
 がおおよそ把握できるビューが1つ以上提供されている。
- 上記ビューで得られる情報を前提にした **AI向けマスタープロンプトの草案** が、どこかのノートにメモされている。

## 手順（ラフでOK）
- [ ] `knowledge/tasks/_MASTER_TASKS.md` に Dataview/DataviewJS ブロックを追加する場所を決める（例：依存関係ビュー専用セクション）。
- [ ] 既存の GTD 実装計画（[[gtd_implementation_plan_20260101|GTD実装計画書（Obsidian/Dataview中心）]]) の要件を再確認し、DataviewJS で扱うべきフィールド・ロジックを整理する。
- [ ] `dv.table` / `dv.list` ベースの Dataview クエリから着手し、必要に応じて DataviewJS（`dv.api`）に拡張する。
- [ ] 依存関係の有無でタスクをグルーピングするロジック（blocked / ready）を実装する。
- [ ] プロジェクトの多層構造（親プロジェクト / 子プロジェクト）が分かる補助ビュー（または並び順）を検討する。
- [ ] 実装したビューを前提にした、AI向けマスタープロンプトのサンプル（依存関係の説明部分）をノートにまとめる。

## メモ
- 元になっている設計ノート: [[gtd_implementation_plan_20260101|GTD実装計画書（Obsidian/Dataview中心） - Kaggle_sandbox]]
- 関連タスク: [[task_parent_project_concept_20260121062656|親プロジェクトの概念考える]]
- まずは Dataview（通常クエリ）で要件を満たせるかを確認し、**本当に必要になったところだけ DataviewJS 化**する方針。
- 依存関係ビューが安定したら、`tasks/current_sprint.json` 側のスキーマやマスタープロンプトと一緒に見直す。
