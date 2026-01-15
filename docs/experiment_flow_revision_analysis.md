# experiment_flow_instructions.mdc 改訂分析

## 現在のexperiment_flow_instructions.mdcとコードベースの不一致

### 1. 実験IDの命名規則が古い

**experiment_flow_instructions.mdc（現在）**:
- 参考情報セクションに `experiment{N}_{description}` と記載

**実際の実装**:
- 実験IDは `exp[YYYYMMDDHHMMSS]_[description]` 形式（タイムスタンプ形式）
- 例: `exp20260106030720_baseline_tfidf_lr`
- 例: `exp20260112174906_keyword_tfidf_lr`

**修正が必要**: 実験IDの命名規則をタイムスタンプ形式に更新

---

### 2. ディレクトリ構造の説明が不正確

**experiment_flow_instructions.mdc（現在）**:
```
experiments/exp[timestamp]_[description]/
├── exp[timestamp]_config.yaml
├── exp[timestamp]_train.py
└── exp[timestamp]_predict.py

results/exp[timestamp]_[description]/
├── exp[timestamp]_metrics.json
├── exp[timestamp]_cv_results.json
├── exp[timestamp]_model.pkl
└── exp[timestamp]_submission.csv
```

**実際の実装**:
- ディレクトリ構造は正しいが、実験IDの形式が `exp[YYYYMMDDHHMMSS]_[description]` であることを明記すべき
- `results/` には `exp[timestamp]_report.md` も含まれる（Validatorが作成）

**修正が必要**: 実験IDの形式を明確化し、`exp[timestamp]_report.md` を追加

---

### 3. タスク読み取りのパスが記載されていない

**experiment_flow_instructions.mdc（現在）**:
- Plannerのタスク読み取りについての記載がない

**実際の実装**:
- Plannerは `tasks/current_sprint.json` からタスクを読み取る
- `scripts/workflow/task_loader.py` を使用

**修正が必要**: Plannerのタスク読み取り手順を追加

---

### 4. コミットメッセージの例が古い可能性

**experiment_flow_instructions.mdc（現在）**:
- コミットメッセージの例が記載されている
- スコープの例が記載されている

**実際の実装**:
- `.cursor/version_controller_rules.mdc` に詳細な規約が定義されている
- 規約は正しいが、参照先を明確化すべき

**修正が必要**: Version Controllerルールへの参照を明確化

---

### 5. 実験レポートの作成場所の説明が不足

**experiment_flow_instructions.mdc（現在）**:
- Validatorが実験レポートを作成すると記載されている
- しかし、`results/` ディレクトリに保存されることが明記されていない

**実際の実装**:
- 実験レポートは `results/exp[YYYYMMDDHHMMSS]_[description]/exp[timestamp]_report.md` に保存される

**修正が必要**: 実験レポートの保存場所を明確化

---

### 6. 関連タスク・プロジェクトの検索手順の詳細化

**experiment_flow_instructions.mdc（現在）**:
- 関連タスク・プロジェクトの検索手順が記載されている
- しかし、検索条件が具体的でない

**実際の実装**:
- 検索条件は記載されているが、より具体的な例を追加できる

**改善案**: 検索例を追加

---

### 7. エラーハンドリングセクションの誤字

**experiment_flow_instructions.mdc（現在）**:
- 行290に「１」という文字が誤って記載されている

**修正が必要**: 誤字を削除

---

### 8. 実験管理セクションの情報が古い

**experiment_flow_instructions.mdc（現在）**:
- 参考情報セクションに「命名規則: `experiment{N}_{description}`」と記載

**実際の実装**:
- 実験IDは `exp[YYYYMMDDHHMMSS]_[description]` 形式（タイムスタンプ形式）

**修正が必要**: 命名規則をタイムスタンプ形式に更新

---

## 可読性の問題と改善案

### 現在の問題点

1. **情報が散在**: 実験IDの命名規則が複数箇所に記載されているが、形式が統一されていない
2. **実装詳細の不足**: 実際のディレクトリ構造やファイル命名規則の説明が不足
3. **参照先の不明確さ**: 関連ドキュメントへの参照が散在している
4. **構成が長い**: ドキュメントが長く、必要な情報を見つけにくい

### 改善案：構成の再編成

#### 提案1: セクション構成の再編成

```markdown
# Experiment Flow Instructions for AI Agents

## 概要
- 実験実行フローの全体像
- エージェント間の連携

## 基本原則
- 役割の明確な分離
- 品質保証
- 情報の流れ

## Experiment実行フロー（詳細）
- 各ステップの詳細説明
- 実際のディレクトリ構造に基づいた説明

## エラーハンドリング
- 各ステップでの失敗時の対応
- エスカレーション手順

## 品質チェックポイント
- 各ステップ完了時の確認事項

## 次のステップへの引き継ぎ
- 各エージェントから次のエージェントへの引き継ぎ方法

## 参考情報
- 関連ドキュメント
- 実験管理（命名規則、ディレクトリ構造、結果記録）
- 品質保証
```

#### 提案2: 実験管理セクションの詳細化

- 実験IDの命名規則を明確化（タイムスタンプ形式）
- ディレクトリ構造の説明を詳細化
- ファイル命名規則の説明を追加

#### 提案3: 参照先の明確化

- 各エージェントの詳細ルールへの参照を明確化
- Version Controllerルールへの参照を明確化

---

## 改訂の優先順位

### 高優先度
1. 実験IDの命名規則の修正（`experiment{N}_{description}` → `exp[YYYYMMDDHHMMSS]_[description]`）
2. 実験管理セクションの命名規則の修正
3. エラーハンドリングセクションの誤字修正
4. 実験レポートの保存場所の明確化

### 中優先度
5. Plannerのタスク読み取り手順の追加
6. ディレクトリ構造の説明の詳細化
7. Version Controllerルールへの参照の明確化

### 低優先度
8. 構成の再編成（可読性向上）
9. 関連タスク・プロジェクトの検索例の追加




