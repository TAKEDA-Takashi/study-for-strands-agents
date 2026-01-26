"""
03_development_team_swarm.py - 開発チームのSwarm

プロダクトマネージャー、設計者、開発者が協調して
機能要件から実装まで処理するSwarm。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.multiagent.swarm import Swarm

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# プロダクトマネージャー
product_manager = Agent(
    model=model,
    name="product_manager",
    system_prompt="""あなたはプロダクトマネージャーです。
ユーザーからの要望を受け、機能要件を整理します。

要件が整理できたら、設計者（architect）に引き継いでください。
引き継ぐ際は「architectに引き継ぎます」と明示してください。""",
)

# アーキテクト（設計者）
architect = Agent(
    model=model,
    name="architect",
    system_prompt="""あなたはソフトウェアアーキテクトです。
プロダクトマネージャーから受け取った要件をもとに、
技術設計（アーキテクチャ、使用技術、コンポーネント構成）を行います。

設計が完了したら、開発者（developer）に引き継いでください。
引き継ぐ際は「developerに引き継ぎます」と明示してください。""",
)

# 開発者
developer = Agent(
    model=model,
    name="developer",
    system_prompt="""あなたはシニア開発者です。
アーキテクトから受け取った設計をもとに、
具体的な実装計画とサンプルコードを作成します。

もし設計に不明点があれば、architectに確認してください。
実装計画が完成したら、処理を完了してください。""",
)

# レビュアー
reviewer = Agent(
    model=model,
    name="reviewer",
    system_prompt="""あなたはコードレビュアーです。
開発者の実装計画とコードをレビューします。

問題があれば開発者（developer）に修正を依頼してください。
問題がなければ、最終的な評価コメントを出力して処理を完了してください。""",
)

# Swarmの構築
swarm = Swarm(
    nodes=[product_manager, architect, developer, reviewer],
    entry_point=product_manager,
    max_handoffs=15,
    max_iterations=20,
    execution_timeout=600.0,
)

# テスト実行
print("=== 開発チームSwarmのテスト ===")
print("要望: ユーザー認証機能の追加\n")

result = swarm(
    "ユーザー認証機能を追加したいです。"
    "メールアドレスとパスワードでログインできるようにしてください。"
    "セキュリティを考慮した設計をお願いします。"
)

print("=== 最終結果 ===")
print(result)
