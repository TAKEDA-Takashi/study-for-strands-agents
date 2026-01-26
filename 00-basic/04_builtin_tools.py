"""
04_builtin_tools.py - 組み込みツールの使用

strands-agents-toolsパッケージで提供される組み込みツールを使用する。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import calculator

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# 組み込みのcalculatorツールを使用
agent = Agent(
    model=model,
    system_prompt="あなたは数学のアシスタントです。計算が必要な場合はcalculatorツールを使ってください。",
    tools=[calculator],
)

print("=== 基本的な計算 ===")
response1 = agent("(123 + 456) * 789 を計算してください")
print(response1)

print("\n=== 複雑な計算 ===")
response2 = agent("2の10乗を計算してください")
print(response2)
