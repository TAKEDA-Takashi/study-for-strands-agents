"""
01_basic_workflow.py - 基本的なワークフロー

workflowツールを使って、依存関係のあるタスクを順番に実行する。
strands_toolsのworkflowはエージェントが使用するツール。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import workflow

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# workflowツールを持つエージェント
agent = Agent(
    model=model,
    system_prompt="""あなたはワークフロー管理の専門家です。
workflowツールを使ってタスクを整理し、効率的に実行してください。

ワークフローの作成時は以下の形式を使用してください:
- action: "create" でワークフローを作成
- workflow_id: ワークフローの識別子
- tasks: タスクのリスト（task_id, description, dependencies を含む）

タスクの依存関係を適切に設定し、順序立てて実行してください。""",
    tools=[workflow],
)

# ワークフローの作成
print("=== 基本的なワークフローの作成 ===")
print("タスク: レポート作成（調査→分析→執筆）\n")

result = agent("""
以下の3つのタスクをワークフローとして作成してください（実行はまだしないでください）。

1. task_id: research, description: 再生可能エネルギーの現状を調査
2. task_id: analysis, description: 調査結果を分析, dependencies: ["research"]
3. task_id: report, description: 分析結果をもとにレポートを作成, dependencies: ["analysis"]

workflow_id は "energy_report" としてください。
action は "create" を使用してください。
""")

print("=== 結果 ===")
print(result)
