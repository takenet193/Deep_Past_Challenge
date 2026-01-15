---
id: 20260112
title: LangChainベースマルチエージェントシステム実装プラン
author: takeikumi
type: reference
form: plan
tags: [langchain, multi-agent, architecture, implementation, kaggle, system-design]
links:
  - reference_experiment_workflow_comparison_20260105
created: 2026-01-12
updated: 2026-01-12
---

# LangChainベースマルチエージェントシステム実装プラン

## 概要

現在のCursor IDEベースのマルチエージェントシステムを、LangChain/LangGraphで再実装する際の詳細な実装プラン。現在のシステム仕様（`.cursor/experiment_flow_instructions.mdc`、`.cursor/kaggle_team.mdc`等）を完全に反映した設計。

---

## 現在のシステム仕様の分析

### 1. 実験フロー（7ステップ）

```
User → Document Manager → Planner → User → Developer → Validator → User → Validator → Document Manager → Version Controller
```

**重要なポイント**:
- **承認ゲート**: Planner → User → Developer（計画承認が必要）
- **双方向インタラクション**: Validator → User → Validator（結果入力）
- **厳密な役割分離**: 各エージェントは特定の出力形式のみ許可

### 2. 各エージェントの制約

| エージェント | 許可される出力 | 禁止される出力 |
|:---|:---|:---|
| **Planner** | `[Plan:]` と `[Action:]` のみ | コード生成、実装 |
| **Developer** | Pythonコードブロック、`[Result:]` | 評価ロジックの断定、長文考察、レポート作成 |
| **Validator** | 実験レポート（Markdown） | 学習/推論コードの再生成、実装差し替え |
| **Docs Manager** | Markdownレポート/要約 | Pythonコード生成 |
| **Version Controller** | Gitコマンドと説明 | Pythonコード生成 |

### 3. 実験管理の厳密なルール

- **実験ID**: タイムスタンプ形式（`expYYYYMMDDHHMMSS`）
- **全ファイルに実験ID付与**: ファイル名から実験を特定可能
- **config.yamlをSSOT**: 実験設定はconfig.yamlに集約
- **リポジトリルート基準の相対パス**: ポータビリティのため
- **乱数シード固定**: `random_state=42` で統一

### 4. 関連情報検索機能

- Validatorが関連タスク・プロジェクト・ノートを自動検索
- ユーザーに提案して確認
- レポートのYAMLフロントマターに記載

---

## LangChain実装プラン

### アーキテクチャ設計

```
src/
├── agents/
│   ├── base_agent.py              # ベースエージェントクラス
│   ├── planner_agent.py            # Plannerエージェント
│   ├── developer_agent.py         # Developerエージェント
│   ├── validator_agent.py          # Validatorエージェント
│   ├── docs_manager_agent.py      # Docs Managerエージェント
│   └── version_controller_agent.py # Version Controllerエージェント
├── tools/
│   ├── file_tools.py               # ファイル操作ツール
│   ├── task_tools.py               # タスク管理ツール（task_loader.py統合）
│   ├── experiment_tools.py         # 実験管理ツール
│   ├── knowledge_tools.py          # 知識管理ツール（関連情報検索）
│   └── git_tools.py                # Git操作ツール
├── chains/
│   ├── experiment_workflow_chain.py # 実験ワークフローチェーン
│   └── workflow_orchestrator.py    # ワークフローオーケストレーター（LangGraph）
├── memory/
│   ├── conversation_memory.py     # 会話メモリ
│   ├── state_memory.py            # 状態管理メモリ
│   └── experiment_state.py        # 実験状態管理
├── prompts/
│   ├── planner_prompt.py           # Planner用プロンプト（.mdcから生成）
│   ├── developer_prompt.py         # Developer用プロンプト
│   ├── validator_prompt.py         # Validator用プロンプト
│   ├── docs_manager_prompt.py     # Docs Manager用プロンプト
│   └── version_controller_prompt.py # Version Controller用プロンプト
├── validators/
│   ├── role_validator.py          # 役割違反検証
│   ├── output_validator.py         # 出力形式検証
│   └── experiment_validator.py    # 実験ルール検証
└── main.py                         # エントリーポイント
```

### 1. ワークフローオーケストレーター（LangGraph）

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Literal
from typing_extensions import TypedDict

class ExperimentWorkflowState(TypedDict):
    """実験ワークフローの状態"""
    # タスク情報
    task_id: str
    task_data: dict
    
    # 実験情報
    experiment_id: str | None
    experiment_config: dict | None
    
    # エージェント間の引き継ぎ情報
    current_step: Literal[
        "docs_manager_info_gathering",
        "planner_planning",
        "user_approval",
        "developer_implementation",
        "validator_evaluation",
        "user_result_input",
        "validator_report_creation",
        "docs_manager_documentation",
        "version_controller_commit"
    ]
    
    # 各ステップの出力
    docs_manager_output: dict | None
    planner_output: dict | None
    user_approval: bool | None
    developer_output: dict | None
    validator_evaluation_output: dict | None
    user_result_input: dict | None
    validator_report_output: dict | None
    docs_manager_final_output: dict | None
    
    # 関連情報
    related_tasks: list[str]
    related_projects: list[str]
    related_notes: list[str]
    
    # エラー情報
    error: str | None
    retry_count: int

