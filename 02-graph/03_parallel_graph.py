"""
03_parallel_graph.py - 並列実行グラフ

依存関係のないノードは並列に実行される。
複数のエージェントが同時に処理を行い、最後に結果を統合する。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.graph import GraphBuilder

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# 分析担当エージェント（並列実行される）
market_analyst = Agent(
    model=model,
    name="market_analyst",
    system_prompt="""あなたは市場分析の専門家です。
与えられた製品アイデアについて、市場の観点から分析してください。
- ターゲット市場
- 競合状況
- 市場規模の推定
を簡潔に述べてください。""",
)

tech_analyst = Agent(
    model=model,
    name="tech_analyst",
    system_prompt="""あなたは技術分析の専門家です。
与えられた製品アイデアについて、技術の観点から分析してください。
- 必要な技術スタック
- 技術的な課題
- 実現可能性
を簡潔に述べてください。""",
)

finance_analyst = Agent(
    model=model,
    name="finance_analyst",
    system_prompt="""あなたは財務分析の専門家です。
与えられた製品アイデアについて、財務の観点から分析してください。
- 初期投資の見積もり
- 収益モデル
- 投資回収期間
を簡潔に述べてください。""",
)

# 統合エージェント
integrator = Agent(
    model=model,
    name="integrator",
    system_prompt="""あなたは事業企画の統括責任者です。
市場分析、技術分析、財務分析の結果を統合し、
総合的な事業評価レポートを作成してください。

最後に「Go」か「No-Go」の判断を明確に示してください。""",
)

# グラフの構築
builder = GraphBuilder()

# ノードの追加
builder.add_node(market_analyst, "market")
builder.add_node(tech_analyst, "tech")
builder.add_node(finance_analyst, "finance")
builder.add_node(integrator, "integrate")

# 並列ノードから統合ノードへのエッジ
# market, tech, finance は互いに依存がないため並列実行される
builder.add_edge("market", "integrate")
builder.add_edge("tech", "integrate")
builder.add_edge("finance", "integrate")

# 複数のエントリーポイント（並列開始）
builder.set_entry_point("market")
builder.set_entry_point("tech")
builder.set_entry_point("finance")

# グラフをビルド
graph = builder.build()

# テスト実行
print("=== 並列実行グラフのテスト ===")
print("製品アイデア: AIを活用したパーソナル英会話学習アプリ\n")

result = graph("AIを活用したパーソナル英会話学習アプリを開発したいと考えています。このアイデアについて分析してください。")

print("=== 統合レポート ===")
print(result)
