# スクリプトガイド

このドキュメントでは、プロジェクト内の各スクリプトの目的、使い方、入出力を説明します。

## 概要

### スクリプトの分類

プロジェクトのスクリプトは以下の2つのカテゴリに分類されます：

1. **ワークフロー管理スクリプト** (`scripts/workflow/`): タスク管理、プロジェクトリンク同期など
2. **Kaggle提出スクリプト** (`scripts/kaggle/`): Kaggle APIを使用した提出処理

### ディレクトリ構造

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

---

## ワークフロー管理スクリプト

### 1. `scripts/workflow/task_converter.py`

#### 目的

タスクをMarkdown（Obsidian形式）からJSONに変換するスクリプト。  
Zettelkasten + GTD形式のタスクをマルチエージェントシステムが読み取れるJSON形式に変換します。

#### 使い方

```bash
python scripts/workflow/task_converter.py
```

#### 入力

- `knowledge/tasks/{active|waiting|someday|completed}/` 配下のMarkdownファイル（`.md`）
  - ファイル名が `_` で始まるものは除外されます

#### 出力

- `tasks/current_sprint.json`
  - 全タスクを集約したJSONファイル
  - タスクは優先度・ステータス・期日・更新日時でソートされます

#### 主要機能

- **Markdownパース**: YAML frontmatterからタスク情報を抽出
- **ステータス変換**: ディレクトリ名（`active`等）→ JSONステータス（`in_progress`等）
- **ソート**: ブロック状態 → 優先度 → 期日 → 更新日時 → ID の順でソート
- **エラーハンドリング**: パースエラーが発生したファイルはスキップし、エラーメッセージを表示
- **重複チェック**: 同じタスクIDが複数のディレクトリに存在する場合を検出して警告

#### 重複チェック機能

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

#### 出力JSONの構造（実際の実装に基づく）

```json
{
  "generated_at": "2026-01-14T13:29:00",
  "tasks": [
    {
      "type": "task",
      "id": "task-20260112173705",
      "title": "Disaster Tweets: keyword特徴量の追加実験",
      "status": "in_progress",
      "priority": "high",
      "project": "kaggle_disaster_tweets_baseline_improvement",
      "mode": "experiment",
      "context": [
        "project_kaggle_disaster_tweets_baseline_improvement",
        "project_kaggle_disaster_tweets"
      ],
      "dependencies": [
        "exp20260106030720_report"
      ],
      "related_notes": [
        "disaster_tweets_baseline_improvement_ideas_20260112162435",
        "exp20260106030720_report",
        "disaster_tweets_eda_20260105180000"
      ],
      "source_file": "knowledge/tasks/active/task_disaster_tweets_keyword_feature_20260112173705.md",
      "tags": [
        "kaggle",
        "kaggle_disaster_tweets",
        "improvement",
        "feature-engineering",
        "keyword",
        "experiment"
      ],
      "due_date": null,
      "assignee": null,
      "assigned_agent": null,
      "updated_at": "2026-01-12T00:00:00"
    }
  ]
}
```

#### 注意事項

- **SSOT（Single Source of Truth）**: `knowledge/tasks/` のMarkdownファイルが真実の源です
- **手編集禁止**: `tasks/current_sprint.json` は自動生成されるため、**手で編集しないでください**
- **実行タイミング**: タスクを追加・更新・移動した後に実行してください

---

### 2. `scripts/workflow/task_loader.py`

#### 目的

マルチエージェントシステムがタスクJSONを読み取るためのユーティリティ。  
Plannerエージェントがタスクを読み取り、分解して各エージェントに割り当てる際に使用します。

#### 使い方

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

#### 主要関数

##### `load_task(task_id: str, tasks_dir: Path = Path("tasks")) -> Optional[Dict]`

特定のタスクを読み込む。

**引数**:
- `task_id`: タスクID（例: `"task-20260112173705"`）
- `tasks_dir`: タスクJSONファイルのディレクトリ（デフォルト: `tasks/`）

**戻り値**: タスク情報の辞書、見つからない場合は `None`

##### `load_pending_tasks(tasks_dir: Path = Path("tasks")) -> List[Dict]`

未処理のタスク（`status: "pending"`）をすべて読み込む。

**注意**: 実際のシステムでは `status: "pending"` のタスクは通常存在しません。  
`active/` ディレクトリのタスクは `status: "in_progress"` として扱われます。

**戻り値**: 未処理タスクのリスト（通常は空）

##### `load_active_tasks(tasks_dir: Path = Path("tasks")) -> List[Dict]` ⭐ 推奨

進行中のタスク（`status: "in_progress"`）をすべて読み込む。

**戻り値**: 進行中タスクのリスト

