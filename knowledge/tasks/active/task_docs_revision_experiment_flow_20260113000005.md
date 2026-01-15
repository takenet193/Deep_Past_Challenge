---
type: task
id: task-20260113000005
title: .cursor/experiment_flow_instructions.mdc の改訂
author: takeikumi
status: completed
priority: medium
project: docs_revision
mode: documentation
context: []
dependencies: []
related_notes: []
assignee:
assigned_agent:
due_date:
created: 2026-01-13
updated: 2026-01-14
---

# タスク: .cursor/experiment_flow_instructions.mdc の改訂

## 目的
- 実験フロー指示ファイルを実際の実験ディレクトリ構造に合わせて更新
- 実装済みの実験管理システムに基づいた指示の更新

## 手順
- [x] 現在のexperiment_flow_instructions.mdcの内容を確認
- [x] 実際の実験ディレクトリ構造の確認
  - experiments/ の実際の構造
  - results/ の実際の構造
  - ファイル命名規則の確認
- [x] 実装済みの実験管理システムに基づいた指示の更新
- [x] 実際の実験例に基づいた説明の追加
- [x] エージェントの動作指示の更新
- [x] レビューと修正

## 改訂ポイント
- 実際の実験ディレクトリ構造に合わせた更新
- 実装済みの実験管理システムに基づいた指示の更新
- 実際の実験例に基づいた説明の追加
- ファイル命名規則の確認と反映

## 結果（実施報告）

### 主要な改訂内容

1. **Plannerのタスク読み取り手順の追加**
   - `tasks/current_sprint.json` からタスクを読み取る手順を追加
   - `load_active_tasks()` を推奨として明記
   - 使用例を追加

2. **実験IDの命名規則の明確化**
   - 実験IDは `exp[YYYYMMDDHHMMSS]_[description]` 形式（タイムスタンプ形式）であることを明記
   - 例を追加（`exp20260106030720_baseline_tfidf_lr` など）

3. **ディレクトリ構造の説明の詳細化**
   - `experiments/` と `results/` の分離について説明を追加
   - 実験レポート（`exp[timestamp]_report.md`）が `results/` に含まれることを明記
   - コードと結果の分離について説明を追加

4. **エラーハンドリングセクションの誤字修正**
   - 行290の「１」という誤字を削除

5. **Version Controllerルールへの参照の明確化**
   - `.cursor/version_controller_rules.mdc` への参照を明確化
   - コミットメッセージの例を実際の実装に合わせて更新

6. **実験管理セクションの命名規則の修正**
   - `experiment{N}_{description}` → `exp[YYYYMMDDHHMMSS]_[description]` に修正
   - ディレクトリ構造の説明を詳細化
   - 結果記録の説明を追加

7. **関連ドキュメントへの参照の追加**
   - Developer 実験運用ルールへの参照を追加
   - Version Controller ルールへの参照を追加

### 関連作業

- `docs/experiment_flow_revision_analysis.md` を作成し、不一致点をリスト化
- 実際のコードベースと照合して正確性を確認
- 実際の実験ディレクトリ構造を参照して説明を更新

## 学び

- 実験フロー指示ファイルは実際の実装に基づいて記述することが重要
- 実験IDの命名規則やディレクトリ構造の説明があると、エージェントが正しくファイルを作成できる
- エージェント間の連携フローは詳細に記載することで、エージェントが正しく動作しやすくなる
- 誤字や古い情報は定期的に確認して修正する必要がある

## 次のアクション

- なし（このタスクで完了）

<!-- AUTO:project:start -->
- [[project_docs_revision|project: docs_revision]]
<!-- AUTO:project:end -->
