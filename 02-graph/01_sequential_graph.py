"""
01_sequential_graph.py - シーケンシャル（直列）グラフ

GraphBuilderを使って、ノードが順番に実行される基本的なグラフを構築する。
各ノードは前のノードの結果を受け取って処理を行う。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.graph import GraphBuilder

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# 各ステップを担当するエージェントを作成
idea_generator = Agent(
    model=model,
    name="idea_generator",
    system_prompt="""あなたはアイデア発想の専門家です。
与えられたテーマについて、斬新なアイデアを3つ提案してください。
箇条書きで簡潔に出力してください。""",
)

idea_evaluator = Agent(
    model=model,
    name="idea_evaluator",
    system_prompt="""あなたはアイデア評価の専門家です。
提示されたアイデアの中から最も実現可能性が高いものを1つ選び、
その理由を説明してください。""",
)

action_planner = Agent(
    model=model,
    name="action_planner",
    system_prompt="""あなたは実行計画の専門家です。
選ばれたアイデアを実現するための具体的なアクションプランを
3ステップで作成してください。""",
)

# グラフの構築
builder = GraphBuilder()

# ノードの追加
builder.add_node(idea_generator, "generate")
builder.add_node(idea_evaluator, "evaluate")
builder.add_node(action_planner, "plan")

# エッジの追加（順序を定義）
builder.add_edge("generate", "evaluate")
builder.add_edge("evaluate", "plan")

# エントリーポイントの設定
builder.set_entry_point("generate")

# グラフをビルド
graph = builder.build()

# グラフの実行
print("=== シーケンシャルグラフの実行 ===")
print("テーマ: 環境に優しい通勤方法\n")

result = graph("環境に優しい通勤方法について考えてください")

print("=== 最終結果 ===")
print(result)
