"""
01_basic_swarm.py - 基本的なSwarm（エージェント間のhandoff）

Swarmパターンでは、エージェントが自律的に判断して
別のエージェントに処理を引き継ぐ（handoff）ことができる。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.swarm import Swarm

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# リサーチャーエージェント
researcher = Agent(
    model=model,
    name="researcher",
    system_prompt="""あなたはリサーチの専門家です。
ユーザーからの質問に対して、必要な情報を調査・整理します。

調査が完了したら、その情報をライターに引き継いでください。
引き継ぐ際は「ライターに引き継ぎます」と明示してください。""",
)

# ライターエージェント
writer = Agent(
    model=model,
    name="writer",
    system_prompt="""あなたはプロのライターです。
リサーチャーから受け取った情報をもとに、
読みやすく魅力的な文章を作成します。

最終的な文章を作成したら、処理を完了してください。""",
)

# Swarmの構築
swarm = Swarm(
    nodes=[researcher, writer],
    entry_point=researcher,
    max_handoffs=5,
    max_iterations=10,
    execution_timeout=300.0,
)

# Swarmの実行
print("=== 基本的なSwarmの実行 ===")
print("タスク: 人工知能の歴史について短い記事を書く\n")

result = swarm("人工知能の歴史について、200文字程度の短い記事を書いてください")

print("=== 最終結果 ===")
print(result)
