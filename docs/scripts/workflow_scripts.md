# ワークフロー管理スクリプト

このドキュメントでは、ワークフロー管理用のスクリプト（`scripts/workflow/`）の目的、使い方、入出力を説明します。

## 1. `scripts/workflow/task_converter.py`

### 目的

タスクをMarkdown（Obsidian形式）からJSONに変換するスクリプト。  
Zettelkasten + GTD形式のタスクをマルチエージェントシステムが読み取れるJSON形式に変換します。

### 使い方

```bash
python scripts/workflow/task_converter.py
```

### 入力

- `knowledge/tasks/{active|waiting|someday|completed}/` 配下のMarkdownファイル（`.md`）
  - ファイル名が `_` で始まるものは除外されます

### 出力

- `tasks/current_sprint.json`
  - 全タスクを集約したJSONファイル
  - タスクは優先度・ステータス・期日・更新日時でソートされます

### 主要機能

- **Markdownパース**: YAML frontmatterからタスク情報を抽出
- **ステータス変換**: ディレクトリ名（`active`等）→ JSONステータス（`in_progress`等）
- **ソート**: ブロック状態 → 優先度 → 期日 → 更新日時 → ID の順でソート
- **エラーハンドリング**: パースエラーが発生したファイルはスキップし、エラーメッセージを表示
- **重複チェック**: 同じタスクIDが複数のディレクトリに存在する場合を検出して警告

### 重複チェック機能

タスク変換時に、同じタスクIDが複数のディレクトリに存在する場合、警告メッセージを表示します。

**警告例**:
```
警告: タスクID 'task-20260105120020' が複数のディレクトリに存在します:
  - active/: task_disaster_tweets_baseline_submit_20260105120020.md
  - completed/: task_disaster_tweets_baseline_submit_20260105120020.md
  推奨: 完了したタスクは 'completed/' にのみ存在すべきです。
        重複ファイルを確認し、不要な方を削除してください。
```

**対処法**:
- 警告を確認して、不要なファイルを削除してください
- 通常、完了したタスクは `completed/` にのみ存在すべきです
- タスクを移動する際は `move_task.py` を使用することで重複を防げます

### 出力JSONの構造

