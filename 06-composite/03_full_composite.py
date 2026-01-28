"""
03_full_composite.py - 完全な複合パターン

Graph + Swarm + Agents as Tools を組み合わせたコンテンツ制作システム。

フロー:
- 企画: Swarm（編集者・マーケター・ライターが協議）
- 調査: Agents as Tools（専門エージェントをツールとして呼び出し）
- 執筆: 単純なAgent
- レビュー: Swarm（技術・文章の両面からレビュー）
"""

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands.multiagent.graph import GraphBuilder
from strands.multiagent.swarm import Swarm

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


# ============================================================
# 企画フェーズ: Swarm（複数専門家が協議）
# ============================================================

editor = Agent(
    model=model,
    name="editor",
    system_prompt="""あなたは編集者です。
テーマを受けて、記事の方向性を提案してください。
提案後、marketerに引き継いでください。""",
)

marketer = Agent(
    model=model,
    name="marketer",
    system_prompt="""あなたはマーケターです。
読者視点でアドバイスし、content_writerに引き継いでください。""",
)

content_writer = Agent(
    model=model,
    name="content_writer",
    system_prompt="""あなたはコンテンツライターです。
意見を踏まえて企画案をまとめてください。

出力形式:
【タイトル案】【想定読者】【記事構成】【キーメッセージ】

他のエージェントには引き継がないでください。""",
)

planning_swarm = Swarm(
    nodes=[editor, marketer, content_writer],
    entry_point=editor,
    max_handoffs=5,
    max_iterations=10,
    execution_timeout=300.0,
)


# ============================================================
# 調査フェーズ: Agents as Tools（専門エージェントをツールとして呼び出し）
# ============================================================

# 専門家エージェント1: トレンド調査
trend_analyst_agent = Agent(
    model=model,
    system_prompt="""あなたはトレンドアナリストです。
指定されたテーマの最新トレンドを3点挙げてください。簡潔に。""",
)


@tool
def analyze_trends(topic: str) -> str:
    """指定されたトピックの最新トレンドを分析します。

    Args:
        topic: 分析するトピック

    Returns:
        トレンド分析結果
    """
    result = trend_analyst_agent(f"「{topic}」の最新トレンドを分析してください。")
    return str(result)


# 専門家エージェント2: 事例調査
case_researcher_agent = Agent(
    model=model,
    system_prompt="""あなたは事例リサーチャーです。
指定されたテーマに関する具体的な事例を2つ挙げてください。簡潔に。""",
)


@tool
def find_case_studies(topic: str) -> str:
    """指定されたトピックの事例を調査します。

    Args:
        topic: 調査するトピック

    Returns:
        事例調査結果
    """
    result = case_researcher_agent(f"「{topic}」に関する事例を調査してください。")
    return str(result)


# 調査オーケストレーター（Agents as Toolsパターン）
research_orchestrator = Agent(
    model=model,
    name="research_orchestrator",
    system_prompt="""あなたは調査コーディネーターです。
企画内容を受けて、専門家ツールを使って情報を収集してください。

必ず以下の両方を実行してください:
1. analyze_trends: トレンド分析
2. find_case_studies: 事例調査

収集した情報を整理して出力してください。""",
    tools=[analyze_trends, find_case_studies],
)


# ============================================================
# 執筆フェーズ: シンプルなAgent
# ============================================================

writer = Agent(
    model=model,
    name="writer",
    system_prompt="""あなたはライターです。
企画と調査結果をもとに、300〜500字程度の記事を執筆してください。
読みやすく、具体的な内容を盛り込んでください。""",
)


# ============================================================
# レビューフェーズ: Swarm（複数観点からレビュー）
# ============================================================

technical_reviewer = Agent(
    model=model,
    name="technical_reviewer",
    system_prompt="""あなたは技術レビュアーです。
記事の正確性と具体性をチェックしてください。
チェック後、style_reviewerに引き継いでください。""",
)

style_reviewer = Agent(
    model=model,
    name="style_reviewer",
    system_prompt="""あなたは文章レビュアーです。
記事の読みやすさと構成をチェックしてください。
チェック後、final_editorに引き継いでください。""",
)

final_editor = Agent(
    model=model,
    name="final_editor",
    system_prompt="""あなたは最終編集者です。
レビュー結果を踏まえて、総合評価をまとめてください。

出力形式:
【総合評価】良い / 要修正
【良い点】
【改善点】
【最終コメント】

他のエージェントには引き継がないでください。""",
)

review_swarm = Swarm(
    nodes=[technical_reviewer, style_reviewer, final_editor],
    entry_point=technical_reviewer,
    max_handoffs=5,
    max_iterations=10,
    execution_timeout=300.0,
)


# ============================================================
# Graphの構築（全体フロー）
# ============================================================

builder = GraphBuilder()

# ノードの追加
# SwarmやAgentは直接add_nodeに渡せる（MultiAgentBaseを継承）
builder.add_node(planning_swarm, "planning")  # Swarm
builder.add_node(research_orchestrator, "research")  # Agent (with tools)
builder.add_node(writer, "writing")  # Simple Agent
builder.add_node(review_swarm, "review")  # Swarm

# エッジの追加
builder.add_edge("planning", "research")
builder.add_edge("research", "writing")
builder.add_edge("writing", "review")

# エントリーポイント
builder.set_entry_point("planning")

# グラフをビルド
graph = builder.build()


# ============================================================
# 実行
# ============================================================

if __name__ == "__main__":
    print("=== 完全な複合パターン: コンテンツ制作システム ===")
    print()
    print("全体構造: Graph")
    print("├─ 企画(planning): Swarm")
    print("│    └─ editor → marketer → content_writer")
    print("├─ 調査(research): Agents as Tools")
    print("│    └─ orchestrator → [trend_analyst, case_researcher]")
    print("├─ 執筆(writing): Simple Agent")
    print("│    └─ writer")
    print("└─ レビュー(review): Swarm")
    print("     └─ technical_reviewer → style_reviewer → final_editor")
    print()

    result = graph("「リモートワークの生産性向上」をテーマに記事を作成してください。")

    print("=== 最終結果 ===")
    print(result)
