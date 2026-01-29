# Kaggle Competition 

Kaggleコンペ参加のための統合的な開発環境

知識管理（Zettelkasten + GTD）、マルチエージェントシステム、実験管理を統合したワークフローを実現します。

## 概要

### プロジェクトの目的

- **知識の有機的循環**: 実験結果→知識蓄積→タスク生成→新たな実験のサイクル ✅ 実装済み
- **効率的なチーム開発**: リアルタイムな情報共有と進捗の可視化 ✅ 実装済み
- **半自動化された実験フロー**: マルチエージェントによる実験の自動実行 ✅ 実装済み
- **スケーラブルなMLOps**: 将来的な本格運用への拡張性 ⏳ 将来実装

### 実装状況（2026年1月時点）

| コンポーネント | 実装状況 | 主要機能 |
|:---|:---|:---|
| 1. 知識・タスクデータベース | ✅ 実装済み | Obsidian、Zettelkasten、GTD |
| 2. JSON形式タスク管理 | ✅ 実装済み | task_converter.py、task_loader.py、sync_project_links.py |
| 3. マルチエージェントシステム | ✅ 実装済み | Planner、Developer、Validator、Docs Manager、Version Controller |
| 4. 実験・結果管理 | ✅ 実装済み | experiments/、results/、テンプレートシステム |
| 5. MLOpsパイプライン | ⏳ 未実装 | GitHub Actions、MLflow、W&B、DVC |
| 監視スクリプトシステム | ⏳ 未実装 | task_watcher.py、knowledge_watcher.py等 |

---

## クイックスタート

### 1. セットアップ

```bash
# 依存関係のインストール
pip install -r requirements.txt

# ディレクトリの作成
mkdir -p knowledge/{inbox,zettelkasten/{permanent,references,structure,index},tasks/{active,waiting,someday,completed,archive,projects/{archive}},templates}
mkdir -p tasks experiments results data/{raw,processed} scripts

# Obsidianの設定
# knowledge/ ディレクトリをObsidianのVaultとして開く
```

### 2. 最初の実験を実行する

1. 実験テンプレートをコピー:
   ```bash
   cp -r experiments/_template_experiment experiments/exp$(date +%Y%m%d%H%M%S)_my_first_experiment
   ```

2. 設定ファイルを編集:
   - `experiments/exp[timestamp]_my_first_experiment/exp[timestamp]_config.yaml` を編集

3. 実験を実行:
   ```bash
   cd experiments/exp[timestamp]_my_first_experiment
   python exp[timestamp]_train.py
   ```

詳細は `docs/workflow_guide.md` を参照してください。

---

## プロジェクト構成

### ✅ 実装済みコンポーネント

### 1. 知識とタスクのデータベース
- **Zettelkasten**: 知識ノートの管理（`knowledge/zettelkasten/`）
  - `permanent/`: 永続的な知識ノート
  - `references/`: 外部資料の要約やリンク
  - `structure/`: システム構造や設計に関するノート
  - `index/`: 知識ノートのインデックス
- **GTD**: タスク管理（`knowledge/tasks/`）
  - `active/`: アクティブなタスク
  - `waiting/`: 待機中タスク
  - `someday/`: いつかやるタスク
  - `completed/`: 完了タスク
  - `projects/`: プロジェクト（複数タスクの集合）
- **Inbox**: 未整理の情報（`knowledge/inbox/`）
- Obsidianで編集、Gitで管理

### 2. JSON形式タスク管理
- `scripts/workflow/task_converter.py`: MarkdownタスクをJSONに変換
- `scripts/workflow/task_loader.py`: タスクJSONを読み込むユーティリティ
- `scripts/workflow/sync_project_links.py`: プロジェクトとタスクの相互リンクを同期
- `tasks/current_sprint.json`: タスクのSSOTスナップショット（生成物だがGit管理）

### 3. マルチエージェントシステム
- **Planner**: タスク分解・計画立案
- **Developer**: 実装（実験コードと結果ファイルの作成）
- **Validator**: 評価と実験レポート作成
- **Docs Manager**: 文書化
- **Version Controller**: Git管理

詳細は `.cursor/kaggle_team.mdc` を参照してください。

### 4. 実験・結果管理
- **実験ディレクトリ**: `experiments/exp[YYYYMMDDHHMMSS]_[description]/`
  - `exp[timestamp]_config.yaml`: 実験設定ファイル
  - `exp[timestamp]_train.py`: 学習スクリプト
  - `exp[timestamp]_predict.py`: 推論スクリプト
- **結果ディレクトリ**: `results/exp[YYYYMMDDHHMMSS]_[description]/`
  - `exp[timestamp]_metrics.json`: 評価指標
  - `exp[timestamp]_cv_results.json`: CV結果
  - `exp[timestamp]_submission.csv`: 提出ファイル
  - `exp[timestamp]_model.pkl`: モデルファイル（Git管理対象外）
  - `exp[timestamp]_report.md`: 実験レポート
- **テンプレート**: `experiments/_template_experiment/`, `results/_template_experiment/`

### ⏳ 将来実装予定コンポーネント

