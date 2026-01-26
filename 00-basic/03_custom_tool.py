"""
03_custom_tool.py - カスタムツールの作成と使用

@toolデコレーターを使って独自のツールを定義し、エージェントに与える。
"""

from strands import Agent, tool
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


# カスタムツールの定義
@tool
def get_weather(city: str) -> str:
    """指定された都市の天気を取得します。

    Args:
        city: 天気を取得したい都市名

    Returns:
        天気情報の文字列
    """
    # 実際のAPIを呼ぶ代わりにダミーデータを返す
    weather_data = {
        "東京": "晴れ、気温25度",
        "大阪": "曇り、気温23度",
        "福岡": "雨、気温20度",
        "札幌": "雪、気温-2度",
    }
    return weather_data.get(city, f"{city}の天気情報は見つかりませんでした")


@tool
def calculate(expression: str) -> str:
    """数式を計算します。

    Args:
        expression: 計算したい数式（例: "2 + 3 * 4"）

    Returns:
        計算結果
    """
    # 安全のため、eval の代わりに簡易的な計算
    allowed_chars = set("0123456789+-*/().  ")
    if not all(c in allowed_chars for c in expression):
        return "無効な数式です"

    result = eval(expression)  # noqa: S307
    return f"{expression} = {result}"


# ツールを持つエージェントの作成
agent = Agent(
    model=model,
    system_prompt="あなたは親切なアシスタントです。天気の質問や計算が必要な場合は、適切なツールを使用してください。",
    tools=[get_weather, calculate],
)

# ツールを使った会話
print("=== 天気の質問 ===")
response1 = agent("東京と大阪の天気を教えてください")
print(response1)

print("\n=== 計算の質問 ===")
response2 = agent("100 + 200 * 3 を計算してください")
print(response2)