##### `load_tasks_by_project(project: str, tasks_dir: Path = Path("tasks")) -> List[Dict]`

特定のプロジェクトのタスクを読み込む。

**引数**:
- `project`: プロジェクト名（例: `"kaggle_disaster_tweets"`）

**戻り値**: プロジェクトのタスクリスト

##### `load_tasks_index(tasks_dir: Path = Path("tasks")) -> Optional[Dict]`

タスクインデックスファイル（`current_sprint.json`）全体を読み込む。

**戻り値**: インデックス情報の辞書（`generated_at`, `tasks` を含む）

##### `format_task_for_planner(task: Dict) -> str`

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

#### 使用例

```bash
# コマンドラインから実行
python scripts/workflow/task_loader.py
```

未処理タスクの最初の3件を表示します。

---

### 3. `scripts/workflow/sync_project_links.py`

#### 目的

Project（プロジェクトハブノート）とTask（タスクノート）間のリンクを自動同期するスクリプト。  
Obsidianプラグイン不要で、Markdownファイルを直接編集します。

#### 使い方

```bash
# 通常実行（ファイルを更新）
python scripts/workflow/sync_project_links.py

# ドライラン（変更内容を確認のみ、ファイルは更新しない）
python scripts/workflow/sync_project_links.py --dry-run
```

#### 動作

1. **タスク → プロジェクトリンク**: 各タスクノートに、所属プロジェクトへのリンクを自動追加
   - マーカー: `<!-- AUTO:project:start -->` と `<!-- AUTO:project:end -->` の間
2. **プロジェクト → タスク一覧**: 各プロジェクトハブノートに、所属タスクの一覧を自動生成
   - マーカー: `<!-- AUTO:tasks:start -->` と `<!-- AUTO:tasks:end -->` の間
   - タスクはステータス（active/waiting/someday/completed）ごとにグループ化

#### 実行結果例

```
Updated:
Projects: 6 / Tasks: 22
```

#### 前提条件

- タスクノートのfrontmatterに `project: <project名>` が設定されていること
- プロジェクトハブノートは `knowledge/tasks/projects/project_<project名>.md` に配置される

#### 注意事項

- **自動生成セクション**: マーカーで囲まれた部分は自動生成されるため、手で編集しても上書きされます
- **プロジェクトハブノートの自動作成**: 存在しないプロジェクトハブノートは自動で作成されます

---

### 4. `scripts/workflow/move_task.py` ⭐ 新規

#### 目的

タスクファイルを安全に移動するユーティリティ。  
`mv` コマンドで移動した際に元のファイルが残ってしまう問題を防ぐため、移動後に確実に元のファイルを削除します。

#### 使い方

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

#### 動作

1. 移動元のファイルが存在するか確認
2. 移動先のディレクトリが存在しない場合は作成
3. ファイルをコピー（`shutil.copy2`）
4. コピーが成功したことを確認
5. 元のファイルを削除（`source.unlink()`）
6. 元のファイルが残っていないことを確認

#### 実行結果例

```
✓ タスクを移動しました: task-20260112173705.md
  移動元: knowledge/tasks/active/task-20260112173705.md
  移動先: knowledge/tasks/completed/task-20260112173705.md
```

#### エラーハンドリング

- 移動元のファイルが存在しない場合: エラーメッセージを表示して終了
- コピーに失敗した場合: エラーメッセージを表示して終了
- 元のファイルの削除に失敗した場合: 警告メッセージを表示（移動先は作成済み）

#### 注意事項

- **重複防止**: このスクリプトを使用することで、タスクの重複を防げます
- **推奨**: タスクを移動する際は、`mv` コマンドではなくこのスクリプトを使用してください

---

## Kaggle提出スクリプト

### 1. `scripts/kaggle/check_kaggle_auth.sh`

#### 目的

Kaggle API認証を確認するスクリプト。  
`~/.kaggle/kaggle.json` の存在と権限、API認証の動作を確認します。

#### 使い方

```bash
bash scripts/kaggle/check_kaggle_auth.sh
```

または

```bash
chmod +x scripts/kaggle/check_kaggle_auth.sh
./scripts/kaggle/check_kaggle_auth.sh
```

#### 動作

1. `~/.kaggle/kaggle.json` の存在確認
2. ファイル権限の確認（推奨: `600`）
3. API認証テスト（`kaggle competitions list`）
4. 利用可能なコンペティションの一覧表示（最初の5件）

#### 実行結果例

```
==========================================
Kaggle API認証確認
==========================================

✅ kaggle.jsonが見つかりました
-rw-------  1 user  staff   123 Jan 14 12:00 /Users/user/.kaggle/kaggle.json

✅ ファイル権限は正しく設定されています (600)

API認証をテストします...
✅ 認証成功！Kaggle APIが使用できます

利用可能なコンペティション（最初の5件）:
ref                                                      deadline  category  reward  teamCount  userHasEntered
------------------------------------------------------  ---------  --------  ------  ---------  --------------
nlp-getting-started                                     2026-01-31  Getting   $0      1234       True
...

==========================================
```

