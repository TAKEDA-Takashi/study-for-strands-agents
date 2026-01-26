"""
02_parallel_workflow.py - 並列実行ワークフロー

依存関係のないタスクは並列に実行される。
最後のタスクで並列タスクの結果を統合する。
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
workflowツールを使ってタスクを整理し、効率的に実行してください。

並列実行可能なタスクは依存関係なしで定義し、
最終的な統合タスクで結果をまとめてください。""",
    tools=[workflow],
)

print("=== 並列実行ワークフローの作成 ===")
print("タスク: 市場調査（3つの並列調査→統合）\n")

result = agent("""
市場調査のワークフローを作成してください（実行はまだしないでください）。
workflow_id は "market_research"、action は "create" です。

以下の構造でタスクを定義してください:

並列タスク（依存関係なし、同時実行可能）:
1. task_id: competitor_analysis, description: 競合他社の分析, priority: 3
2. task_id: customer_survey, description: 顧客ニーズの調査, priority: 3
3. task_id: trend_research, description: 市場トレンドの調査, priority: 3

統合タスク:
4. task_id: final_report, description: 上記3つの調査結果を統合してレポート作成
   dependencies: ["competitor_analysis", "customer_survey", "trend_research"]
   priority: 5
""")

print("=== 結果 ===")
print(result)