class ExperimentWorkflowOrchestrator:
    """実験ワークフローオーケストレーター"""
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self):
        workflow = StateGraph(ExperimentWorkflowState)
        
        # ノード定義（7ステップ + 承認ゲート）
        workflow.add_node("docs_manager_info", self.docs_manager_info_node)
        workflow.add_node("planner_planning", self.planner_planning_node)
        workflow.add_node("user_approval_gate", self.user_approval_gate_node)
        workflow.add_node("developer_implementation", self.developer_implementation_node)
        workflow.add_node("validator_evaluation", self.validator_evaluation_node)
        workflow.add_node("user_result_input", self.user_result_input_node)
        workflow.add_node("validator_report", self.validator_report_node)
        workflow.add_node("docs_manager_documentation", self.docs_manager_documentation_node)
        workflow.add_node("version_controller_commit", self.version_controller_commit_node)
        
        # エントリーポイント
        workflow.set_entry_point("docs_manager_info")
        
        # エッジ定義（厳密な制御）
        workflow.add_edge("docs_manager_info", "planner_planning")
        workflow.add_edge("planner_planning", "user_approval_gate")
        
        # 承認ゲート（条件分岐）
        workflow.add_conditional_edges(
            "user_approval_gate",
            self._check_user_approval,
            {
                "approved": "developer_implementation",
                "rejected": "planner_planning",  # 差し戻し
                "end": END
            }
        )
        
        workflow.add_edge("developer_implementation", "validator_evaluation")
        workflow.add_edge("validator_evaluation", "user_result_input")
        workflow.add_edge("user_result_input", "validator_report")
        workflow.add_edge("validator_report", "docs_manager_documentation")
        workflow.add_edge("docs_manager_documentation", "version_controller_commit")
        workflow.add_edge("version_controller_commit", END)
        
        return workflow.compile()
    
    def _check_user_approval(self, state: ExperimentWorkflowState) -> str:
        """ユーザー承認の確認"""
        if state["user_approval"] is True:
            return "approved"
        elif state["user_approval"] is False:
            return "rejected"
        else:
            return "end"  # まだ承認待ち
```

### 2. エージェント定義（厳密な制約付き）

```python
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish

class RoleValidatorCallback(BaseCallbackHandler):
    """役割違反を検出するコールバック"""
    
    def __init__(self, agent_role: str, allowed_outputs: list[str]):
        self.agent_role = agent_role
        self.allowed_outputs = allowed_outputs
    
    def on_agent_action(self, action: AgentAction, **kwargs):
        """エージェントの行動を検証"""
        # 役割に応じた厳密な検証
        if self.agent_role == "planner":
            # Plannerはコード生成を試みてはいけない
            if "python" in action.tool.lower() or "code" in action.tool.lower():
                raise ValueError(f"Plannerはコード生成ツールを使用できません: {action.tool}")
        
        elif self.agent_role == "developer":
            # Developerはレポート作成ツールを使用できない
            if "report" in action.tool.lower() or "markdown" in action.tool.lower():
                raise ValueError(f"Developerはレポート作成ツールを使用できません: {action.tool}")
        
        elif self.agent_role == "validator":
            # Validatorはコード生成ツールを使用できない
            if "train" in action.tool.lower() or "predict" in action.tool.lower():
                raise ValueError(f"Validatorはコード生成ツールを使用できません: {action.tool}")