#### エラー時の対処

- **`kaggle.json` が見つからない場合**:
  1. https://www.kaggle.com/ → Account → API → Create New API Token
  2. ダウンロードした `kaggle.json` を `~/.kaggle/` に配置
  3. `chmod 600 ~/.kaggle/kaggle.json` を実行

- **認証に失敗する場合**:
  - `kaggle.json` の内容を確認
  - ファイル権限が `600` になっているか確認

---

### 2. `scripts/kaggle/submit_to_kaggle.sh`

#### 目的

Kaggleコンペティションに提出ファイルを送信するスクリプト。  
実験結果（`submission.csv`）をKaggle APIを使用して提出します。

#### 使い方

```bash
# スクリプトを編集して実験IDと提出ファイルを設定
vim scripts/kaggle/submit_to_kaggle.sh

# 実行
bash scripts/kaggle/submit_to_kaggle.sh
```

#### 設定項目

スクリプト内の以下の変数を編集してください：

```bash
EXP_ID="exp20260112174906"
COMPETITION="nlp-getting-started"
SUBMISSION_FILE="results/${EXP_ID}_keyword_tfidf_lr/${EXP_ID}_submission.csv"
MESSAGE="${EXP_ID}: keyword feature + TF-IDF + LogisticRegression"
```

#### 動作

1. 提出ファイルの存在確認
2. Kaggle API認証確認
3. 提出実行（`kaggle competitions submit`）
4. 結果の表示

#### 実行結果例

```
==========================================
Kaggle提出スクリプト
==========================================
実験ID: exp20260112174906
コンペティション: nlp-getting-started
提出ファイル: results/exp20260112174906_keyword_tfidf_lr/exp20260112174906_submission.csv
メッセージ: exp20260112174906: keyword feature + TF-IDF + LogisticRegression
==========================================

提出ファイルを確認しました:
-rw-r--r--  1 user  staff  98K Jan 14 12:00 results/exp20260112174906_keyword_tfidf_lr/exp20260112174906_submission.csv

Kaggle API認証を確認中...
認証OK

提出を実行します...
Successfully submitted to nlp-getting-started

==========================================
提出が完了しました！
Kaggleのコンペティションページで結果を確認してください
https://www.kaggle.com/competitions/nlp-getting-started/submissions
==========================================
```

#### エラーハンドリング

- 提出ファイルが見つからない場合: エラーメッセージを表示して終了
- API認証に失敗した場合: エラーメッセージを表示して終了
- 提出に失敗した場合: エラーメッセージを表示して終了

---

### 3. `scripts/kaggle/submit_with_token.sh`

#### 目的

Kaggle APIトークンを直接指定して提出するスクリプト。  
環境変数や設定ファイルを使用せず、コマンドライン引数でトークンを指定します。

#### 使い方

```bash
bash scripts/kaggle/submit_with_token.sh \
  <コンペティション名> \
  <提出ファイル> \
  <メッセージ> \
  <username> \
  <key>
```

**例**:
```bash
bash scripts/kaggle/submit_with_token.sh \
  nlp-getting-started \
  results/exp20260112174906_keyword_tfidf_lr/exp20260112174906_submission.csv \
  "exp20260112174906: keyword feature" \
  your_username \
  your_api_key
```

#### 注意事項

- APIキーをコマンドライン引数で指定するため、シェル履歴に残る可能性があります
- 通常は `submit_to_kaggle.sh` を使用することを推奨します

---

## スクリプト実行のワークフロー

### 典型的な使用フロー

#### 1. タスク管理のワークフロー

```bash
# 1. タスク作成・更新
# knowledge/tasks/active/ にMarkdownファイルを追加・編集

# 2. タスク変換（JSON生成）
python scripts/workflow/task_converter.py
# → 重複チェックも自動実行される

# 3. プロジェクトリンク同期（タスクにprojectフィールドがある場合）
python scripts/workflow/sync_project_links.py

# 4. エージェント実行
# Plannerが tasks/current_sprint.json を読み取り、タスクを分解

# 5. タスク完了（推奨: move_task.pyを使用）
python scripts/workflow/move_task.py \
  knowledge/tasks/active/task-xxx.md \
  knowledge/tasks/completed/task-xxx.md

# 6. 再変換（必要に応じて）
python scripts/workflow/task_converter.py
```

#### 2. Kaggle提出のワークフロー

