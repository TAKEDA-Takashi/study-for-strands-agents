"""
03_backtrack_swarm.py - バックトラックのあるSwarm

Swarmの特徴: エージェントが自律的に判断し、必要に応じて前のエージェントに戻れる。

Graphとの違い:
- Graph: ループはset_max_node_executionsで制御、条件関数で判断
- Swarm: エージェント自身が「うまくいかない」と判断して戻る

このサンプルでは、処理が失敗したときに前のステップに戻って
再試行するバックトラックパターンを示す。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.swarm import Swarm

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# 要件定義エージェント
requirements_analyst = Agent(
    model=model,
    name="requirements_analyst",
    system_prompt="""あなたは要件アナリストです。
ユーザーの要望を聞いて、技術要件を整理します。

要件を整理したら、implementerに引き継いでください。

もしimplementerから「要件が不明確」というフィードバックを受けた場合は、
追加の質問をユーザーに投げかけるか、要件を明確化して再度implementerに引き継いでください。

出力形式:
【要件】
1. ...
2. ...

引き継ぐ際は「implementerに引き継ぎます」と明示してください。""",
)

# 実装エージェント
implementer = Agent(
    model=model,
    name="implementer",
    system_prompt="""あなたは実装担当のエンジニアです。
要件アナリストから受け取った要件をもとに、実装計画を作成します。

要件が明確な場合:
- 実装計画を作成
- コード例を提示
- reviewerに引き継ぐ

要件が不明確・矛盾している場合:
- 何が不明確かを具体的に指摘
- requirements_analystに引き継いで明確化を依頼

引き継ぐ際は「〇〇に引き継ぎます」と明示してください。""",
)

# レビューエージェント
reviewer = Agent(
    model=model,
    name="reviewer",
    system_prompt="""あなたはシニアエンジニアのレビュアーです。
実装計画とコードをレビューします。

問題がない場合:
- 「承認」と明示して、最終コメントを出力
- 処理を完了

問題がある場合（バグ、設計ミス、要件との不整合など）:
- 具体的な問題点を指摘
- 軽微な修正 → implementerに引き継ぎ
- 要件レベルの問題 → requirements_analystに引き継ぎ

引き継ぐ際は「〇〇に引き継ぎます」と明示してください。""",
)

# Swarmの構築
swarm = Swarm(
    nodes=[requirements_analyst, implementer, reviewer],
    entry_point=requirements_analyst,
    max_handoffs=10,  # バックトラックを考慮して多めに設定
    max_iterations=15,
    execution_timeout=600.0,
)

# テスト実行
print("=== バックトラックSwarmのテスト ===")
print()
print("Swarmの特徴: 処理がうまくいかない場合、")
print("エージェントが自律的に前のステップに戻って再試行する")
print()
print("想定フロー:")
print("  requirements_analyst → implementer → reviewer")
print("                 ↑            │")
print("                 └────────────┘ (問題があれば戻る)")
print()

# 曖昧な要件を与えて、バックトラックを誘発
print("--- ケース: 曖昧な要件からの実装 ---")
print("要件: 「ユーザー管理機能を作って」（詳細が曖昧）")
print()

result = swarm(
    "ユーザー管理機能を作ってください。"
    "ログインとかできるようにしたいです。"
)

print("=== 最終結果 ===")
print(result)
