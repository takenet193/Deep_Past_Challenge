---
type: memo
status: inbox
author: takeikumi
created: 2026-01-08
updated: 2026-01-08
tags: [workflow, agent]
links: []
---

# ワークフローは二つある

## 学び / 気づき
- ワークフローは二つある
  - experiment
  - chore
- それぞれエージェントにフローを事前に指示しておく

## 事実 / 観察

### 1. エクスペリメントワークフロー
- **定義済みドキュメント**: 
  - `.cursor/kaggle_team.mdc`
  - `.cursor/experiment_flow_instructions.mdc`
- **流れ**: モデル学習から解答提出までの一連の流れ
- **プロセス**:
  1. アイディア受領・情報収集 (Document Manager)
  2. 計画立案 (Planner)
  3. 計画承認 (User)
  4. 実装・実行 (Developer)
  5. 結果入力依頼・レポート作成 (Validator)
  6. ドキュメント化 (Document Manager)
  7. バージョン管理 (Version Controller)

### 2. タスクワークフロー（cchore）
- **流れ**: マスターノートで管理されたタスクの実行フロー
- **プロセス**:
  1. マスターノートで管理されたタスクをAIに渡す
  2. AIが作業を実行する
  3. 作業完了後、ステータスを変更する
  4. 結果報告をタスクノートに書き込む
- **定義**: 今後、エージェントに事前指示するドキュメントを作成する必要がある

## 次に試すこと
- タスクワークフロー（cohre）の詳細な定義ドキュメント作成

