"""
01_basic_agent_as_tool.py - エージェントをツールとしてラップする基本パターン

@toolデコレーターでエージェントをラップし、オーケストレーターから呼び出す。
これにより、専門的なタスクを別のエージェントに委譲できる。
"""

from strands import Agent, tool
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


# 専門家エージェントをツールとしてラップ
@tool
def translator_agent(text: str, target_language: str) -> str:
    """テキストを指定された言語に翻訳する専門家エージェントです。

    Args:
        text: 翻訳したいテキスト
        target_language: 翻訳先の言語（例: 英語、中国語、フランス語）

    Returns:
        翻訳されたテキスト
    """
    translator = Agent(
        model=model,
        system_prompt=f"""あなたはプロの翻訳者です。
与えられたテキストを{target_language}に翻訳してください。
翻訳結果のみを返し、説明は不要です。
自然で流暢な翻訳を心がけてください。""",
    )
    result = translator(f"次のテキストを翻訳してください: {text}")
    return str(result)


# オーケストレーター（上位エージェント）
orchestrator = Agent(
    model=model,
    system_prompt="""あなたは多言語対応のアシスタントです。
ユーザーから翻訳のリクエストがあった場合は、translator_agentツールを使用して翻訳を行ってください。
複数言語への翻訳が必要な場合は、それぞれの言語に対してツールを呼び出してください。""",
    tools=[translator_agent],
)

# オーケストレーターを通じて翻訳を実行
print("=== 英語への翻訳 ===")
response1 = orchestrator("「今日は良い天気ですね」を英語に翻訳してください")
print(response1)

print("\n=== 複数言語への翻訳 ===")
response2 = orchestrator("「ありがとうございます」を英語と中国語に翻訳してください")
print(response2)
