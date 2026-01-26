"""
02_customer_support_swarm.py - カスタマーサポートチームのSwarm

複数の専門エージェントが協調してカスタマーサポートを行う。
問い合わせ内容に応じて適切なエージェントにhandoffする。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.swarm import Swarm

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# 受付エージェント（トリアージ担当）
receptionist = Agent(
    model=model,
    name="receptionist",
    system_prompt="""あなたはカスタマーサポートの受付担当です。
お客様からの問い合わせを受け、内容を分析して適切な担当者に引き継ぎます。

- 技術的な問題 → technical_support に引き継ぐ
- 請求・支払いの問題 → billing_support に引き継ぐ
- 一般的な質問 → あなたが直接回答する

引き継ぐ際は「〇〇に引き継ぎます」と明示してください。""",
)

# 技術サポートエージェント
technical_support = Agent(
    model=model,
    name="technical_support",
    system_prompt="""あなたは技術サポートの専門家です。
ソフトウェアやハードウェアに関する技術的な問題を解決します。

問題が解決したら、その解決策を説明してください。
もし請求に関連する問題が見つかった場合は、billing_supportに引き継いでください。""",
)

# 請求サポートエージェント
billing_support = Agent(
    model=model,
    name="billing_support",
    system_prompt="""あなたは請求・支払いサポートの専門家です。
料金プラン、請求書、支払い方法などに関する問題を解決します。

問題が解決したら、その内容を説明してください。
もし技術的な問題が見つかった場合は、technical_supportに引き継いでください。""",
)

# Swarmの構築
swarm = Swarm(
    nodes=[receptionist, technical_support, billing_support],
    entry_point=receptionist,
    max_handoffs=10,
    max_iterations=15,
    execution_timeout=300.0,
)

# テスト実行
print("=== カスタマーサポートSwarmのテスト ===\n")

print("--- 技術的な問い合わせ ---")
result1 = swarm("アプリにログインできません。パスワードを入力しても「認証エラー」と表示されます。")
print(result1)

print("\n--- 請求に関する問い合わせ ---")
result2 = swarm("今月の請求額が先月より高くなっています。理由を教えてください。")
print(result2)

print("\n--- 一般的な問い合わせ ---")
result3 = swarm("営業時間を教えてください。")
print(result3)
