# タスク管理（GTD形式）

このディレクトリは、Getting Things Done (GTD) の方法論に基づいてタスクを管理します。

## ディレクトリ構造

- `inbox/`: 未整理のタスク（新しく追加されたタスク）
- `active/`: 現在進行中のタスク
- `waiting/`: 他のタスクや外部要因を待っているタスク
- `completed/`: 完了したタスク

## タスクファイルの形式

各タスクはMarkdownファイルとして保存され、以下の構造を持ちます：

```markdown
---
id: task-001
title: 特徴量エンジニアリングの実験
status: active
priority: high
project: feature_engineering
context: experiment
due_date: 2024-01-20
tags: [feature-engineering, experiment]
related_notes: [20240101000000, 20240102000000]
assigned_agent: planner
dependencies: []
created: 2024-01-15
updated: 2024-01-15
expected_outcome:
  type: experiment
  metrics: [RMSE]
  target_improvement: "0.15 -> 0.12"
---

# 特徴量エンジニアリングの実験

## 目的
カテゴリカル変数のターゲットエンコーディングを実装し、モデルの性能を向上させる。

## 手順
1. カテゴリカル変数を特定
2. ターゲットエンコーディングを実装
3. クロスバリデーションで評価
4. 結果を記録

## 結果
（実験後に記入）

## 学び
（実験後に記入）
```

## タスクのライフサイクル

1. **作成**: `inbox/` に新しいタスクを作成
2. **整理**: タスクを適切なステータスに移動（`active/`, `waiting/`）
3. **実行**: マルチエージェントシステムにJSON形式で引き渡し
4. **完了**: タスクを `completed/` に移動

## JSONへの変換

タスクをマルチエージェントシステムに引き渡す際は、`src/task_converter.py` を使用してJSON形式に変換します。

```bash
python src/task_converter.py
```

変換されたJSONファイルは `tasks/` ディレクトリに保存されます。

