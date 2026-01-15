# scripts_guide.md 改訂分析

## 現在のscripts_guide.mdとコードベースの不一致

### 1. 新規スクリプトの欠落

**scripts_guide.md（現在）**:
- `task_converter.py`, `task_loader.py`, `sync_project_links.py` のみ記載

**実際の実装**:
- ✅ `scripts/workflow/move_task.py` が追加されているが記載されていない
- ✅ `scripts/kaggle/` 配下のスクリプトが記載されていない
  - `check_kaggle_auth.sh`
  - `submit_to_kaggle.sh`
  - `submit_with_token.sh`

**修正が必要**: 新規スクリプトの説明を追加

---

### 2. task_converter.py の重複チェック機能が記載されていない

**scripts_guide.md（現在）**:
- 重複チェック機能についての記載がない

**実際の実装**:
- 重複チェック機能が追加されている（同じタスクIDが複数のディレクトリに存在する場合を検出）
- 警告メッセージを表示する

**修正が必要**: 重複チェック機能の説明を追加

---

### 3. JSONスキーマの例が古い

**scripts_guide.md（現在）**:
```json
{
  "generated_at": "2026-01-05T00:00:00",
  "total_tasks": 5,
  "tasks": [
    {
      "type": "task",
      "id": "task-001",
      "title": "タスクタイトル",
      "status": "in_progress",
      "priority": "high",
      "project": "kaggle",
      "mode": "experiment",
      "context": ["note_id_1"],
      "due_date": "2026-01-10",
      "tags": ["kaggle", "experiment"],
      "related_notes": [],
      "dependencies": [],
      "assignee": null,
      "assigned_agent": "planner",
      "source_file": "knowledge/tasks/active/task_001.md",
      "updated_at": "2026-01-05T00:00:00"
    }
  ]
}
```

**実際の実装** (`tasks/current_sprint.json`):
- `total_tasks` フィールドは存在しない（`tasks` 配列の長さで判断）
- タスクIDは `task-YYYYMMDDHHMMSS` 形式（タイムスタンプ形式）
- `assigned_agent` は通常 `null`（`"planner"` ではない）
- `source_file` のパス形式が異なる（`task_001.md` → `task_xxx_20260113000003.md`）

**修正が必要**: JSONスキーマ例を実際の実装に合わせて更新

---

### 4. task_loader.py の説明が不正確

**scripts_guide.md（現在）**:
- `load_pending_tasks()` は `status: "pending"` のタスクを読み込むと記載

**実際の実装**:
- `load_pending_tasks()` は `status == "pending"` のタスクを読み込む（正しい）
- しかし、実際のシステムでは `status: "in_progress"` のタスクが `active/` ディレクトリに存在する
- `pending` ステータスのタスクは通常存在しない（`active/` = `in_progress`）

**修正が必要**: `load_pending_tasks()` の説明を実際の使用状況に合わせて更新（または `load_active_tasks()` を推奨）

---

### 5. ディレクトリ構造の説明が不足

**scripts_guide.md（現在）**:
- `scripts/workflow/` のみ記載
- `scripts/kaggle/` についての記載がない

**実際の実装**:
```
scripts/
├── workflow/          # ワークフロー管理用
│   ├── task_converter.py
│   ├── task_loader.py
│   ├── sync_project_links.py
│   └── move_task.py
└── kaggle/            # Kaggle提出用
    ├── check_kaggle_auth.sh
    ├── submit_to_kaggle.sh
    └── submit_with_token.sh
```

**修正が必要**: ディレクトリ構造の説明を追加

---

### 6. 実行例が不足

**scripts_guide.md（現在）**:
- 基本的な使い方のみ記載
- 実際の出力例がない
- エラーメッセージの例がない

**実際の実装**:
- 重複チェック時の警告メッセージ
- エラーハンドリングの実際の動作

**修正が必要**: 実際の出力例とエラーメッセージの例を追加

---

### 7. ワークフロー説明が不十分

**scripts_guide.md（現在）**:
- 基本的な使用フローのみ
- `move_task.py` の使用が含まれていない

**実際の実装**:
- タスクを移動する際は `move_task.py` を使用すべき
- 重複チェックは `task_converter.py` 実行時に自動的に行われる

**修正が必要**: ワークフローに `move_task.py` の使用を追加

---

### 8. トラブルシューティングが不足

**scripts_guide.md（現在）**:
- `task_converter.py` と `task_loader.py` のトラブルシューティングのみ
- 重複チェックに関するトラブルシューティングがない
- `move_task.py` のトラブルシューティングがない
- `sync_project_links.py` のトラブルシューティングがない

**修正が必要**: 各スクリプトのトラブルシューティングを追加

---

## 可読性の問題と改善案

### 現在の問題点

1. **スクリプトの分類が不明確**: workflow と kaggle の区別が不明確
2. **新規スクリプトの記載がない**: `move_task.py` と `scripts/kaggle/` 配下のスクリプト
3. **実際の出力例がない**: 実行結果のイメージがつかない
4. **エラーハンドリングの説明が不足**: 実際のエラーメッセージの例がない
5. **ワークフローが不十分**: `move_task.py` の使用が含まれていない

### 改善案：構成の再編成

#### 提案1: セクション構成の再編成

```markdown
# スクリプトガイド

## 概要
- スクリプトの分類（workflow / kaggle）
- ディレクトリ構造

## ワークフロー管理スクリプト

### 1. task_converter.py
- 目的、使い方、入出力
- 重複チェック機能
- 実際の出力例

### 2. task_loader.py
- 目的、使い方、主要関数
- 使用例

### 3. sync_project_links.py
- 目的、使い方、動作
- 前提条件、注意事項

### 4. move_task.py（新規）
- 目的、使い方
- 安全な移動の仕組み

## Kaggle提出スクリプト

### 1. check_kaggle_auth.sh
- 目的、使い方

### 2. submit_to_kaggle.sh
- 目的、使い方

### 3. submit_with_token.sh
- 目的、使い方

## スクリプト実行のワークフロー
- 典型的な使用フロー（move_task.pyを含む）
- 各スクリプトの実行タイミング

## トラブルシューティング
- 各スクリプトのよくある問題と解決方法
- 重複チェックに関するトラブルシューティング

## 関連ドキュメント
```

#### 提案2: 実際の出力例の追加

各スクリプトの実行結果の例を追加：
- `task_converter.py` の重複警告メッセージ
- `task_loader.py` の出力例
- `sync_project_links.py` の実行結果

#### 提案3: エラーハンドリングの詳細化

各スクリプトのエラーメッセージの例と対処法を追加。

---

## 改訂の優先順位

### 高優先度
1. 新規スクリプトの追加（`move_task.py`, `scripts/kaggle/` 配下）
2. 重複チェック機能の説明追加
3. JSONスキーマ例の更新（実際の実装に合わせる）
4. ワークフローに `move_task.py` の使用を追加

### 中優先度
5. 実際の出力例の追加
6. エラーハンドリングの詳細化
7. トラブルシューティングの拡充

### 低優先度
8. 構成の再編成（可読性向上）
9. ディレクトリ構造の説明追加