### 5. MLOpsパイプライン
- GitHub Actionsによる自動実験実行
- MLflowによる実験管理
- Weights & Biasesによる可視化
- DVCによるデータバージョン管理

詳細は `docs/project_architecture.md` の「将来実装機能の詳細設計」セクションを参照してください。

### 監視スクリプトシステム
- `task_watcher.py`: タスクファイルの変更を監視
- `knowledge_watcher.py`: 知識ノートの変更を監視
- `experiment_watcher.py`: 実験ファイルの変更を監視
- `results_watcher.py`: 結果ファイルの変更を監視

---

## ディレクトリ構造

```
.
├── .cursor/                          # Cursor設定（エージェント定義）
│   ├── kaggle_team.mdc               # エージェント定義（チーム憲法）
│   ├── experiment_flow_instructions.mdc  # 実験フロー指示
│   ├── developer_experiment_rules.mdc    # Developer運用ルール
│   ├── docs_manager_rules.mdc            # Docs Manager運用ルール
│   └── version_controller_rules.mdc      # Version Controller運用ルール
│
├── knowledge/                         # Obsidian知識ベース
│   ├── inbox/                        # 未整理の情報
│   │   ├── _inbox_guide.md
│   │   └── archive/                  # 処理済みInboxのアーカイブ
│   │
│   ├── zettelkasten/                 # 知識ノート（永続的）
│   │   ├── _zettelkasten_guide.md
│   │   ├── permanent/                # 永続的な知識ノート
│   │   ├── references/               # 外部資料の要約やリンク
│   │   ├── structure/                # システム構造や設計に関するノート
│   │   └── index/                    # 知識ノートのインデックス
│   │
│   ├── tasks/                        # GTDタスク管理
│   │   ├── _gtd_guide.md
│   │   ├── _MASTER_TASKS.md          # 全タスクのマスターリスト（Dataview用）
│   │   ├── active/                   # アクティブなタスク
│   │   ├── waiting/                  # 待機中タスク
│   │   ├── someday/                  # いつかやるタスク
│   │   ├── completed/                # 完了タスク
│   │   ├── archive/                  # 完了済みタスクのアーカイブ
│   │   └── projects/                 # プロジェクト（複数タスクの集合）
│   │       └── archive/              # 完了済みプロジェクトのアーカイブ
│   │
│   └── templates/                    # 各種テンプレート
│       ├── inbox/
│       ├── tasks/
│       └── zettelkasten/
│
├── tasks/                            # タスクJSON（エージェント用・生成物だがGit管理）
│   └── current_sprint.json           # `knowledge/tasks/` を集約したSSOTスナップショット
│
├── data/                             # データ
│   ├── raw/                          # Kaggleからの生データ
│   └── processed/                    # 加工済みデータ
│
├── experiments/                      # 実験ディレクトリ
│   ├── _template_experiment/         # 実験テンプレート
│   │   ├── config.yaml
│   │   └── README.md
│   └── exp[YYYYMMDDHHMMSS]_[description]/  # 実験ディレクトリ（タイムスタンプ形式）
│       ├── exp[timestamp]_config.yaml
│       ├── exp[timestamp]_train.py
│       └── exp[timestamp]_predict.py
│
├── results/                         # 実験結果ディレクトリ
│   ├── _template_experiment/        # 結果テンプレート
│   └── exp[YYYYMMDDHHMMSS]_[description]/  # 結果ディレクトリ
│       ├── exp[timestamp]_metrics.json
│       ├── exp[timestamp]_cv_results.json
│       ├── exp[timestamp]_submission.csv
│       ├── exp[timestamp]_model.pkl  # Git管理対象外
│       └── exp[timestamp]_report.md
│
├── scripts/                          # スクリプト
│   ├── workflow/                    # ワークフロー管理用
│   │   ├── task_converter.py        # タスク変換ツール（Markdown → JSON）
│   │   ├── task_loader.py           # タスク読み込みツール
│   │   └── sync_project_links.py    # プロジェクトリンク同期ツール
│   └── kaggle/                      # Kaggle提出用
│       ├── check_kaggle_auth.sh
│       ├── submit_to_kaggle.sh
│       └── submit_with_token.sh
│
├── docs/                             # ドキュメント
│   ├── project_architecture.md       # プロジェクト全体アーキテクチャ
│   ├── workflow_guide.md            # ワークフローガイド
│   ├── scripts_guide.md             # スクリプトガイド
│   ├── inconsistencies_to_fix.md    # 実装との不一致リスト
│   └── portfolio_evaluation.md      # ポートフォリオ評価
│
└── mcp_setup/                        # MCP設定（将来実装）
```

---

## ワークフロー

### 1. 知識収集
Obsidianで知識ノートを作成（Zettelkasten形式）
- `knowledge/zettelkasten/permanent/`: 永続的な知識ノート
- `knowledge/zettelkasten/references/`: 外部資料の要約

### 2. タスク生成
- `knowledge/inbox/` にタスク/アイデア/メモを追加（共通Inbox）
- タスクとして採用する場合は `knowledge/tasks/{active|waiting|someday}/` に **コピーしてSSOT化**
- 元のInboxファイルは `knowledge/inbox/archive/` に移動

