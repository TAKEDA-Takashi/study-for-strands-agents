"""
03_complex_dag_workflow.py - 複雑なDAGワークフロー

シーケンシャルと並列を組み合わせた複雑な依存関係を持つワークフロー。
タスクごとに異なる優先度やタイムアウトを設定。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import workflow

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

agent = Agent(
    model=model,
    system_prompt="""あなたはワークフロー管理の専門家です。
workflowツールを使って複雑なタスクを整理し、効率的に実行してください。

タスクの依存関係を適切に設定し、DAG（有向非巡回グラフ）として
ワークフローを構築してください。""",
    tools=[workflow],
)

print("=== 複雑なDAGワークフローの作成 ===")
print("タスク: ソフトウェアリリースプロセス\n")

result = agent("""
ソフトウェアリリースのワークフローを作成してください（実行はまだしないでください）。
workflow_id は "release_process"、action は "create" です。

以下のDAG構造でタスクを定義してください:

フェーズ1（開始）:
- task_id: requirements, description: 要件定義, priority: 5

フェーズ2（並列、requirementsに依存）:
- task_id: frontend_dev, description: フロントエンド開発, dependencies: ["requirements"]
- task_id: backend_dev, description: バックエンド開発, dependencies: ["requirements"]
- task_id: api_design, description: API設計, dependencies: ["requirements"]

フェーズ3（部分的な依存）:
- task_id: integration, description: 統合, dependencies: ["frontend_dev", "backend_dev"]
- task_id: api_impl, description: API実装, dependencies: ["api_design", "backend_dev"]

フェーズ4:
- task_id: testing, description: テスト実行, dependencies: ["integration", "api_impl"], priority: 5

フェーズ5:
- task_id: release, description: リリース, dependencies: ["testing"], priority: 5
""")

print("=== 結果 ===")
print(result)
