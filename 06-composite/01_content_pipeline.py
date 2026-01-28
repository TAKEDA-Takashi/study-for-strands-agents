"""
01_content_pipeline.py - コンテンツ制作パイプライン（基本版）

Graphパターンを使った基本的なコンテンツ制作フロー。
各ノードは単純なAgentで、後のサンプルでSwarmやAgents as Toolsに置き換える。

フロー: 企画 → 調査 → 執筆 → レビュー
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.graph import GraphBuilder

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# 企画担当エージェント
planner = Agent(
    model=model,
    name="planner",
    system_prompt="""あなたはコンテンツ企画担当です。
与えられたテーマに対して、記事の構成案を作成してください。

出力形式:
【タイトル案】
【想定読者】
【記事構成】
1. ...
2. ...
3. ...
【キーメッセージ】""",
)

# 調査担当エージェント
researcher = Agent(
    model=model,
    name="researcher",
    system_prompt="""あなたはリサーチャーです。
企画内容を受けて、記事に必要な情報を調査・整理してください。

出力形式:
【調査結果】
- ポイント1: ...
- ポイント2: ...
- ポイント3: ...
【参考になる事例】
【注意点】""",
)

# 執筆担当エージェント
writer = Agent(
    model=model,
    name="writer",
    system_prompt="""あなたはライターです。
企画と調査結果をもとに、記事本文を執筆してください。

300〜500字程度の短い記事を書いてください。
読みやすく、分かりやすい文章を心がけてください。""",
)

# レビュー担当エージェント
reviewer = Agent(
    model=model,
    name="reviewer",
    system_prompt="""あなたは編集者です。
執筆された記事をレビューし、フィードバックを提供してください。

出力形式:
【総合評価】良い / 要修正
【良い点】
【改善点】
【最終コメント】""",
)

# Graphの構築
builder = GraphBuilder()

# ノードの追加
builder.add_node(planner, "planning")
builder.add_node(researcher, "research")
builder.add_node(writer, "writing")
builder.add_node(reviewer, "review")

# エッジの追加（シーケンシャルフロー）
builder.add_edge("planning", "research")
builder.add_edge("research", "writing")
builder.add_edge("writing", "review")

# エントリーポイント
builder.set_entry_point("planning")

# グラフをビルド
graph = builder.build()

# 実行
print("=== コンテンツ制作パイプライン（基本版） ===")
print()
print("フロー: 企画 → 調査 → 執筆 → レビュー")
print("各ノードは単純なAgentで構成")
print()

result = graph("「リモートワークの生産性向上」をテーマに記事を作成してください。")

print("=== 最終結果 ===")
print(result)
