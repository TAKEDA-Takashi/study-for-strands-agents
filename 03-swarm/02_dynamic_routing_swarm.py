"""
02_dynamic_routing_swarm.py - 動的ルーティングのSwarm

Swarmの特徴: エージェントが会話の内容を理解して、自律的にhandoff先を決定する。

Graphとの違い:
- Graph: 条件関数（コード）でルーティングを定義
- Swarm: エージェント（LLM）が文脈を理解してルーティングを判断

このサンプルでは、「技術的な問題かと思ったら請求の問題だった」など、
会話を通じて問題の本質が明らかになり、動的にhandoffするケースを示す。
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

判断基準:
- 技術的な問題（エラー、動作不良など）→ technical_support
- 請求・料金の問題 → billing_support
- 解約・退会の相談 → retention_specialist

曖昧な場合は、最も可能性が高いと思われる担当者に引き継いでください。
引き継ぐ際は「〇〇に引き継ぎます」と明示してください。""",
)

# 技術サポートエージェント
technical_support = Agent(
    model=model,
    name="technical_support",
    system_prompt="""あなたは技術サポートの専門家です。

お客様の問題を深掘りして、真の原因を特定してください。
技術的な問題であれば解決策を提案してください。

重要: 対話を通じて、実は技術的な問題ではなく別の問題だと判明した場合は、
適切な担当者にhandoffしてください。
- 料金に関する問題 → billing_support
- 解約の意向 → retention_specialist

例えば「機能が使えない」という問い合わせが、実は「プランの制限」だった場合は
billing_supportに引き継いでください。""",
)

# 請求サポートエージェント
billing_support = Agent(
    model=model,
    name="billing_support",
    system_prompt="""あなたは請求・料金サポートの専門家です。

料金プラン、請求書、支払い方法に関する問題を解決します。
プランのアップグレードやダウングレードの相談にも対応します。

重要: お客様が料金に不満を持ち、解約を検討している様子であれば、
retention_specialistに引き継いでください。""",
)

# 解約防止スペシャリスト
retention_specialist = Agent(
    model=model,
    name="retention_specialist",
    system_prompt="""あなたは顧客維持の専門家です。

解約を検討しているお客様に対して、以下を行います:
1. 解約理由をヒアリング
2. 問題解決の提案（割引、プラン変更など）
3. どうしても解約希望の場合は、丁寧に手続きを案内

お客様の不満が技術的な問題に起因する場合は、
technical_supportに引き継いで問題解決を試みてください。""",
)

# Swarmの構築
swarm = Swarm(
    nodes=[receptionist, technical_support, billing_support, retention_specialist],
    entry_point=receptionist,
    max_handoffs=10,
    max_iterations=15,
    execution_timeout=300.0,
)

# テスト実行
print("=== 動的ルーティングSwarmのテスト ===")
print()
print("Swarmの特徴: エージェントが会話の文脈を理解し、")
print("適切な担当者に自律的にhandoffする")
print()

# ケース: 技術的な問題かと思ったら、実はプラン制限の問題
print("--- ケース: 曖昧な問い合わせ（技術？料金？） ---")
print("問い合わせ: 「プレミアム機能が使えないんですけど」")
print()
result = swarm(
    "プレミアム機能が使えないんですけど、どうなってますか？"
    "昨日までは使えてたのに。お金払ってるのにおかしいですよね。"
)
print("=== 結果 ===")
print(result)
