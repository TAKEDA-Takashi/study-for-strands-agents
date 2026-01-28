# study-for-strands-agents

Strands Agents SDK を使用したマルチエージェントパターンの習作リポジトリ。

## セットアップ

```bash
uv sync
```

A2Aパターンを使用する場合:
```bash
uv sync --extra a2a
```

## ディレクトリ構成

| ディレクトリ | パターン | 説明 |
|-------------|---------|------|
| `00-basic` | - | シングルエージェントの基礎（ツール、メモリ、ストリーミング等） |
| `01-agents-as-tools` | Agents as Tools | エージェントをツールとしてラップし階層化 |
| `02-graph` | Graph | 有向グラフによるフロー制御（条件分岐、ループ対応） |
| `03-swarm` | Swarm | 自律的なエージェント協調（動的ルーティング、バックトラック） |
| `04-workflow` | Workflow | 決定論的DAGによる並列実行 |
| `05-a2a` | A2A | Agent-to-Agent プロトコル（HTTP経由） |
| `06-composite` | 複合 | Graph + Swarm + Agents as Tools の組み合わせ |

## 学習順序

1. **00-basic** - Agent API の基本（ツール、メモリ、ToolContext）
2. **01-agents-as-tools** - 階層的なエージェント構造
3. **02-graph** - 明示的なフロー制御（条件分岐、ループ）
4. **03-swarm** - 自律的な協調（動的ルーティング、バックトラック）
5. **04-workflow** - 並列タスク処理（DAG）
6. **05-a2a** - プラットフォーム間通信（HTTPプロトコル）
7. **06-composite** - 複合パターン（Graph + Swarm + Agents as Tools）

## 参考リンク

- [Strands Agents Documentation](https://strandsagents.com/)
- [strands-agents/sdk-python](https://github.com/strands-agents/sdk-python)
- [strands-agents/samples](https://github.com/strands-agents/samples)