JSON構造の詳細については、[タスク管理システムのドキュメント](../components/task_management.md#タスクjson-スキーマ)を参照してください。

### 注意事項

- **SSOT（Single Source of Truth）**: `knowledge/tasks/` のMarkdownファイルが真実の源です
- **手編集禁止**: `tasks/current_sprint.json` は自動生成されるため、**手で編集しないでください**
- **実行タイミング**: タスクを追加・更新・移動した後に実行してください

## 2. `scripts/workflow/task_loader.py`

### 目的

マルチエージェントシステムがタスクJSONを読み取るためのユーティリティ。  
Plannerエージェントがタスクを読み取り、分解して各エージェントに割り当てる際に使用します。

### 使い方

```python
from scripts.workflow.task_loader import (
    load_active_tasks,
    load_task,
    format_task_for_planner
)

# 進行中のタスクを読み込む（推奨）
active_tasks = load_active_tasks()

# 特定のタスクを読み込む
task = load_task("task-20260112173705")

# Planner向けにフォーマット
formatted = format_task_for_planner(task)
print(formatted)
```

### 主要関数

### `load_task(task_id: str, tasks_dir: Path = Path("tasks")) -> Optional[Dict]`

特定のタスクを読み込む。

**引数**:
- `task_id`: タスクID（例: `"task-20260112173705"`）
- `tasks_dir`: タスクJSONファイルのディレクトリ（デフォルト: `tasks/`）

**戻り値**: タスク情報の辞書、見つからない場合は `None`

### `load_pending_tasks(tasks_dir: Path = Path("tasks")) -> List[Dict]`

未処理のタスク（`status: "pending"`）をすべて読み込む。

**注意**: 実際のシステムでは `status: "pending"` のタスクは通常存在しません。  
`active/` ディレクトリのタスクは `status: "in_progress"` として扱われます。

**戻り値**: 未処理タスクのリスト（通常は空）

### `load_active_tasks(tasks_dir: Path = Path("tasks")) -> List[Dict]` ⭐ 推奨

進行中のタスク（`status: "in_progress"`）をすべて読み込む。

**戻り値**: 進行中タスクのリスト

### `load_tasks_by_project(project: str, tasks_dir: Path = Path("tasks")) -> List[Dict]`

特定のプロジェクトのタスクを読み込む。

**引数**:
- `project`: プロジェクト名（例: `"kaggle_disaster_tweets"`）

**戻り値**: プロジェクトのタスクリスト

### `load_tasks_index(tasks_dir: Path = Path("tasks")) -> Optional[Dict]`

タスクインデックスファイル（`current_sprint.json`）全体を読み込む。

**戻り値**: インデックス情報の辞書（`generated_at`, `tasks` を含む）

### `format_task_for_planner(task: Dict) -> str`

タスクをPlannerエージェントが読みやすい形式にフォーマット。

**戻り値**: フォーマットされた文字列（Markdown形式）

**出力例**:
```
# タスク: Disaster Tweets: keyword特徴量の追加実験
ID: task-20260112173705
ステータス: in_progress
優先度: high
プロジェクト: kaggle_disaster_tweets_baseline_improvement
モード: experiment

## 関連ノート
disaster_tweets_baseline_improvement_ideas_20260112162435, exp20260106030720_report, disaster_tweets_eda_20260105180000

## 依存タスク
exp20260106030720_report
```

### 使用例

```bash
# コマンドラインから実行
python scripts/workflow/task_loader.py
```

未処理タスクの最初の3件を表示します。

## 3. `scripts/workflow/sync_project_links.py`

### 目的

Project（プロジェクトハブノート）とTask（タスクノート）間のリンクを自動同期するスクリプト。  
Obsidianプラグイン不要で、Markdownファイルを直接編集します。

### 使い方

```bash
# 通常実行（ファイルを更新）
python scripts/workflow/sync_project_links.py

# ドライラン（変更内容を確認のみ、ファイルは更新しない）
python scripts/workflow/sync_project_links.py --dry-run
```

### 動作

1. **タスク → プロジェクトリンク**: 各タスクノートに、所属プロジェクトへのリンクを自動追加
   - マーカー: `<!-- AUTO:project:start -->` と `<!-- AUTO:project:end -->` の間
2. **プロジェクト → タスク一覧**: 各プロジェクトハブノートに、所属タスクの一覧を自動生成
   - マーカー: `<!-- AUTO:tasks:start -->` と `<!-- AUTO:tasks:end -->` の間
   - タスクはステータス（active/waiting/someday/completed）ごとにグループ化

### 実行結果例

```
Updated:
Projects: 6 / Tasks: 22
```

### 前提条件

- タスクノートのfrontmatterに `project: <project名>` が設定されていること
- プロジェクトハブノートは `knowledge/tasks/projects/project_<project名>.md` に配置される

### 注意事項

- **自動生成セクション**: マーカーで囲まれた部分は自動生成されるため、手で編集しても上書きされます
- **プロジェクトハブノートの自動作成**: 存在しないプロジェクトハブノートは自動で作成されます

## 4. `scripts/workflow/move_task.py` ⭐ 新規

### 目的

タスクファイルを安全に移動するユーティリティ。  
`mv` コマンドで移動した際に元のファイルが残ってしまう問題を防ぐため、移動後に確実に元のファイルを削除します。

### 使い方

```bash
python scripts/workflow/move_task.py <移動元> <移動先>
```

**例**:
```bash
# タスクを完了にする
python scripts/workflow/move_task.py \
  knowledge/tasks/active/task-20260112173705.md \
  knowledge/tasks/completed/task-20260112173705.md
```

### 動作

1. 移動元のファイルが存在するか確認
2. 移動先のディレクトリが存在しない場合は作成
3. ファイルをコピー（`shutil.copy2`）
4. コピーが成功したことを確認
5. 元のファイルを削除（`source.unlink()`）
6. 元のファイルが残っていないことを確認

### 実行結果例

```
✓ タスクを移動しました: task-20260112173705.md
  移動元: knowledge/tasks/active/task-20260112173705.md
  移動先: knowledge/tasks/completed/task-20260112173705.md
```

### エラーハンドリング

- 移動元のファイルが存在しない場合: エラーメッセージを表示して終了
- コピーに失敗した場合: エラーメッセージを表示して終了
- 元のファイルの削除に失敗した場合: 警告メッセージを表示（移動先は作成済み）

### 注意事項

- **重複防止**: このスクリプトを使用することで、タスクの重複を防げます
- **推奨**: タスクを移動する際は、`mv` コマンドではなくこのスクリプトを使用してください

## 関連ドキュメント

- [スクリプトガイド](../scripts_guide.md) - スクリプトの概要
- [Kaggle提出スクリプト](./kaggle_scripts.md) - Kaggle提出用スクリプト
- [スクリプト実行のワークフロー](./scripts_workflow.md) - 典型的な使用フロー
- [トラブルシューティング](./scripts_troubleshooting.md) - よくある問題と解決方法

