"""
05_conversation_memory.py - 会話履歴（メモリ）の管理

エージェントは会話履歴を保持し、文脈を理解した応答ができる。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# エージェントの作成
agent = Agent(
    model=model,
    system_prompt="あなたは親切なアシスタントです。ユーザーとの会話の文脈を覚えておいてください。",
)

# 会話を続ける
print("=== 会話1 ===")
response1 = agent("私の名前は田中です。よろしくお願いします。")
print(response1)

print("\n=== 会話2 ===")
response2 = agent("私の好きな食べ物はラーメンです。")
print(response2)

print("\n=== 会話3（文脈を参照） ===")
response3 = agent("私の名前と好きな食べ物を教えてください。")
print(response3)

# 会話履歴の確認
print("\n=== 会話履歴（メッセージ数） ===")
print(f"メッセージ数: {len(agent.messages)}")
