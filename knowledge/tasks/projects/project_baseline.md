---
type: project
id: project-baseline
title: ベースライン作成
project: baseline
created: 2026-02-10
updated: 2026-02-10
tags:
  - project
  - baseline
status: active
---

# ベースライン作成

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

[Deep Past Initiative Machine Translation](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation) コンペティションにチャレンジしている。

### コンペ目標
- **上位10%に入る**ことを目指す

### このプロジェクトの目的
1. コンペの概要を理解する
2. ベースラインを作成する

## 状態メモ

- 2026-02-10: プロジェクト作成。

<!-- AUTO:tasks:start -->
## タスク一覧（AUTO）

### active
- （自動生成されます）
<!-- AUTO:tasks:end -->
