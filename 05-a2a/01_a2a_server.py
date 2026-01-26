"""
01_a2a_server.py - A2Aサーバー

エージェントをA2Aプロトコル対応のサーバーとして公開する。
他のプラットフォームやクライアントからアクセス可能になる。

実行方法:
    uv run python 05-a2a/01_a2a_server.py

別ターミナルからクライアントで接続:
    uv run python 05-a2a/02_a2a_client.py
"""

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands.multiagent.a2a import A2AServer

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


# サーバー側で提供するツール
@tool
def calculate(expression: str) -> str:
    """数式を計算します。

    Args:
        expression: 計算したい数式（例: "2 + 3 * 4"）

    Returns:
        計算結果
    """
    allowed_chars = set("0123456789+-*/().  ")
    if not all(c in allowed_chars for c in expression):
        return "無効な数式です"
    result = eval(expression)  # noqa: S307
    return f"{expression} = {result}"


@tool
def get_greeting(name: str) -> str:
    """指定された名前に対して挨拶を返します。

    Args:
        name: 挨拶する相手の名前

    Returns:
        挨拶メッセージ
    """
    return f"こんにちは、{name}さん！"


# A2Aサーバーとして公開するエージェント
agent = Agent(
    model=model,
    name="CalculatorAgent",
    description="計算と挨拶ができるアシスタントエージェント",
    system_prompt="""あなたは計算と挨拶ができるアシスタントです。
calculateツールで数式を計算し、get_greetingツールで挨拶ができます。""",
    tools=[calculate, get_greeting],
)

# A2Aサーバーの作成と起動
server = A2AServer(
    agent=agent,
    host="127.0.0.1",
    port=9000,
)

if __name__ == "__main__":
    print("=== A2Aサーバー起動 ===")
    print("URL: http://127.0.0.1:9000")
    print("停止するには Ctrl+C を押してください")
    print()
    server.serve()
