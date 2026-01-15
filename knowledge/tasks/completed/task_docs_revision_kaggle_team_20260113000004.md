---
type: task
id: task-20260113000004
title: .cursor/kaggle_team.mdc の改訂
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

# タスク: .cursor/kaggle_team.mdc の改訂

## 目的
- エージェント定義ファイルを実装済み機能に基づいて更新
- 実際のワークフローに合わせた動作説明の更新

## 手順
- [x] 現在のkaggle_team.mdcの内容を確認
- [x] 実装済み機能の確認
  - タスク管理システムの実装状況
  - 実験管理システムの実装状況
  - エージェントの実際の動作
- [x] エージェントの役割定義の更新
- [x] 実際のワークフローに合わせた動作説明の更新
- [x] 各エージェントの制約と役割の明確化
- [x] レビューと修正

## 改訂ポイント
- 実装済み機能に基づいたエージェントの役割定義の更新
- 実際のワークフローに合わせた動作説明の更新
- 各エージェントの制約と役割の明確化

## 結果（実施報告）

### 主要な改訂内容

1. **タスク読み取りのパス修正**
   - `tasks/` ディレクトリ → `tasks/current_sprint.json` に修正
   - 実際の実装に合わせて正確なパスを記載

2. **タスク読み取りの説明修正**
   - `load_pending_tasks()` → `load_active_tasks()` を推奨として明記
   - 実際のシステムでは `status: "pending"` のタスクは通常存在しないことを説明
   - 使用例を追加

3. **実験IDの命名規則の明記**
   - 実験IDは `exp[YYYYMMDDHHMMSS]_[description]` 形式（タイムスタンプ形式）であることを明記
   - 例を追加

4. **ディレクトリ構造の説明追加**
   - `experiments/` と `results/` の分離について説明を追加
   - 実験コードは `experiments/` に、実験結果は `results/` に保存されることを明記

5. **エージェント間の連携フローの詳細化**
   - 全体フローを明確に記載
   - 各ステップの詳細を追加
   - Document Managerが最初に情報収集を行うことを明記
   - `.cursor/experiment_flow_instructions.mdc` への参照を追加

6. **Validatorのワークフローの詳細化**
   - 関連タスク・プロジェクトの検索手順を明確化
   - 検索条件を具体的に記載

### 関連作業

- `docs/kaggle_team_revision_analysis.md` を作成し、不一致点をリスト化
- 実際のコードベースと照合して正確性を確認
- 実際のスクリプトファイルを参照して説明を更新

## 学び

- エージェント定義ファイルは実際の実装に基づいて記述することが重要
- タスク読み取りのパスや関数名は実際の実装と一致させる必要がある
- エージェント間の連携フローは詳細に記載することで、エージェントが正しく動作しやすくなる
- 実験IDの命名規則やディレクトリ構造の説明があると、エージェントが正しくファイルを作成できる

## 次のアクション

- なし（このタスクで完了）

<!-- AUTO:project:start -->
- [[project_docs_revision|project: docs_revision]]
<!-- AUTO:project:end -->