class BaseKaggleAgent:
    """ベースエージェントクラス（厳密な制約付き）"""
    
    def __init__(
        self,
        name: str,
        role: str,
        tools: list[Tool],
        llm,
        mdc_rules_path: str,
        allowed_outputs: list[str],
        forbidden_outputs: list[str]
    ):
        self.name = name
        self.role = role
        self.tools = tools
        self.llm = llm
        self.mdc_rules_path = mdc_rules_path
        self.allowed_outputs = allowed_outputs
        self.forbidden_outputs = forbidden_outputs
        
        # .mdcファイルからルールを読み込む
        self.rules = self._load_mdc_rules()
        
        # メモリ
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # コールバック（役割違反検出）
        self.callbacks = [
            RoleValidatorCallback(role, allowed_outputs)
        ]
        
        # エージェント作成
        self.agent = self._create_agent()
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True,
            callbacks=self.callbacks
        )
    
    def _load_mdc_rules(self) -> str:
        """.mdcファイルからルールを読み込む"""
        from pathlib import Path
        rules_path = Path(self.mdc_rules_path)
        if rules_path.exists():
            return rules_path.read_text(encoding="utf-8")
        return ""
    
    def _create_agent(self):
        """エージェントを作成"""
        prompt = self._build_prompt()
        return create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
    
    def _build_prompt(self):
        """プロンプトを構築（.mdcルールを含む）"""
        return ChatPromptTemplate.from_messages([
            ("system", f"""
あなたは{self.role}エージェントです。

## 役割定義
{self.rules}

## 制約
- 許可される出力: {', '.join(self.allowed_outputs)}
- 禁止される出力: {', '.join(self.forbidden_outputs)}
- 役割違反を検出した場合は即座に停止してください
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
```

### 3. ツール定義（既存システムとの統合）

```python
from langchain.tools import tool
from typing import List, Dict
from pathlib import Path
import yaml
import json

# 既存のtask_loader.pyを統合
from src.task_loader import (
    load_pending_tasks,
    load_task,
    format_task_for_planner
)

@tool
def load_pending_tasks_tool() -> str:
    """未処理タスクを読み込む（Planner用）"""
    tasks = load_pending_tasks()
    if not tasks:
        return "未処理タスクはありません"
    
    formatted = []
    for task in tasks:
        formatted.append(format_task_for_planner(task))
    
    return "\n\n".join(formatted)

@tool
def create_experiment_directory(experiment_id: str, description: str) -> str:
    """実験ディレクトリを作成（Developer用）"""
    from datetime import datetime
    
    # タイムスタンプ形式の検証
    if not experiment_id.startswith("exp") or len(experiment_id) != 18:
        raise ValueError(f"実験IDはタイムスタンプ形式（expYYYYMMDDHHMMSS）である必要があります: {experiment_id}")
    
    exp_dir = Path(f"experiments/{experiment_id}_{description}")
    results_dir = Path(f"results/{experiment_id}_{description}")
    
    exp_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # テンプレートからconfig.yamlをコピー
    template_config = Path("experiments/_template_experiment/config.yaml")
    if template_config.exists():
        config_content = template_config.read_text(encoding="utf-8")
        # 実験IDを置換
        config_content = config_content.replace("expYYYYMMDDHHMMSS", experiment_id)
        config_content = config_content.replace("YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))
        
        config_path = exp_dir / f"{experiment_id}_config.yaml"
        config_path.write_text(config_content, encoding="utf-8")
    
    return f"実験ディレクトリを作成しました: {exp_dir}"

@tool
def search_related_tasks(project: str, experiment_id: str) -> List[Dict]:
    """関連タスクを検索（Validator用）"""
    from pathlib import Path
    import frontmatter
    
    related_tasks = []
    
    # タイムスタンプを抽出（exp20260106030720 → 20260106030720）
    timestamp = experiment_id.replace("exp", "")
    
    # active/とcompleted/から検索
    for status_dir in ["active", "completed"]:
        tasks_dir = Path(f"knowledge/tasks/{status_dir}")
        if not tasks_dir.exists():
            continue
        
        for task_file in tasks_dir.glob("*.md"):
            try:
                with open(task_file, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)
                    metadata = post.metadata
                    
                    # 検索条件
                    if metadata.get("project") == project:
                        related_tasks.append({
                            "id": metadata.get("id"),
                            "title": metadata.get("title"),
                            "path": str(task_file)
                        })
                    elif timestamp in metadata.get("id", ""):
                        related_tasks.append({
                            "id": metadata.get("id"),
                            "title": metadata.get("title"),
                            "path": str(task_file)
                        })
            except Exception:
                continue
    
    return related_tasks

@tool
def search_related_projects(project_name: str) -> Dict | None:
    """関連プロジェクトを検索（Validator用）"""
    project_file = Path(f"knowledge/tasks/projects/project_{project_name}.md")
    if project_file.exists():
        return {
            "id": f"project-{project_name}",
            "path": str(project_file)
        }
    return None

@tool
def create_experiment_report(
    experiment_id: str,
    metrics: dict,
    related_tasks: list[str],
    related_projects: list[str],
    related_notes: list[str],
    user_result: dict
) -> str:
    """実験レポートを作成（Validator用）"""
    from datetime import datetime
    import frontmatter
    
    # タイムスタンプを抽出
    timestamp = experiment_id.replace("exp", "")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # YAMLフロントマター（knowledgeフォルダの様式に合わせる）
    frontmatter_data = {
        "id": timestamp,
        "title": f"Disaster Tweets - {experiment_id}",
        "author": "takeikumi",
        "type": "experiment_report",
        "experiment_id": experiment_id,
        "project": related_projects[0] if related_projects else "kaggle_disaster_tweets",
        "form": "report",
        "tags": ["kaggle", "kaggle_disaster_tweets", "experiment", "report"],
        "status": "completed",
        "metrics": metrics,
        "links": related_projects + related_tasks + related_notes,
        "created": date_str,
        "updated": date_str
    }
    
    # レポート本文（テンプレートから生成）
    report_content = f"""# Experiment: {experiment_id}

## 実験概要
...

## 結果
- CV Mean: {metrics.get('cv_mean')}
- Public LB: {user_result.get('public_lb')}
...
"""
    
    # フロントマター + 本文
    report = frontmatter.dumps(frontmatter.Post(report_content, **frontmatter_data))
    
    # ファイルに保存
    report_path = Path(f"results/{experiment_id}/exp{timestamp}_report.md")
    report_path.write_text(report, encoding="utf-8")
    
    return f"実験レポートを作成しました: {report_path}"
```

### 4. ユーザー承認ゲートの実装

```python
from langchain.schema import HumanMessage

class UserApprovalGate:
    """ユーザー承認ゲート"""
    
    def __init__(self):
        self.pending_approvals = {}
    
    def request_approval(self, plan: dict, context: dict) -> dict:
        """承認を要求"""
        approval_id = f"approval_{len(self.pending_approvals)}"
        self.pending_approvals[approval_id] = {
            "plan": plan,
            "context": context,
            "status": "pending"
        }
        
        return {
            "approval_id": approval_id,
            "message": f"""
以下の計画の承認をお願いします：

[Plan:]
{plan.get('plan', '')}

[Action:]
{plan.get('action', '')}

承認しますか？ (yes/no)
"""
        }
    
    def check_approval(self, approval_id: str) -> bool | None:
        """承認状態を確認"""
        if approval_id in self.pending_approvals:
            return self.pending_approvals[approval_id]["status"] == "approved"
        return None
    
    def set_approval(self, approval_id: str, approved: bool):
        """承認状態を設定"""
        if approval_id in self.pending_approvals:
            self.pending_approvals[approval_id]["status"] = "approved" if approved else "rejected"
```

### 5. 実験ルール検証

```python
class ExperimentRuleValidator:
    """実験ルールの検証"""
    
    @staticmethod
    def validate_experiment_id(experiment_id: str) -> bool:
        """実験IDの形式を検証"""
        if not experiment_id.startswith("exp"):
            return False
        if len(experiment_id) != 18:  # exp + 14桁
            return False
        try:
            datetime.strptime(experiment_id[3:], "%Y%m%d%H%M%S")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_file_naming(experiment_id: str, file_path: Path) -> bool:
        """ファイル名に実験IDが含まれているか検証"""
        return experiment_id in file_path.name
    
    @staticmethod
    def validate_config_yaml(experiment_id: str, config: dict) -> bool:
        """config.yamlの内容を検証"""
        if config.get("experiment", {}).get("id") != experiment_id:
            return False
        if "data" not in config:
            return False
        if "model" not in config:
            return False
        return True
```

---

## 実装の詳細設計

### 1. エージェント別の実装

#### Plannerエージェント

```python
class PlannerAgent(BaseKaggleAgent):
    """Plannerエージェント"""
    
    def __init__(self, llm):
        tools = [
            load_pending_tasks_tool(),
            # コード生成ツールは含めない
        ]
        
        super().__init__(
            name="planner",
            role="Kaggle Planner/Orchestrator",
            tools=tools,
            llm=llm,
            mdc_rules_path=".cursor/kaggle_team.mdc",
            allowed_outputs=["[Plan:]", "[Action:]"],
            forbidden_outputs=["Pythonコード", "実装コード"]
        )
    
    def plan(self, task_id: str) -> dict:
        """計画を立案"""
        # タスクを読み込む
        task = load_task(task_id)
        if not task:
            return {"error": f"タスクが見つかりません: {task_id}"}
        
        # エージェント実行
        result = self.executor.invoke({
            "input": f"タスク {task_id} の計画を立案してください。\n\n{format_task_for_planner(task)}"
        })
        
        # 出力を解析（[Plan:]と[Action:]を抽出）
        output = result["output"]
        plan_match = re.search(r'\[Plan:\](.*?)(?=\[Action:\]|$)', output, re.DOTALL)
        action_match = re.search(r'\[Action:\](.*?)$', output, re.DOTALL)
        
        return {
            "plan": plan_match.group(1).strip() if plan_match else "",
            "action": action_match.group(1).strip() if action_match else ""
        }
```

#### Developerエージェント

```python
class DeveloperAgent(BaseKaggleAgent):
    """Developerエージェント"""
    
    def __init__(self, llm):
        tools = [
            create_experiment_directory,
            # コード生成ツール（Python実行環境）
            # ファイル操作ツール
        ]
        
        super().__init__(
            name="developer",
            role="Kaggle Developer/Coder",
            tools=tools,
            llm=llm,
            mdc_rules_path=".cursor/kaggle_team.mdc",
            allowed_outputs=["Pythonコードブロック", "[Result:]"],
            forbidden_outputs=["評価ロジックの断定", "長文考察", "実験レポート"]
        )
    
    def implement(self, plan: dict) -> dict:
        """実装を実行"""
        # 実験IDを生成
        from datetime import datetime
        experiment_id = f"exp{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # エージェント実行
        result = self.executor.invoke({
            "input": f"""
以下の計画に基づいて実装してください：

[Plan:]
{plan.get('plan', '')}

[Action:]
{plan.get('action', '')}

実験ID: {experiment_id}
実験運用ルール: .cursor/developer_experiment_rules.mdc を参照してください。
"""
        })
        
        return {
            "experiment_id": experiment_id,
            "result": result["output"]
        }
```

#### Validatorエージェント

```python
class ValidatorAgent(BaseKaggleAgent):
    """Validatorエージェント"""
    
    def __init__(self, llm):
        tools = [
            search_related_tasks,
            search_related_projects,
            create_experiment_report,
            # 評価ツール（metrics.json読み込み等）
        ]
        
        super().__init__(
            name="validator",
            role="Kaggle Validator/Scorer",
            tools=tools,
            llm=llm,
            mdc_rules_path=".cursor/kaggle_team.mdc",
            allowed_outputs=["実験レポート（Markdown）"],
            forbidden_outputs=["学習/推論コードの再生成", "実装差し替え"]
        )
    
    def evaluate_and_create_report(
        self,
        experiment_id: str,
        user_result: dict
    ) -> dict:
        """評価とレポート作成"""
        # 関連情報を検索
        config_path = Path(f"experiments/{experiment_id}/exp{experiment_id}_config.yaml")
        config = yaml.safe_load(config_path.read_text())
        project = config.get("experiment", {}).get("tags", [""])[0]
        
        related_tasks = search_related_tasks(project, experiment_id)
        related_project = search_related_projects(project)
        
        # メトリクスを読み込む
        metrics_path = Path(f"results/{experiment_id}/exp{experiment_id}_metrics.json")
        metrics = json.loads(metrics_path.read_text())
        metrics["public_lb"] = user_result.get("public_lb")
        
        # エージェント実行
        result = self.executor.invoke({
            "input": f"""
実験 {experiment_id} の評価とレポート作成を行ってください。

メトリクス: {metrics}
関連タスク: {[t['id'] for t in related_tasks]}
関連プロジェクト: {related_project['id'] if related_project else None}

実験レポートのYAMLフロントマターはknowledgeフォルダの様式に合わせてください。
"""
        })
        
        return {
            "report_path": f"results/{experiment_id}/exp{experiment_id}_report.md",
            "result": result["output"]
        }
```

### 2. 状態管理と永続化

```python
from langchain.memory import ConversationSummaryBufferMemory
import pickle

class ExperimentStateManager:
    """実験状態の管理"""
    
    def __init__(self, state_file: Path = Path(".experiment_state.pkl")):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> ExperimentWorkflowState:
        """状態を読み込む"""
        if self.state_file.exists():
            with open(self.state_file, "rb") as f:
                return pickle.load(f)
        return ExperimentWorkflowState(
            task_id="",
            task_data={},
            experiment_id=None,
            experiment_config=None,
            current_step="docs_manager_info_gathering",
            docs_manager_output=None,
            planner_output=None,
            user_approval=None,
            developer_output=None,
            validator_evaluation_output=None,
            user_result_input=None,
            validator_report_output=None,
            docs_manager_final_output=None,
            related_tasks=[],
            related_projects=[],
            related_notes=[],
            error=None,
            retry_count=0
        )
    
    def save_state(self, state: ExperimentWorkflowState):
        """状態を保存"""
        with open(self.state_file, "wb") as f:
            pickle.dump(state, f)
    
    def reset_state(self):
        """状態をリセット"""
        if self.state_file.exists():
            self.state_file.unlink()
        self.state = self._load_state()
```

### 3. エラーハンドリングとリトライ

```python
class WorkflowErrorHandler:
    """ワークフローエラーハンドリング"""
    
    @staticmethod
    def handle_agent_error(
        agent_name: str,
        error: Exception,
        state: ExperimentWorkflowState
    ) -> dict:
        """エージェントエラーを処理"""
        # エラーログを記録
        error_log = {
            "agent": agent_name,
            "error": str(error),
            "step": state["current_step"],
            "timestamp": datetime.now().isoformat()
        }
        
        # リトライ可能か判断
        if state["retry_count"] < 3:
            return {
                "action": "retry",
                "error_log": error_log
            }
        else:
            # エスカレーション
            return {
                "action": "escalate",
                "error_log": error_log,
                "escalation_level": "user"
            }
```

---

## 現在のシステム（Cursor IDEベース）の評価

### 10段階評価

| 評価項目 | スコア | 評価理由 |
|:---|:---|:---|
| **厳密な制御** | **6/10** | .mdcファイルでルールを定義できるが、実行時検証が弱い。自己ロール推定に依存し、役割違反を検出しにくい。 |
| **可観測性** | **5/10** | Cursor IDE内での実行ログが限定的。エージェント間の引き継ぎが追跡しにくい。状態の永続化がない。 |
| **テスト容易性** | **4/10** | エージェントを個別にテストしにくい。ワークフローの統合テストが困難。再現性が低い。 |
| **拡張性** | **7/10** | .mdcファイルで簡単にルールを追加・変更できる。新しいエージェントの追加は手動だが可能。 |
| **自動化の可能性** | **5/10** | 手動でのエージェント切り替えが必要。ユーザー承認ゲートが手動。完全自動化は困難。 |
| **再現性** | **5/10** | 状態の保存・復元が困難。同じ実験の再実行が手動。実験IDとconfig.yamlで一部再現性は確保。 |
| **実装コスト** | **9/10** | 既に動作している。.mdcファイルで簡単にルールを定義。学習コストが低い。 |
| **複雑性** | **8/10** | シンプルで理解しやすい。.mdcファイルでルールを直接編集可能。コードベースが小さい。 |
| **Cursor IDEとの統合** | **10/10** | Cursor IDEと完全に統合。.mdcファイルでルールを直接編集。IDE内で直接実行可能。 |
| **パフォーマンス** | **9/10** | 軽量で高速。オーバーヘッドが少ない。即座に実行可能。 |
| **メンテナンス** | **8/10** | シンプルでメンテナンスが容易。.mdcファイルの編集のみ。依存関係が少ない。 |
| **学習曲線** | **9/10** | シンプルで理解しやすい。チームメンバーがすぐに使える。.mdcファイルの構造が直感的。 |
| **ユーザー体験** | **9/10** | Cursor IDE内で直接使用可能。自然な会話形式での操作。デバッグが容易。 |

### 総合評価

**総合スコア: 7.2/10**

**強み**:
- Cursor IDEとの完全統合（10/10）
- シンプルさと理解しやすさ（複雑性: 8/10、学習曲線: 9/10）
- 実装コストの低さ（9/10）
- パフォーマンス（9/10）
- メンテナンスの容易さ（8/10）

**弱み**:
- 厳密な制御の不足（6/10）
- 可観測性の低さ（5/10）
- テスト容易性の低さ（4/10）
- 自動化の限界（5/10）
- 再現性の課題（5/10）

### 評価の詳細

#### 高評価項目（8点以上）

1. **Cursor IDEとの統合（10/10）**
   - Cursor IDEと完全に統合されており、IDE内で直接使用可能
   - .mdcファイルでルールを直接編集できる
   - 自然な会話形式での操作が可能

2. **実装コスト（9/10）**
   - 既に動作しているシステム
   - .mdcファイルで簡単にルールを定義
   - 学習コストが低い

3. **パフォーマンス（9/10）**
   - 軽量で高速
   - オーバーヘッドが少ない
   - 即座に実行可能

4. **学習曲線（9/10）**
   - シンプルで理解しやすい
   - チームメンバーがすぐに使える
   - .mdcファイルの構造が直感的

5. **ユーザー体験（9/10）**
   - Cursor IDE内で直接使用可能
   - 自然な会話形式での操作
   - デバッグが容易

#### 中評価項目（6-7点）

1. **厳密な制御（6/10）**
   - .mdcファイルでルールを定義できるが、実行時検証が弱い
   - 自己ロール推定に依存し、役割違反を検出しにくい
   - エージェント間の遷移が明示的でない

2. **拡張性（7/10）**
   - .mdcファイルで簡単にルールを追加・変更できる
   - 新しいエージェントの追加は手動だが可能
   - ワークフローの変更が容易

#### 低評価項目（5点以下）

1. **可観測性（5/10）**
   - Cursor IDE内での実行ログが限定的
   - エージェント間の引き継ぎが追跡しにくい
   - 状態の永続化がない

2. **自動化の可能性（5/10）**
   - 手動でのエージェント切り替えが必要
   - ユーザー承認ゲートが手動
   - 完全自動化は困難

3. **再現性（5/10）**
   - 状態の保存・復元が困難
   - 同じ実験の再実行が手動
   - 実験IDとconfig.yamlで一部再現性は確保

4. **テスト容易性（4/10）**
   - エージェントを個別にテストしにくい
   - ワークフローの統合テストが困難
   - 再現性が低い

---

## メリットとデメリット

### メリット

#### 1. 厳密な制御

**現在のシステム**:
- Cursor IDEベースで、エージェントの役割違反を検出しにくい
- 自己ロール推定に依存（曖昧さが残る）

**LangChain実装**:
- **StateGraphでワークフローを厳密に定義**: エージェント間の遷移を強制
- **RoleValidatorCallbackで実行時検証**: 役割違反を即座に検出
- **型安全な状態管理**: TypedDictで状態の構造を保証
- **条件分岐の明確化**: 承認ゲートやユーザー入力待ちを明示的に定義

#### 2. 可観測性とデバッグ

**現在のシステム**:
- Cursor IDE内での実行ログが限定的
- エージェント間の引き継ぎが追跡しにくい

**LangChain実装**:
- **LangSmith統合**: 全実行ログを可視化
- **状態の永続化**: 途中で中断しても状態を復元可能
- **詳細なトレーシング**: 各エージェントの入出力を完全に記録
- **エラーの詳細な記録**: エラー発生時の状態を完全に保存

#### 3. テスト容易性

**現在のシステム**:
- エージェントを個別にテストしにくい
- ワークフローの統合テストが困難

**LangChain実装**:
- **単体テスト**: 各エージェントを独立してテスト可能
- **モックツール**: ツールをモックしてテスト可能
- **統合テスト**: ワークフロー全体をテスト可能
- **再現性**: 同じ状態で同じ結果を再現可能

#### 4. 拡張性

**現在のシステム**:
- 新しいエージェントの追加が手動
- ワークフローの変更が困難

**LangChain実装**:
- **ツールの追加が容易**: 新しいツールを簡単に追加
- **エージェントの追加が容易**: 新しいエージェントを簡単に追加
- **ワークフローの柔軟な変更**: StateGraphでワークフローを柔軟に変更
- **チェーンの組み合わせ**: 複雑なワークフローを構築可能

#### 5. 自動化の可能性

**現在のシステム**:
- 手動でのエージェント切り替えが必要
- ユーザー承認ゲートが手動

**LangChain実装**:
- **完全自動化の可能性**: ワークフローを完全に自動実行可能
- **スケジューリング**: 定期的な実験実行をスケジュール可能
- **並列実行**: 独立した実験を並列実行可能

#### 6. 再現性

**現在のシステム**:
- 状態の保存・復元が困難
- 同じ実験の再実行が手動

**LangChain実装**:
- **状態の永続化**: 実験状態を完全に保存・復元可能
- **再現性の保証**: 同じ入力で同じ結果を再現可能
- **実験の再実行**: 保存した状態から再実行可能

### デメリット

#### 1. 実装コスト

**現在のシステム**:
- 既に動作している
- .mdcファイルで簡単にルールを定義

**LangChain実装**:
- **完全な再実装が必要**: 既存システムを置き換える必要がある
- **学習コスト**: LangChain/LangGraphの学習が必要
- **初期実装に時間がかかる**: 推定2-4週間の開発期間
- **既存システムとの互換性**: 移行期間中の二重管理が必要

#### 2. 複雑性の増加

**現在のシステム**:
- シンプルで理解しやすい
- .mdcファイルでルールを直接編集可能

**LangChain実装**:
- **コードベースが大きくなる**: 推定2000-3000行のコード
- **依存関係が増える**: LangChain、LangGraph、LangSmith等
- **デバッグが難しくなる**: 複雑なワークフローグラフのデバッグ
- **メンテナンスコスト**: より多くのコードをメンテナンスする必要がある

#### 3. Cursor IDEとの統合

**現在のシステム**:
- Cursor IDEと完全に統合
- .mdcファイルでルールを直接編集
- IDE内で直接実行可能

**LangChain実装**:
- **Cursor IDEとの統合が困難**: 別の実行環境が必要になる可能性
- **.mdcファイルの活用が限定的**: プロンプト生成に変換する必要がある
- **IDE内での直接実行が困難**: コマンドライン実行が必要になる可能性

#### 4. パフォーマンス

**現在のシステム**:
- 軽量で高速
- オーバーヘッドが少ない

**LangChain実装**:
- **LangChainのオーバーヘッド**: フレームワークのオーバーヘッド
- **状態管理のオーバーヘッド**: 状態の保存・読み込みに時間がかかる
- **実行速度が遅くなる可能性**: 推定20-30%の速度低下

#### 5. メンテナンス

**現在のシステム**:
- シンプルでメンテナンスが容易
- .mdcファイルの編集のみ

**LangChain実装**:
- **LangChainのバージョンアップ対応**: 定期的なバージョンアップ対応が必要
- **依存関係の管理**: 複雑な依存関係の管理が必要
- **既存システムとの二重管理**: 移行期間中の二重管理が必要

#### 6. 学習曲線

**現在のシステム**:
- シンプルで理解しやすい
- チームメンバーがすぐに使える

**LangChain実装**:
- **LangChainの学習が必要**: チームメンバーの学習が必要
- **移行コスト**: 既存のワークフローからの移行コスト
- **ドキュメントの更新**: 新しいシステムのドキュメント作成が必要

#### 7. ユーザー体験

**現在のシステム**:
- Cursor IDE内で直接使用可能
- 自然な会話形式での操作

**LangChain実装**:
- **別のインターフェースが必要**: コマンドラインやWeb UIが必要になる可能性
- **操作が複雑になる可能性**: ワークフローの理解が必要
- **デバッグが困難**: エラー時の対処が複雑になる可能性

---

## 推奨アプローチ

### ハイブリッドアプローチ（推奨）

現在のシステムの強みを活かしつつ、LangChainの利点を取り入れる：

#### フェーズ1: 選択的実装（1-2週間）

**実装すべき部分**:
1. **実験実行チェーン（Developer → Validator）**
   - 最も厳密な制御が必要な部分
   - 実験ルールの検証が重要
   - LangChainで実装して厳密に制御

2. **関連情報検索の自動化**
   - Validatorの関連タスク・プロジェクト検索
   - LangChainツールとして実装
   - 既存システムから呼び出し可能

3. **状態管理とエラーハンドリング**
   - 実験状態の永続化
   - エラーの詳細な記録
   - リトライ機能

**既存システムを維持する部分**:
- Planner、Docs Manager、Version ControllerはCursorベースのまま
- ユーザー承認ゲートは手動のまま（明確性のため）

#### フェーズ2: 統合レイヤー（1週間）

1. **.mdcファイルからLangChainプロンプトへの変換スクリプト**
   ```python
   def convert_mdc_to_prompt(mdc_path: str) -> str:
       """.mdcファイルをLangChainプロンプトに変換"""
       # .mdcファイルを読み込んでプロンプト形式に変換
   ```

2. **Cursor IDEからLangChainエージェントの呼び出し**
   ```python
   # Cursor IDE内で使用可能なラッパー
   def run_langchain_agent(agent_name: str, input: str):
       """Cursor IDEからLangChainエージェントを呼び出し"""
   ```

3. **既存ツールとの統合**
   - `src/task_loader.py`をLangChainツールとして統合
   - 既存の実験管理スクリプトをツール化

#### フェーズ3: 段階的移行（2-4週間）

1. **並行運用期間**
   - 既存システムとLangChainシステムを並行運用
   - 比較検証

2. **段階的移行**
   - 成功した部分から順次移行
   - 問題があれば既存システムに戻す

3. **完全移行（オプション）**
   - すべての機能がLangChainで実装されたら完全移行
   - または、ハイブリッドのまま運用

### 完全実装アプローチ（非推奨）

**理由**:
- 実装コストが高い
- 既存システムの強みを失う
- Cursor IDEとの統合が困難
- リスクが高い

---

## 実装優先度

### 高優先度（実装すべき）

1. **実験実行チェーン（Developer → Validator）**
   - 厳密な制御が必要
   - 実験ルールの検証が重要
   - 実装コスト: 中、効果: 高

2. **関連情報検索の自動化**
   - Validatorの機能強化
   - 既存システムから呼び出し可能
   - 実装コスト: 低、効果: 中

3. **状態管理とエラーハンドリング**
   - 実験の再現性向上
   - デバッグの容易化
   - 実装コスト: 中、効果: 中

### 中優先度（検討すべき）

1. **タスク管理チェーン（Planner → Developer）**
   - ワークフローの一部自動化
   - 実装コスト: 高、効果: 中

2. **完全なワークフローオーケストレーション**
   - 7ステップ全体の自動化
   - 実装コスト: 高、効果: 高

### 低優先度（将来検討）

1. **完全なLangChain移行**
   - 既存システムの完全置き換え
   - 実装コスト: 非常に高、効果: 中

2. **並列実行の最適化**
   - 複数実験の並列実行
   - 実装コスト: 高、効果: 低（現時点では不要）

---

## 結論

### 推奨: ハイブリッドアプローチ

**理由**:
1. **既存システムの強みを活かす**: Cursor IDEとの統合、シンプルさ、理解しやすさ
2. **LangChainの利点を取り入れる**: 厳密な制御、可観測性、テスト容易性
3. **リスクを最小化**: 段階的な実装でリスクを管理
4. **実装コストを抑える**: 必要な部分のみ実装

### 実装ロードマップ

**Week 1-2: 選択的実装**
- 実験実行チェーン（Developer → Validator）のLangChain実装
- 関連情報検索の自動化
- 状態管理とエラーハンドリング

**Week 3: 統合レイヤー**
- .mdcファイルからLangChainプロンプトへの変換
- Cursor IDEからの呼び出しラッパー
- 既存ツールとの統合

**Week 4-6: 段階的移行**
- 並行運用と比較検証
- 問題の修正と改善
- 段階的な移行

### 最終判断

**現時点での推奨**: **ハイブリッドアプローチで選択的実装**

- 既存システムの強み（Cursor IDE統合、シンプルさ）を維持
- LangChainの利点（厳密な制御、可観測性）を取り入れる
- リスクを最小化しつつ、段階的に改善

**完全移行は将来検討**: ハイブリッドアプローチで十分な効果が得られ、完全移行の必要性が確認された場合に検討

---

## 参考資料

- LangChain公式ドキュメント: https://python.langchain.com/
- LangGraph公式ドキュメント: https://langchain-ai.github.io/langgraph/
- LangSmith: https://smith.langchain.com/
- 現在のシステム仕様:
  - `.cursor/kaggle_team.mdc`
  - `.cursor/experiment_flow_instructions.mdc`
  - `.cursor/developer_experiment_rules.mdc`
  - `.cursor/docs_manager_rules.mdc`

