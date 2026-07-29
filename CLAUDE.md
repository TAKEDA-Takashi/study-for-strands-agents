# study-for-strands-agents

グローバル規約（日本語・品質ゲート・TDD・YAGNI等）は `~/.claude/CLAUDE.md` にある。ここには本プロジェクト固有の情報だけを書く。

## 概要

Strands Agents SDK でマルチエージェントパターンを学ぶための習作リポジトリ。動くコードは `00-basic/` 〜 `06-composite/` のサンプルが正で、この CLAUDE.md はサンプルの索引と、コードを読んだだけでは気づきにくい知見だけを持つ。API の書き方をここに写すと SDK 更新で嘘になるため、コード例はサンプル側に置く。

- ディレクトリとパターンの対応表・学習順序: `README.md`
- 各パターンの解説記事と図: `docs/blog/`（サンプルを変更すると記事の記述とずれる）
- AWS 認証と東京リージョンで使えるモデル一覧: `.claude/CLAUDE.local.md`（コミット対象外）

## 実行

```bash
uv run python 02-graph/01_sequential_graph.py
```

A2A のサンプル（`05-a2a/`）だけは追加依存が必要で、`uv sync` では入らない。

```bash
uv sync --extra a2a
```

## デフォルトモデル

Claude Haiku 4.5 を東京リージョンで使う。model id は cross-region inference profile の `jp.` 接頭辞付き（`jp.anthropic.claude-haiku-4-5-20251001-v1:0`）で、接頭辞なしの素の model id では呼び出せない。

実行環境として Amazon Bedrock AgentCore Runtime を使う場合、セッションごとに分離された microVM 上で動き、セッションは最大8時間永続化される。

## パターン別の知見

### Agents as Tools（`01-agents-as-tools/`）

エージェントを `@tool` デコレーターでラップし、オーケストレーターから呼び出す階層構造。専門家を増やすほどオーケストレーターのツール選択の問題になる。

### Graph（`02-graph/`）

開発者が定義した有向グラフをノード間の依存関係に従って実行する。DAG だけでなくループ（サイクル）もサポートする。

- 条件分岐は `add_edge(..., condition=関数)`。条件関数は `GraphState` を受け取り、`state.results.get("ノード名").result` から前のノードの出力を読んで真偽を返す（`02_conditional_graph.py`）
- ループは条件付きエッジで前のノードに戻す。`set_max_node_executions(3)` を付けないと無限ループを止める仕組みがない（`03_loop_graph.py`）

### Swarm（`03-swarm/`）

自律的なエージェント群が handoff で協調する。

- 共有作業メモリを持ち、すべてのエージェントが過去の作業履歴にアクセスできる
- `handoff_to_agent` ツールでエージェント間の制御転送が自動的に行われ、専門性に基づいてタスクが振り分けられる
- `entry_point` / `max_handoffs` / `max_iterations` / `execution_timeout` で暴走を抑える（`01_basic_swarm.py`）
- 失敗したときにエージェント自身の判断で前のエージェントに戻る（バックトラック）ことができる（`03_backtrack_swarm.py`）

Graph との違い: Graph は条件関数（コード）でルーティングを定義し、Swarm はエージェント（LLM）が文脈を理解してルーティングを判断する。ループも Graph は `set_max_node_executions` と条件関数で制御するが、Swarm はエージェント自身が「うまくいかない」と判断して戻る。決定論的な制御が必要なら Graph を選ぶ。

### Workflow（`04-workflow/`）

決定論的な DAG で並列実行する。SDK 本体ではなく strands-agents-tools の `workflow` ツールを使い、`agent.tool.workflow(action=...)` を通してプログラム的に制御する（アクションは create, start, status, pause, resume）。タスクの依存は `dependencies` で宣言する。

### A2A（`05-a2a/`）

オープンプロトコルによるプラットフォーム間通信。エージェントを `A2AServer` で HTTP サーバーとして公開する。

クライアント側は2通りある。`A2AClientToolProvider`（`known_agent_urls` を渡してツールとして使う）と、`a2a.client` を直接使う方法（`A2ACardResolver` でエージェントカードを取得 → `ClientFactory` でクライアント生成）。どちらも `05-a2a/` のサンプルを参照。`02_a2a_client.py` は `01_a2a_server.py` が別ターミナルで起動済みであることが前提。

### Composite（`06-composite/`）

Graph + Swarm + Agents as Tools の組み合わせ。

- Swarm は `MultiAgentBase` を継承しているため、`GraphBuilder.add_node()` にそのまま渡せる。関数でラップする必要はない（`02_planning_with_swarm.py`）
- ツールを持つ Agent も同じように直接ノードにできるので、1つのグラフに Swarm・Agent・オーケストレーターを混在させられる（`03_full_composite.py`）

## 共有状態（invocation_state）

`agent("query", invocation_state={...})` で渡した値は、`@tool(context=True)` を付けたツールから `ToolContext.invocation_state` 経由で読める。LLM には露出しないので、プロンプトに載せたくない設定（ユーザー識別子や実行時の構成）の受け渡しに使う。サンプルは `00-basic/07_tool_context.py`。

## 組み込みツール

strands-agents-tools が提供する主なもの: `calculator`（SymPy による数式計算）、`python_repl`、`shell`、`http_request`、`file_read` / `file_write`、`memory`、`retrieve`（RAG 検索）。使用例は `00-basic/04_builtin_tools.py`。

## 参考リンク

- [Strands Agents 公式ドキュメント](https://strandsagents.com/)
- [Multi-Agent Patterns](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/multi-agent-patterns/)
- [Agent-to-Agent (A2A)](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agent-to-agent/)
- [A2A Protocol 公式サイト](https://a2a-protocol.org/)
- [Bedrock AgentCore Runtime](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_bedrock_agentcore/)
- [GitHub - sdk-python](https://github.com/strands-agents/sdk-python)
- [GitHub - samples](https://github.com/strands-agents/samples)
