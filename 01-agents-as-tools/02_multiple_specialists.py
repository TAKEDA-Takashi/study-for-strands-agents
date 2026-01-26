"""
02_multiple_specialists.py - 複数の専門家エージェントをオーケストレーターが使い分ける

それぞれ異なる専門知識を持つエージェントをツールとして定義し、
オーケストレーターが質問の内容に応じて適切な専門家を選択する。
"""

from strands import Agent, tool
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


@tool
def math_expert(question: str) -> str:
    """数学の専門家エージェントです。数学的な問題を解決します。

    Args:
        question: 数学に関する質問や問題

    Returns:
        数学的な回答と解説
    """
    expert = Agent(
        model=model,
        system_prompt="""あなたは数学の専門家です。
数学的な問題を正確に解き、わかりやすく解説してください。
計算過程も示しながら説明してください。""",
    )
    result = expert(question)
    return str(result)


@tool
def history_expert(question: str) -> str:
    """歴史の専門家エージェントです。歴史に関する質問に答えます。

    Args:
        question: 歴史に関する質問

    Returns:
        歴史的な事実と解説
    """
    expert = Agent(
        model=model,
        system_prompt="""あなたは歴史の専門家です。
歴史的な出来事や人物について、正確で詳細な情報を提供してください。
時代背景や因果関係も含めて説明してください。""",
    )
    result = expert(question)
    return str(result)


@tool
def science_expert(question: str) -> str:
    """科学の専門家エージェントです。自然科学に関する質問に答えます。

    Args:
        question: 科学に関する質問

    Returns:
        科学的な説明と解説
    """
    expert = Agent(
        model=model,
        system_prompt="""あなたは自然科学の専門家です。
物理学、化学、生物学などの科学的な質問に対して、
正確でわかりやすい説明を提供してください。""",
    )
    result = expert(question)
    return str(result)


# オーケストレーター
orchestrator = Agent(
    model=model,
    system_prompt="""あなたは知識豊富なアシスタントです。
ユーザーの質問内容に応じて、適切な専門家エージェントに相談してください。

- 数学的な問題 → math_expert
- 歴史に関する質問 → history_expert
- 科学に関する質問 → science_expert

複数の分野にまたがる質問の場合は、必要な専門家すべてに相談してください。""",
    tools=[math_expert, history_expert, science_expert],
)

print("=== 数学の質問 ===")
response1 = orchestrator("二次方程式 x^2 - 5x + 6 = 0 を解いてください")
print(response1)

print("\n=== 歴史の質問 ===")
response2 = orchestrator("江戸幕府が開かれた経緯を教えてください")
print(response2)

print("\n=== 複合的な質問 ===")
response3 = orchestrator("ピタゴラスについて、数学者としての業績と生きた時代背景を教えてください")
print(response3)
