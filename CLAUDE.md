# Strands Agents 習作プロジェクト

## プロジェクト概要

Strands Agents SDKを使用したマルチエージェントパターンの学習リポジトリ。

## 実行方法

```bash
uv run python <script.py>
```

## 実行環境

Amazon Bedrock AgentCore Runtime を使用。
- セッション分離された専用microVM
- 最大8時間のセッション永続化
- スケーラブルなサーバーレス環境

AWS認証設定は`.claude/CLAUDE.local.md`を参照。

## デフォルトモデル

Claude Haiku 4.5（東京リージョン）を使用。

```python
from strands import Agent
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1"
)
agent = Agent(model=model)
```

## マルチエージェントパターン一覧

### 1. Agents as Tools

エージェントを`@tool`デコレーターでラップし、オーケストレーターから呼び出す階層構造。

```python
from strands import Agent, tool

@tool
def specialist_agent(query: str) -> str:
    """専門家エージェント"""
    agent = Agent(system_prompt="You are a specialist...")
    return str(agent(query))

orchestrator = Agent(tools=[specialist_agent])
```

### 2. Graph

開発者定義の有向グラフ。ノード間の依存関係に従って実行。

```python
from strands import Agent
from strands.multiagent import GraphBuilder

builder = GraphBuilder()
builder.add_node(agent_a, "node_a")
builder.add_node(agent_b, "node_b")
builder.add_edge("node_a", "node_b")
builder.set_entry_point("node_a")

graph = builder.build()
result = graph("タスク")
```

**条件分岐:**
```python
def condition_func(state):
    return "success" in str(state.results.get("node_a").result).lower()

builder.add_edge("node_a", "node_b", condition=condition_func)
```

### 3. Swarm

自律的なエージェント群がhandoffで協調。

```python
from strands import Agent
from strands.multiagent import Swarm

researcher = Agent(name="researcher", system_prompt="...")
coder = Agent(name="coder", system_prompt="...")

swarm = Swarm(
    [researcher, coder],
    entry_point=researcher,
    max_handoffs=20,
    max_iterations=20,
    execution_timeout=900.0
)
result = swarm("タスク")
```

### 4. Workflow

決定論的DAG。並列実行可能。strands-agents-toolsから使用。

```python
# タスク定義と依存関係管理
# 独立タスクは並列実行される
```

### 5. A2A (Agent-to-Agent)

オープンプロトコルによるプラットフォーム間通信。

```bash
# 追加インストールが必要
uv sync --extra a2a
```

**サーバー:**
```python
from strands import Agent
from strands.multiagent.a2a import A2AServer

agent = Agent(name="Calculator", tools=[calculator])
server = A2AServer(agent=agent)
server.serve()
```

**クライアント:**
```python
from strands.multiagent.a2a import A2AClientToolProvider

provider = A2AClientToolProvider(known_agent_urls=["http://127.0.0.1:9000"])
agent = Agent(tools=provider.tools)
```

## 共有状態

`invocation_state`パラメータでエージェント間の設定を共有（LLMには露出しない）:

```python
from strands.types.tools import ToolContext

@tool(context=True)
def my_tool(context: ToolContext, query: str) -> str:
    config = context.invocation_state.get("config")
    return f"Config: {config}"

agent = Agent(tools=[my_tool])
result = agent("query", invocation_state={"config": "value"})
```

## 組み込みツール

strands-agents-toolsで提供される主要ツール:

- `calculator` - 数式計算（SymPy）
- `python_repl` - Pythonコード実行
- `shell` - シェルコマンド実行
- `http_request` - HTTPリクエスト
- `file_read`, `file_write` - ファイル操作
- `memory` - メモリ機能
- `retrieve` - RAG検索

## 参考リンク

- [Strands Agents 公式ドキュメント](https://strandsagents.com/)
- [GitHub - sdk-python](https://github.com/strands-agents/sdk-python)
- [GitHub - samples](https://github.com/strands-agents/samples)
- [Multi-Agent Patterns](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/multi-agent-patterns/)
- [Bedrock AgentCore Runtime](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_bedrock_agentcore/)
