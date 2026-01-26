"""
01_simple_agent.py - 最もシンプルなエージェントの作成と実行

Strands Agentsの基本的な使い方を学ぶ最初のサンプル。
BedrockモデルでClaude Haiku 4.5を使用。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel

# Bedrockモデルの設定（Claude Haiku 4.5、東京リージョン）
model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# 最もシンプルなエージェントの作成
agent = Agent(model=model)

# エージェントへの問い合わせ
response = agent("こんにちは！あなたは何ができますか？")

print("=== レスポンス ===")
print(response)
