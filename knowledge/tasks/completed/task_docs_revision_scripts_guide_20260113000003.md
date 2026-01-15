---
type: task
id: task-20260113000003
title: docs/scripts_guide.md の改訂
author: takeikumi
status: completed
completed_date: 2026-01-14
priority: medium
project: docs_revision
mode: documentation
context: []
dependencies: []
related_notes: []
assignee: null
assigned_agent: null
due_date: null
created: 2026-01-13
updated: 2026-01-14
---

# タスク: docs/scripts_guide.md の改訂

## 目的
- 基本的な説明はあるが、実装内容との整合性確認
- 実際の出力例の追加
- エラーハンドリングの実装状況を反映

## 手順
- [x] 現在のscripts_guide.mdの内容を確認
- [x] 実装済みスクリプトの動作確認
  - task_converter.py
  - task_loader.py
  - sync_project_links.py
  - move_task.py（新規追加）
  - scripts/kaggle/配下のスクリプト（新規追加）
- [x] 実際の出力例の追加
- [x] エラーハンドリングの実装状況を反映
- [x] 各スクリプトの実際の動作を確認して説明を更新
- [x] レビューと修正

## 改訂ポイント
- 実装済みスクリプトの動作確認
- 実際の出力例の追加
- エラーハンドリングの実装状況を反映
- 実際のファイル構造に基づいた説明の更新

## 結果（実施報告）

### 主要な改訂内容

1. **構成の再編成**
   - 概要セクションを追加（スクリプトの分類、ディレクトリ構造）
   - ワークフロー管理スクリプトとKaggle提出スクリプトを明確に分離

2. **新規スクリプトの追加**
   - `scripts/workflow/move_task.py` の説明を追加（安全なタスク移動）
   - `scripts/kaggle/` 配下のスクリプトの説明を追加
     - `check_kaggle_auth.sh`: Kaggle API認証確認
     - `submit_to_kaggle.sh`: Kaggle提出
     - `submit_with_token.sh`: トークン指定での提出

3. **重複チェック機能の説明追加**
   - `task_converter.py` の重複チェック機能を説明
   - 警告メッセージの例と対処法を追加

4. **JSONスキーマ例の更新**
   - 実際の実装に合わせて更新（`total_tasks` フィールドを削除、タスクIDをタイムスタンプ形式に）
   - `assigned_agent` は通常 `null` であることを明記

5. **`task_loader.py` の説明修正**
   - `load_pending_tasks()` の説明を修正（実際には `pending` ステータスは使われていない）
   - `load_active_tasks()` を推奨として明記
   - 実際の出力例を追加

6. **実際の出力例の追加**
   - 各スクリプトの実行結果例を追加
   - 重複警告メッセージの例を追加
   - Kaggle提出スクリプトの実行結果例を追加

7. **ワークフローの更新**
   - `move_task.py` の使用を推奨ワークフローに追加
   - タスク管理とKaggle提出の2つのワークフローを分離

8. **トラブルシューティングの拡充**
   - 各スクリプトのトラブルシューティングを追加
   - 重複チェックに関するトラブルシューティングを追加
   - Kaggle提出スクリプトのトラブルシューティングを追加

### 関連作業

- `docs/scripts_guide_revision_analysis.md` を作成し、不一致点をリスト化
- 実際のコードベースと照合して正確性を確認
- 実際のスクリプトファイルを参照して説明を更新

## 学び

- スクリプトガイドは実際の実装に基づいて記述することが重要
- 新規スクリプトが追加された際は、ドキュメントも同時に更新する必要がある
- 実際の出力例があると、ユーザーがスクリプトの動作を理解しやすくなる
- トラブルシューティングセクションがあると、問題解決が容易になる

## 次のアクション

- なし（このタスクで完了）

<!-- AUTO:project:start -->
- [[project_docs_revision|project: docs_revision]]
<!-- AUTO:project:end -->
