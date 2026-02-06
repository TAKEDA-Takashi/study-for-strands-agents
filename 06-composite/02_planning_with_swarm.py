"""
02_planning_with_swarm.py - 企画フェーズにSwarmを組み込み

Graphの「企画」ノードをSwarmで置き換え。
編集者・ライター・マーケターが協議して企画を練る。

複合パターン: Graph + Swarm
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.graph import GraphBuilder
from strands.multiagent.swarm import Swarm

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


# === 企画フェーズ用のSwarm ===

# 編集者（企画の方向性を決める）
editor = Agent(
    model=model,
    name="editor",
    system_prompt="""あなたは編集者です。
テーマを受けて、記事の方向性を提案してください。

提案後、marketerに引き継いで読者視点の意見をもらってください。
「marketerに引き継ぎます」と明示してください。""",
)

# マーケター（読者視点でアドバイス）
marketer = Agent(
    model=model,
    name="marketer",
    system_prompt="""あなたはマーケターです。
編集者の提案に対して、読者視点でアドバイスしてください。

- ターゲット読者の明確化
- 読者が求める情報
- タイトルの訴求力

アドバイス後、content_writerに引き継いで構成案を作ってもらってください。
「content_writerに引き継ぎます」と明示してください。""",
)

# コンテンツライター（最終的な企画をまとめる）
content_writer = Agent(
    model=model,
    name="content_writer",
    system_prompt="""あなたはコンテンツライターです。
編集者とマーケターの意見を踏まえて、最終的な企画案をまとめてください。

出力形式:
【タイトル案】
【想定読者】
【記事構成】
1. ...
2. ...
3. ...
【キーメッセージ】

これで企画フェーズは完了です。他のエージェントには引き継がないでください。""",
)

# 企画Swarmの構築
planning_swarm = Swarm(
    nodes=[editor, marketer, content_writer],
    entry_point=editor,
    max_handoffs=5,
    max_iterations=10,
    execution_timeout=300.0,
)


# === 後続のシンプルなAgent ===

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
【参考になる事例】""",
)

writer = Agent(
    model=model,
    name="writer",
    system_prompt="""あなたはライターです。
企画と調査結果をもとに、300〜500字程度の記事を執筆してください。""",
)

reviewer = Agent(
    model=model,
    name="reviewer",
    system_prompt="""あなたは編集者です。
記事をレビューし、総合評価と改善点を提供してください。""",
)


# === Graphの構築 ===

builder = GraphBuilder()

# ノードの追加（企画はSwarmを直接使用）
builder.add_node(planning_swarm, "planning")  # SwarmはMultiAgentBaseを継承
builder.add_node(researcher, "research")
builder.add_node(writer, "writing")
builder.add_node(reviewer, "review")

# エッジの追加
builder.add_edge("planning", "research")
builder.add_edge("research", "writing")
builder.add_edge("writing", "review")

# エントリーポイント
builder.set_entry_point("planning")

# グラフをビルド
graph = builder.build()

# 実行
if __name__ == "__main__":
    print("=== コンテンツ制作パイプライン（Graph + Swarm） ===")
    print()
    print("フロー: 企画(Swarm) → 調査 → 執筆 → レビュー")
    print()
    print("企画フェーズの内部:")
    print("  editor → marketer → content_writer（協議してまとめる）")
    print()

    result = graph("「リモートワークの生産性向上」をテーマに記事を作成してください。")

    print("=== 最終結果 ===")
    print(result)