```bash
# 1. 認証確認
bash scripts/kaggle/check_kaggle_auth.sh

# 2. 実験実行（Developerエージェントが実行）
# experiments/exp[timestamp]_[description]/exp[timestamp]_train.py

# 3. 提出ファイルの確認
ls -lh results/exp[timestamp]_[description]/exp[timestamp]_submission.csv

# 4. 提出実行
# scripts/kaggle/submit_to_kaggle.sh を編集して実行
bash scripts/kaggle/submit_to_kaggle.sh

# 5. 結果確認
# Kaggleのコンペティションページで結果を確認
```

---

## トラブルシューティング

### `task_converter.py` でエラーが出る場合

**問題**: YAML frontmatterのパースエラー

**原因と解決方法**:
- **YAML frontmatterの形式を確認**: `---` で囲まれているか、閉じタグがあるか
- **ファイルエンコーディング**: UTF-8で保存されているか確認
- **パス**: スクリプトはリポジトリルートから実行してください

**確認方法**:
```bash
# エラーメッセージを確認
python scripts/workflow/task_converter.py

# 問題のあるファイルを特定
# エラーメッセージにファイル名が表示されます
```

**問題**: 重複警告が表示される

**原因と解決方法**:
- 同じタスクIDが複数のディレクトリに存在する
- 不要なファイルを削除してください
- 通常、完了したタスクは `completed/` にのみ存在すべきです

**対処法**:
```bash
# 重複ファイルを確認
python scripts/workflow/task_converter.py
# → 警告メッセージで重複ファイルの場所が表示される

# 不要なファイルを削除（通常は active/ の方を削除）
rm knowledge/tasks/active/task-xxx.md
```

---

### `task_loader.py` でタスクが見つからない場合

**問題**: `load_task()` や `load_active_tasks()` が空のリストを返す

**原因と解決方法**:
- **`current_sprint.json` が存在するか確認**: 先に `task_converter.py` を実行してください
- **タスクIDの確認**: 大文字小文字・ハイフン/アンダースコアの違いに注意
- **ステータスの確認**: `load_active_tasks()` は `status: "in_progress"` のタスクを返します

**確認方法**:
```python
# task_loader.pyを使用して確認
from scripts.workflow.task_loader import load_tasks_index

index = load_tasks_index()
print(f"Total tasks: {len(index.get('tasks', []))}")
```

---

### `sync_project_links.py` でリンクが更新されない場合

**問題**: 実行してもリンクが更新されない

**原因と解決方法**:
- **マーカーの確認**: `<!-- AUTO:project:start -->` と `<!-- AUTO:project:end -->` が正しく記述されているか確認
- **projectフィールドの確認**: タスクのYAML frontmatterに `project: <project_name>` が設定されているか確認
- **プロジェクトノートの存在確認**: `knowledge/tasks/projects/project_<project_name>.md` が存在するか確認

**確認方法**:
```bash
# ドライランで変更内容を確認
python scripts/workflow/sync_project_links.py --dry-run
```

---

### `move_task.py` で移動に失敗する場合

**問題**: 移動元のファイルが削除されない

**原因と解決方法**:
- **ファイル権限の確認**: ファイルの書き込み権限があるか確認
- **ファイルが開かれていないか確認**: 他のプロセスがファイルを使用していないか確認
- **手動削除**: 警告メッセージに従って、手動で削除してください

**確認方法**:
```bash
# 移動先のファイルが作成されているか確認
ls -lh knowledge/tasks/completed/task-xxx.md

# 移動元のファイルが残っているか確認
ls -lh knowledge/tasks/active/task-xxx.md
```

---

### Kaggle提出スクリプトでエラーが出る場合

**問題**: `check_kaggle_auth.sh` で認証に失敗する

**原因と解決方法**:
- **`kaggle.json` の存在確認**: `~/.kaggle/kaggle.json` が存在するか確認
- **ファイル権限の確認**: `chmod 600 ~/.kaggle/kaggle.json` を実行
- **APIトークンの確認**: KaggleのAccountページで新しいトークンを生成

**問題**: `submit_to_kaggle.sh` で提出に失敗する

**原因と解決方法**:
- **提出ファイルの存在確認**: `SUBMISSION_FILE` のパスが正しいか確認
- **コンペティション名の確認**: `COMPETITION` が正しいか確認
- **提出ファイルの形式確認**: CSVファイルが正しい形式か確認

---

## 関連ドキュメント

- **ワークフローガイド**: `docs/workflow_guide.md`
- **プロジェクトアーキテクチャ**: `docs/project_architecture.md`
- **タスク管理（GTD）**: `knowledge/tasks/_gtd_guide.md`（存在する場合）
- **Docs Managerルール**: `.cursor/docs_manager_rules.mdc`
- **Developer 実験運用ルール**: `.cursor/developer_experiment_rules.mdc`
