# JSON形式タスク管理システム

## 概要

ObsidianのGTDタスクをJSON形式に変換し、マルチエージェントシステムに引き渡す仕組み。
SSOT（`knowledge/tasks/`）から `scripts/workflow/task_converter.py` で
`tasks/current_sprint.json` を生成します。

## 実装済み機能

### タスクJSON スキーマ

```json
{
  "generated_at": "2026-01-14T01:21:11",
  "tasks": [
    {
      "id": "task-20260112173705",
      "title": "Disaster Tweets: keyword特徴量の追加実験",
      "type": "task",
      "status": "in_progress",
      "priority": "high",
      "mode": "experiment",
      "project": "kaggle_disaster_tweets_baseline_improvement",
      "assigned_agent": null,
      "assignee": null,
      "context": [
        "project_kaggle_disaster_tweets_baseline_improvement",
        "project_kaggle_disaster_tweets"
      ],
      "dependencies": [
        "exp20260106030720_report"
      ],
      "related_notes": [
        "disaster_tweets_baseline_improvement_ideas_20260112162435",
        "exp20260106030720_report"
      ],
      "source_file": "knowledge/tasks/active/task_disaster_tweets_keyword_feature_20260112173705.md",
      "tags": [
        "kaggle",
        "kaggle_disaster_tweets",
        "improvement",
        "experiment"
      ],
      "due_date": null,
      "updated_at": "2026-01-12T00:00:00"
    }
  ]
}
```

### タスク変換スクリプト

**実装ファイル**: `scripts/workflow/task_converter.py`

**機能**:
- `knowledge/tasks/{active|waiting|someday|completed}/` 配下のMarkdownファイルを読み込み
- YAMLフロントマターからタスク情報を抽出
- `tasks/current_sprint.json` に変換・出力
- タスクは優先度・ステータス・期日・更新日時でソート

**使用方法**:
```bash
python scripts/workflow/task_converter.py
```

**出力**: `tasks/current_sprint.json`（AIエージェント向けのタスク定義ファイル）

**実装済みの主要機能**:
- Markdownパース（YAML frontmatter対応）
- ステータス変換（ディレクトリ名 → JSONステータス）
- ソート機能（優先度・ステータス・期日・更新日時）
- エラーハンドリング（パースエラーファイルのスキップ）

### 関連スクリプト

- `scripts/workflow/task_loader.py`: タスクJSONを読み込むユーティリティ
- `scripts/workflow/sync_project_links.py`: プロジェクトとタスク間のリンクを自動同期

## 将来実装予定

### タスク優先度計算と計算資源割り当て

タスクの優先度と計算資源を考慮した実行計画の立案機能。W&B (Weights & Biases) との統合も検討。

詳細は「[将来実装機能の詳細設計](../future_features.md)」セクションを参照してください。

## 関連ドキュメント

- [プロジェクトアーキテクチャ](../project_architecture.md) - システム設計の概要
- [システム概要](../system_overview.md) - システム全体の概要
- [知識・タスクデータベース](./knowledge_database.md) - 知識管理システムの詳細
- [マルチエージェントシステム](./multi_agent_system.md) - エージェントシステムの詳細

