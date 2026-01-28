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

agent = Agent(model=model, tools=[workflow])

# Bedrockモデル設定（各タスクで使用）
bedrock_settings = {
    "model_id": "jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    "region_name": "ap-northeast-1",
}

# タスク定義: 3つの並列調査 → 統合レポート
tasks = [
    # 並列実行されるタスク（依存関係なし）
    {
        "task_id": "competitor_analysis",
        "description": "クラウドストレージ市場における主要3社（AWS S3、Google Cloud Storage、Azure Blob）の特徴を各1〜2文で比較してください。",
        "system_prompt": "あなたは競合分析の専門家です。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "priority": 3,
        "timeout": 120,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    {
        "task_id": "customer_needs",
        "description": "企業がクラウドストレージを選ぶ際の主要な判断基準を3つ、各1文で挙げてください。",
        "system_prompt": "あなたは顧客調査の専門家です。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "priority": 3,
        "timeout": 120,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    {
        "task_id": "market_trends",
        "description": "クラウドストレージ市場の最新トレンド（AI連携、エッジコンピューティング等）を3つ、各1文で挙げてください。",
        "system_prompt": "あなたは市場調査アナリストです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "priority": 3,
        "timeout": 120,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    # 統合タスク（全ての並列タスクに依存）
    {
        "task_id": "final_report",
        "description": "競合分析、顧客ニーズ、市場トレンドの結果を統合し、「クラウドストレージ市場の現状と展望」という題で200字程度のサマリーを作成してください。",
        "system_prompt": "あなたはレポートライターです。簡潔にまとめてください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["competitor_analysis", "customer_needs", "market_trends"],
        "priority": 5,
        "timeout": 180,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
]

print("=== 並列実行ワークフロー ===")
print("タスク構造:")
print("  competitor_analysis ─┐")
print("  customer_needs ──────┼─→ final_report")
print("  market_trends ───────┘")
print()

# 1. ワークフロー作成
print("1. ワークフローを作成...")
agent.tool.workflow(
    action="create",
    workflow_id="market_research",
    tasks=tasks,
)
print("   作成完了\n")

# 2. ワークフロー開始（同期的に完了まで待機）
print("2. ワークフローを開始...")
print("   ※ 3つの調査タスクが並列実行されます")
start_result = agent.tool.workflow(
    action="start",
    workflow_id="market_research",
)
print(f"   結果: {start_result}\n")

# startアクションは同期的に完了を待つため、結果を確認
start_result_str = str(start_result).lower()
if "completed successfully" in start_result_str:
    print("=== ワークフロー完了（成功） ===")
elif "failed" in start_result_str:
    print("=== ワークフロー完了（失敗あり） ===")
else:
    print("3. 最終ステータスを確認...")
    status = agent.tool.workflow(
        action="status",
        workflow_id="market_research",
    )
    print(f"   最終ステータス: {status}")
    print("\n=== ワークフロー完了 ===")
