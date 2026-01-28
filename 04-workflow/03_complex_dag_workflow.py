"""
03_complex_dag_workflow.py - 複雑なDAGワークフロー

シーケンシャルと並列を組み合わせた複雑な依存関係を持つワークフロー。
ソフトウェア開発プロセスをシミュレートし、DAGの特性を示す。
"""

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import workflow

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)

# workflowツールを持つエージェント
agent = Agent(model=model, tools=[workflow])

# Bedrockモデル設定（各タスクで使用）
bedrock_settings = {
    "model_id": "jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    "region_name": "ap-northeast-1",
}

# DAG構造:
#
#                      requirements
#                           │
#           ┌───────────────┼───────────────┐
#           ▼               ▼               ▼
#     frontend_dev     backend_dev      api_design
#           │               │               │
#           └───────┬───────┘               │
#                   ▼                       │
#              integration                  │
#                   │                       │
#                   │       ┌───────────────┘
#                   │       ▼
#                   │   api_impl
#                   │       │
#                   └───┬───┘
#                       ▼
#                    testing
#                       │
#                       ▼
#                    release

tasks = [
    # フェーズ1: 開始
    {
        "task_id": "requirements",
        "description": "ECサイトの新機能「お気に入り機能」の要件を3点にまとめてください。",
        "system_prompt": "あなたはプロダクトマネージャーです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "priority": 5,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    # フェーズ2: 並列開発（requirementsに依存）
    {
        "task_id": "frontend_dev",
        "description": "お気に入りボタンのUIコンポーネント仕様を簡潔に記述してください。",
        "system_prompt": "あなたはフロントエンドエンジニアです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["requirements"],
        "priority": 3,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    {
        "task_id": "backend_dev",
        "description": "お気に入りデータを保存するDBスキーマを設計してください（テーブル名、カラム名）。",
        "system_prompt": "あなたはバックエンドエンジニアです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["requirements"],
        "priority": 3,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    {
        "task_id": "api_design",
        "description": "お気に入り追加/削除/一覧取得のREST APIエンドポイントを設計してください。",
        "system_prompt": "あなたはAPIアーキテクトです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["requirements"],
        "priority": 3,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    # フェーズ3: 部分的な依存
    {
        "task_id": "integration",
        "description": "フロントエンドUIとバックエンドDBの連携ポイントを特定してください。",
        "system_prompt": "あなたはインテグレーションエンジニアです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["frontend_dev", "backend_dev"],
        "priority": 3,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    {
        "task_id": "api_impl",
        "description": "API設計とDBスキーマに基づいて、エンドポイントの実装方針をまとめてください。",
        "system_prompt": "あなたはバックエンドエンジニアです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["api_design", "backend_dev"],
        "priority": 3,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    # フェーズ4: テスト
    {
        "task_id": "testing",
        "description": "統合テストとAPIテストの観点を各3つずつ挙げてください。",
        "system_prompt": "あなたはQAエンジニアです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["integration", "api_impl"],
        "priority": 5,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
    # フェーズ5: リリース
    {
        "task_id": "release",
        "description": "リリースチェックリストを5項目で作成してください。",
        "system_prompt": "あなたはリリースマネージャーです。簡潔に回答してください。ツールは使わず、あなたの知識だけで回答してください。",
        "dependencies": ["testing"],
        "priority": 5,
        "model_provider": "bedrock",
        "model_settings": bedrock_settings,
    },
]

print("=== 複雑なDAGワークフロー: ソフトウェア開発プロセス ===")
print()
print("DAG構造:")
print("                requirements")
print("                     │")
print("         ┌───────────┼───────────┐")
print("         ▼           ▼           ▼")
print("   frontend_dev  backend_dev  api_design")
print("         │           │           │")
print("         └─────┬─────┘           │")
print("               ▼                 │")
print("          integration            │")
print("               │       ┌─────────┘")
print("               │       ▼")
print("               │   api_impl")
print("               │       │")
print("               └───┬───┘")
print("                   ▼")
print("                testing")
print("                   │")
print("                   ▼")
print("                release")
print()

# 1. ワークフロー作成
print("1. ワークフローを作成...")
agent.tool.workflow(
    action="create",
    workflow_id="release_process",
    tasks=tasks,
)
print("   作成完了\n")

# 2. ワークフロー開始（同期的に完了まで待機）
print("2. ワークフローを開始...")
print("   ※ 複雑なDAG構造に従って実行されます")
start_result = agent.tool.workflow(
    action="start",
    workflow_id="release_process",
)
print(f"   結果: {start_result}\n")

# startアクションは同期的に完了を待つため、結果を確認
start_result_str = str(start_result).lower()
if "completed successfully" in start_result_str:
    print("=== ワークフロー完了（成功） ===")
elif "failed" in start_result_str:
    print("=== ワークフロー完了（失敗あり） ===")
else:
    print("3. 最終ステータスを確認...")
    status = agent.tool.workflow(
        action="status",
        workflow_id="release_process",
    )
    print(f"   最終ステータス: {status}")
    print("\n=== ワークフロー完了 ===")