### 3. タスク変換
```bash
python scripts/workflow/task_converter.py
```
`knowledge/tasks/` を集約し、`tasks/current_sprint.json` を生成（上書き）します。
（このJSONは**手編集しない**）

### 4. プロジェクトリンク同期（タスク確定時）
```bash
python scripts/workflow/sync_project_links.py
```
タスクに `project` フィールドが設定されている場合、プロジェクトノートとタスクファイルの相互リンクを更新します。

### 5. エージェント実行
Plannerが `tasks/current_sprint.json` を読み取り、各エージェントに割り当て
- **Developer**: 実験コードと結果ファイルの作成
- **Validator**: 評価と実験レポート作成
- **Docs Manager**: 文書化
- **Version Controller**: Git管理

### 6. 結果記録
- 実験結果を知識ノートに反映
- タスクを `knowledge/tasks/completed/` に移動

### 7. フィードバックループ
学びから新しい知識ノートを作成

詳細は `docs/workflow_guide.md` を参照してください。

---

## 使い方

### タスクの作成から実行まで

1. **知識ノートの作成**
   - `knowledge/zettelkasten/permanent/` に新しいノートを作成
   - タイムスタンプベースのIDで命名（例: `20240101000000_kaggle_basics.md`）

2. **タスクの生成**
   - `knowledge/inbox/` にタスク/アイデア/メモを追加（共通Inbox）
   - タスクとして採用する場合は `knowledge/tasks/{active|waiting|someday}/` に **コピーしてSSOT化**
   - 元のInboxファイルは `knowledge/inbox/archive/` に移動

3. **タスクの変換**
   ```bash
   python scripts/workflow/task_converter.py
   ```

4. **プロジェクトリンク同期**（タスクに `project` フィールドがある場合）
   ```bash
   python scripts/workflow/sync_project_links.py
   ```

5. **エージェント実行**
   - Plannerが `tasks/current_sprint.json` からタスクを読み取り
   - タスクを分解し、各エージェントに割り当て

6. **結果の記録**
   - 実験結果を知識ノートに反映
   - タスクを `knowledge/tasks/completed/` に移動

### 実験の作成と実行

1. **実験テンプレートをコピー**
   ```bash
   cp -r experiments/_template_experiment experiments/exp$(date +%Y%m%d%H%M%S)_my_experiment
   ```

2. **設定ファイルを編集**
   - `experiments/exp[timestamp]_my_experiment/exp[timestamp]_config.yaml` を編集
   - 実験ID、データパス、前処理、特徴量、モデル、CV方式を設定

3. **学習スクリプトを実行**
   ```bash
   cd experiments/exp[timestamp]_my_experiment
   python exp[timestamp]_train.py
   ```

4. **結果の確認**
   - `results/exp[timestamp]_my_experiment/` に結果ファイルが生成される
   - `exp[timestamp]_metrics.json`: 評価指標
   - `exp[timestamp]_cv_results.json`: CV結果
   - `exp[timestamp]_submission.csv`: 提出ファイル

5. **実験レポートの作成**
   - Validatorエージェントが `exp[timestamp]_report.md` を作成
   - または手動で `results/_template_experiment/expYYYYMMDDHHMMSS_report.md` をコピーして編集

詳細は `.cursor/developer_experiment_rules.mdc` を参照してください。

---

## セットアップ（詳細）

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. ディレクトリの作成

```bash
mkdir -p knowledge/{inbox,zettelkasten/{permanent,references,structure,index},tasks/{active,waiting,someday,completed,archive,projects/{archive}},templates} \
  tasks experiments results data/{raw,processed} scripts
```

### 3. Obsidianの設定

1. `knowledge/` ディレクトリをObsidianのVaultとして開く
2. 推奨プラグイン:
   - **Dataview**: タスク一覧の動的表示
   - **Templater**: テンプレート機能
   - **Git**: 自動コミット・プッシュ

### 4. テンプレートの使用方法

- **実験テンプレート**: `experiments/_template_experiment/` をコピーして使用
- **結果テンプレート**: `results/_template_experiment/` をコピーして使用
- **知識ノートテンプレート**: `knowledge/templates/zettelkasten/` を参照
- **タスクテンプレート**: `knowledge/templates/tasks/` を参照

---

## ドキュメント

### 主要ドキュメント

- **プロジェクト全体アーキテクチャ**: `docs/project_architecture.md`
- **ワークフローガイド**: `docs/workflow_guide.md`
- **スクリプトガイド**: `docs/scripts_guide.md`

### エージェント指示書（.cursor/）

- **エージェント定義（チーム憲法）**: `.cursor/kaggle_team.mdc`
- **実験フロー指示**: `.cursor/experiment_flow_instructions.mdc`
- **Developer 実験運用ルール**: `.cursor/developer_experiment_rules.mdc`
- **Docs Manager ルール**: `.cursor/docs_manager_rules.mdc`
- **Version Controller ルール**: `.cursor/version_controller_rules.mdc`


---

## ライセンス

（必要に応じて追加）
