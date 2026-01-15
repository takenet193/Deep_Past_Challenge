---
type: task
id: task-20260113000002
title: docs/workflow_guide.md の改訂
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

# タスク: docs/workflow_guide.md の改訂

## 目的
- 基本的なワークフローは記載されているが、実装詳細を追加
- 実際のスクリプト実行例を追加
- エージェント実行フローの実装状況を反映

## 手順
- [x] 現在のworkflow_guide.mdの内容を確認
- [x] 実際のスクリプト実行例の追加
  - task_converter.pyの実行例
  - task_loader.pyの使用例
  - sync_project_links.pyの実行例
- [x] 実際のファイル構造に基づいた説明の追加
- [x] エージェント実行フローの実装状況を反映
- [x] トラブルシューティングセクションの追加
- [x] 実践例の更新（実際の実験例に基づく）
- [x] レビューと修正

## 改訂ポイント
- 実際のスクリプト実行例を追加
- 実際のファイル構造に基づいた説明
- エージェント実行フローの実装状況を反映
- トラブルシューティングの追加
- 実践例の更新（実際の実験例に基づく）

## 結果（実施報告）

### 主要な改訂内容

1. **構成の再編成**
   - 概要セクションを追加（ワークフローの全体像、実装状況一覧表）
   - クイックスタートセクションを追加
   - エージェント実行フローを独立したセクションに分離

2. **タスクID・実験IDの命名規則の修正**
   - `task-001` → `task-YYYYMMDDHHMMSS`（タイムスタンプ形式）
   - `experiment{N}_{description}/` → `exp[YYYYMMDDHHMMSS]_[description]/`（タイムスタンプ形式）

3. **タスクJSONスキーマの修正**
   - 実際の実装に合わせて更新（`status: "in_progress"`, `title`, `mode`, `source_file`など）
   - ルートレベルに `generated_at` と `tasks` 配列があることを明記

4. **プロジェクトリンク同期のステップ追加**
   - ステップ4として独立したセクションを追加
   - 実行タイミングとドライランオプションを説明

5. **エージェント実行フローの詳細化**
   - 実際のフロー（`User → Document Manager → Planner → User → Developer → Validator → User → Validator → Document Manager → Version Controller`）を記載
   - 各ステップの詳細説明を追加
   - ユーザー承認ステップとValidatorの結果入力依頼を明記

6. **ノートIDの形式修正**
   - `20240101000000`（8桁） → `YYYYMMDDHHMMSS`（14桁形式）

7. **タスク・ノートのYAMLフロントマター例の更新**
   - 実際の実装に合わせて更新（`type`, `author`, `mode`, `form` などのフィールドを追加）
   - 実際のタスク例（`task-20260112173705`）とノート例（`20260105180000_disaster_tweets_eda`）を使用

8. **実践例の更新**
   - 架空の例を削除し、実際の実験例（`exp20260106030720`, `exp20260112174906`）を使用
   - 実際のタスクID（`task-20260105120020`, `task-20260112173705`）を使用

9. **結果記録の説明更新**
   - 実験コードと結果が分離されていることを明記（`experiments/` と `results/`）
   - 実際の実験レポート例を追加

10. **トラブルシューティングセクションの追加**
    - よくある問題と解決方法を追加
    - タスク変換、プロジェクトリンク同期、エージェント実行、実験レポート作成に関するトラブルシューティング

11. **可読性の向上**
    - セクション間の明確な区切り
    - コードブロックの整理
    - 重要な情報の強調

### 関連作業

- `docs/workflow_guide_revision_analysis.md` を作成し、不一致点をリスト化
- 実際のコードベースと照合して正確性を確認
- 実際のタスクJSONとノートファイルを参照して例を更新

## 学び

- ワークフローガイドは実際の使用例に基づいて記述することが重要
- エージェント間の連携フローは、ユーザーの承認ステップを含めて正確に記載する必要がある
- トラブルシューティングセクションがあると、ユーザーが問題を解決しやすくなる
- 実践例は実際の実験IDやタスクIDを使用することで、より実用的になる

## 次のアクション

- なし（このタスクで完了）

<!-- AUTO:project:start -->
- [[project_docs_revision|project: docs_revision]]
<!-- AUTO:project:end -->
