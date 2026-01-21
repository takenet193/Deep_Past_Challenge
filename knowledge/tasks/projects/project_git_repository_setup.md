---
type: project
id: project-git_repository_setup
title: Git Repository Setup
project: git_repository_setup
created: 2026-01-21
updated: 2026-01-21
tags:
- project
- infrastructure
- git
links: []
---

# Project: Git Repository Setup

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

このプロジェクトのGitリポジトリを作成し、適切な初期設定を行う。

## 状態メモ

- 現在、ローカルにプロジェクトファイルは存在するが、Gitリポジトリがまだ作成されていない状態

## 関連ノート（情報ハブ）

- 

<!-- AUTO:tasks:start -->
## タスク一覧（AUTO）

### active
- [[task_file_cleanup_20260121071626|task-20260121071626: 旧プロジェクトファイルの整理・削除]]
<!-- AUTO:tasks:end -->
