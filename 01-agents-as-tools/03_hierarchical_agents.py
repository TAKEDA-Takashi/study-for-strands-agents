"""
03_hierarchical_agents.py - 階層的なエージェント構造

エージェントが別のエージェントをツールとして持ち、さらにそのエージェントも
別のエージェントを持つ多層構造を実現する。
複雑なタスクを段階的に分解・委譲できる。
"""

from strands import Agent, tool
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


# 最下層: 特定のタスクを実行する専門エージェント
@tool
def code_formatter(code: str, language: str) -> str:
    """コードを整形する専門エージェントです。

    Args:
        code: 整形したいコード
        language: プログラミング言語

    Returns:
        整形されたコード
    """
    formatter = Agent(
        model=model,
        system_prompt=f"""あなたはコード整形の専門家です。
与えられた{language}のコードを、適切なインデントと改行で整形してください。
整形されたコードのみを返してください。""",
    )
    result = formatter(f"次のコードを整形してください:\n{code}")
    return str(result)


@tool
def code_explainer(code: str, language: str) -> str:
    """コードを解説する専門エージェントです。

    Args:
        code: 解説したいコード
        language: プログラミング言語

    Returns:
        コードの解説
    """
    explainer = Agent(
        model=model,
        system_prompt=f"""あなたはプログラミング教育の専門家です。
与えられた{language}のコードを、初心者にもわかりやすく解説してください。
各部分が何をしているか、順を追って説明してください。""",
    )
    result = explainer(f"次のコードを解説してください:\n{code}")
    return str(result)


# 中間層: 複数の専門エージェントを統括するエージェント
@tool
def code_review_agent(code: str, language: str) -> str:
    """コードレビューを行う中間エージェントです。
    必要に応じて整形や解説の専門家に依頼します。

    Args:
        code: レビューするコード
        language: プログラミング言語

    Returns:
        レビュー結果（整形済みコードと解説を含む）
    """
    reviewer = Agent(
        model=model,
        system_prompt="""あなたはシニアエンジニアです。
コードレビューを担当しています。

レビュー時には:
1. まずcode_formatterでコードを整形してもらう
2. 次にcode_explainerでコードの解説をしてもらう
3. その上で、改善点やベストプラクティスについてコメントする

これらを組み合わせて、包括的なレビューを提供してください。""",
        tools=[code_formatter, code_explainer],
    )
    result = reviewer(f"次の{language}コードをレビューしてください:\n{code}")
    return str(result)


# 最上層: プロジェクト全体を管理するオーケストレーター
orchestrator = Agent(
    model=model,
    system_prompt="""あなたはテックリードです。
開発チームからの様々なリクエストに対応します。

コードレビューが必要な場合は、code_review_agentに依頼してください。
レビュー結果を受け取ったら、プロジェクト全体の観点からアドバイスを追加してください。""",
    tools=[code_review_agent],
)

# 階層的なエージェント構造のテスト
sample_code = """
def calc(x,y):
    z=x+y
    return z
result=calc(5,3)
print(result)
"""

print("=== 階層的なコードレビュー ===")
print("（オーケストレーター → レビューエージェント → 整形/解説エージェント）")
print()

response = orchestrator(f"次のPythonコードについてレビューをお願いします:\n{sample_code}")
print(response)
