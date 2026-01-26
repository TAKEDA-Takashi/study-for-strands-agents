"""
02_system_prompt.py - システムプロンプトの設定

エージェントの性格や役割をシステムプロンプトで定義する。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# システムプロンプトでエージェントの役割を定義
agent = Agent(
    model=model,
    system_prompt="""あなたは親切な日本語の先生です。
以下のルールに従って回答してください：
- 常に丁寧な敬語を使用する
- 難しい言葉は分かりやすく説明する
- 例文を交えて説明する
""",
)

# エージェントへの問い合わせ
response = agent("「蛙の子は蛙」ということわざの意味を教えてください。")

print("=== レスポンス ===")
print(response)
