"""
07_tool_context.py - ツールコンテキストと共有状態

invocation_stateを使ってエージェント呼び出し間で設定を共有する。
ToolContextを使うと、ツール内からこの共有状態にアクセスできる。
"""

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands.types.tools import ToolContext

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


@tool(context=True)
def get_user_info(tool_context: ToolContext) -> str:
    """現在のユーザー情報を取得します。

    Returns:
        ユーザー情報の文字列
    """
    # invocation_stateから設定を取得
    user_name = tool_context.invocation_state.get("user_name", "ゲスト")
    user_role = tool_context.invocation_state.get("user_role", "一般")
    return f"ユーザー名: {user_name}, 役割: {user_role}"


@tool(context=True)
def log_action(tool_context: ToolContext, action: str) -> str:
    """アクションをログに記録します。

    Args:
        action: 記録するアクション

    Returns:
        記録結果
    """
    user_name = tool_context.invocation_state.get("user_name", "不明")
    return f"[LOG] ユーザー '{user_name}' が '{action}' を実行しました"


# エージェントの作成
agent = Agent(
    model=model,
    system_prompt="あなたはシステム管理者アシスタントです。ユーザー情報の確認やアクションのログ記録ができます。",
    tools=[get_user_info, log_action],
)

# invocation_stateを使って共有状態を渡す
print("=== 管理者としての実行 ===")
response1 = agent(
    "現在のユーザー情報を確認し、'レポート生成'をログに記録してください",
    invocation_state={"user_name": "山田太郎", "user_role": "管理者"},
)
print(response1)

print("\n=== 一般ユーザーとしての実行 ===")
response2 = agent(
    "現在のユーザー情報を確認してください",
    invocation_state={"user_name": "鈴木花子", "user_role": "一般ユーザー"},
)
print(response2)
