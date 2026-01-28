"""
03_loop_graph.py - ループを含むグラフ

Graphパターンではループ（サイクル）をサポートしている。
Workflowパターン（DAG）では不可能な、繰り返し処理を実現できる。

例: コードレビューで問題があれば修正→再レビューのサイクル
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.graph import GraphBuilder, GraphState

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# コード生成エージェント
coder = Agent(
    model=model,
    name="coder",
    system_prompt="""あなたはPython開発者です。
要求された機能を実装するコードを書いてください。

レビュー指摘を受けた場合は、その指摘に基づいて修正したコードを出力してください。
コードは必ず```pythonで囲んで出力してください。""",
)

# コードレビューエージェント
reviewer = Agent(
    model=model,
    name="reviewer",
    system_prompt="""あなたはシニアエンジニアのコードレビュアーです。
提出されたコードをレビューし、以下の観点で評価してください:
- コードの正確性
- エラーハンドリング
- 可読性

問題がある場合: 「要修正:」で始まる具体的な指摘を出力してください。
問題がない場合: 「承認:」で始まるコメントを出力してください。

最大2回までレビューを行い、3回目以降は承認してください。""",
)

# 最終承認エージェント
approver = Agent(
    model=model,
    name="approver",
    system_prompt="""あなたは最終承認者です。
レビューを通過したコードに対して、最終的な承認コメントを出力してください。
「最終承認:」で始まるコメントを出力してください。""",
)


def needs_revision(state: GraphState) -> bool:
    """レビュー結果が要修正かどうかを判定"""
    review_result = state.results.get("review")
    if review_result:
        result_text = str(review_result.result)
        return "要修正" in result_text
    return False


def is_approved(state: GraphState) -> bool:
    """レビュー結果が承認かどうかを判定"""
    review_result = state.results.get("review")
    if review_result:
        result_text = str(review_result.result)
        return "承認" in result_text
    return False


# グラフの構築
builder = GraphBuilder()

# ノードの追加
builder.add_node(coder, "code")
builder.add_node(reviewer, "review")
builder.add_node(approver, "approve")

# エッジの追加
builder.add_edge("code", "review")
builder.add_edge("review", "code", condition=needs_revision)  # ループ: 要修正なら戻る
builder.add_edge("review", "approve", condition=is_approved)  # 承認なら最終承認へ

# ループ回数の制限（無限ループ防止）
builder.set_max_node_executions(3)

# エントリーポイント
builder.set_entry_point("code")

# グラフをビルド
graph = builder.build()

# 実行
print("=== ループグラフの実行: コードレビューサイクル ===")
print()
print("グラフ構造:")
print("  code ──→ review ──→ approve")
print("            │  ↑")
print("            └──┘ (要修正の場合ループ)")
print()

result = graph(
    "2つの数値を受け取り、その合計を返す関数を作成してください。"
    "ただし、入力が数値でない場合のエラーハンドリングは不要です。"
)

print("=== 最終結果 ===")
print(result)
