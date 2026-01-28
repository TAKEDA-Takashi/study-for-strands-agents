"""
01_basic_workflow.py - 基本的なワークフロー

workflowツールを使って、依存関係のあるタスクを順番に実行する。
agent.tool.workflow() でプログラム的にワークフローを制御。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import workflow

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# workflowツールを持つエージェント
agent = Agent(model=model, tools=[workflow])

# Bedrockモデル設定（各タスクで使用）
bedrock_settings = {
    "model_id": "jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    "region_name": "ap-northeast-1",
}

# タスク定義: 調査 → 分析 → レポート作成
tasks = [
    {
        "task_id": "research",
        "description": "再生可能エネルギー（太陽光、風力、水力）それぞれの特徴を1文ずつ、計3文で説明してください。",
        "system_prompt": "簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "priority": 3,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    {
        "task_id": "analysis",
        "description": "前のタスクの内容を踏まえ、日本での普及における課題を3点挙げてください。",
        "system_prompt": "簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["research"],
        "priority": 3,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    {
        "task_id": "report",
        "description": "これまでの内容を5行以内のサマリーにまとめてください。",
        "system_prompt": "簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["analysis"],
        "priority": 5,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
]

print("=== 基本的なワークフロー: シーケンシャル実行 ===")
print("タスク構造: research → analysis → report\n")

# 1. ワークフロー作成
print("1. ワークフローを作成...")
create_result = agent.tool.workflow(
    action="create",
    workflow_id="energy_report",
    tasks=tasks,
)
print(f"   作成完了: {create_result}\n")

# 2. ワークフロー開始（同期的に完了まで待機）
print("2. ワークフローを開始...")
start_result = agent.tool.workflow(
    action="start",
    workflow_id="energy_report",
)
print(f"   結果: {start_result}\n")

# startアクションは同期的に完了を待つため、結果を確認
start_result_str = str(start_result).lower()
if "completed successfully" in start_result_str:
    print("=== ワークフロー完了（成功） ===")
elif "failed" in start_result_str:
    print("=== ワークフロー完了（失敗あり） ===")
else:
    # 非同期で終わった場合のみステータス確認（通常は不要）
    print("3. 最終ステータスを確認...")
    status = agent.tool.workflow(
        action="status",
        workflow_id="energy_report",
    )
    print(f"   最終ステータス: {status}")
    print("\n=== ワークフロー完了 ===")
