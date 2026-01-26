"""
02_conditional_graph.py - 条件分岐のあるグラフ

エッジに条件関数を設定し、前のノードの結果に応じて
異なるパスを辿るグラフを構築する。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.graph import GraphBuilder, GraphState

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# 分類エージェント
classifier = Agent(
    model=model,
    name="classifier",
    system_prompt="""あなたは質問分類の専門家です。
ユーザーの質問を分析し、以下のいずれかに分類してください。

- 技術的な質問の場合: 「分類: 技術」と出力
- ビジネスに関する質問の場合: 「分類: ビジネス」と出力

必ず「分類: 」で始まる行を含めてください。""",
)

# 技術専門家エージェント
tech_expert = Agent(
    model=model,
    name="tech_expert",
    system_prompt="""あなたは技術の専門家です。
技術的な質問に対して、専門的かつわかりやすく回答してください。""",
)

# ビジネス専門家エージェント
business_expert = Agent(
    model=model,
    name="business_expert",
    system_prompt="""あなたはビジネスの専門家です。
ビジネスに関する質問に対して、実践的なアドバイスを提供してください。""",
)

# 最終まとめエージェント
summarizer = Agent(
    model=model,
    name="summarizer",
    system_prompt="""あなたは優秀なまとめ役です。
これまでの回答を簡潔にまとめ、ユーザーに最終的な回答を提供してください。""",
)


# 条件関数の定義
def is_tech_question(state: GraphState) -> bool:
    """技術的な質問かどうかを判定"""
    classifier_result = state.results.get("classify")
    if classifier_result:
        return "技術" in str(classifier_result.result)
    return False


def is_business_question(state: GraphState) -> bool:
    """ビジネスの質問かどうかを判定"""
    classifier_result = state.results.get("classify")
    if classifier_result:
        return "ビジネス" in str(classifier_result.result)
    return False


# グラフの構築
builder = GraphBuilder()

# ノードの追加
builder.add_node(classifier, "classify")
builder.add_node(tech_expert, "tech")
builder.add_node(business_expert, "business")
builder.add_node(summarizer, "summarize")

# 条件付きエッジの追加
builder.add_edge("classify", "tech", condition=is_tech_question)
builder.add_edge("classify", "business", condition=is_business_question)

# 両方のパスから最終ノードへ
builder.add_edge("tech", "summarize")
builder.add_edge("business", "summarize")

# エントリーポイントの設定
builder.set_entry_point("classify")

# グラフをビルド
graph = builder.build()

# テスト実行
print("=== 条件分岐グラフのテスト ===\n")

print("--- 技術的な質問 ---")
result1 = graph("Pythonで非同期処理を実装するにはどうすればいいですか？")
print(result1)

print("\n--- ビジネスの質問 ---")
result2 = graph("スタートアップの資金調達方法について教えてください")
print(result2)
