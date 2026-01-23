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
| `00-basic` | - | シングルエージェントの基礎 |
| `01-agents-as-tools` | Agents as Tools | エージェントをツールとしてラップ |
| `02-graph` | Graph | 有向グラフによるフロー制御 |
| `03-swarm` | Swarm | 自律的なエージェント協調 |
| `04-workflow` | Workflow | 決定論的DAGによる並列実行 |
| `05-a2a` | A2A | Agent-to-Agent プロトコル |
| `06-combined` | 複合 | パターンの組み合わせ |

## 学習順序

1. **00-basic** - Agent API の基本
2. **01-agents-as-tools** - 階層的なエージェント構造
3. **02-graph** - 明示的なフロー制御
4. **03-swarm** - 自律的な協調
5. **04-workflow** - 並列タスク処理
6. **05-a2a** - プラットフォーム間通信
7. **06-combined** - 複合パターン

## 参考リンク

- [Strands Agents Documentation](https://strandsagents.com/)
- [strands-agents/sdk-python](https://github.com/strands-agents/sdk-python)
- [strands-agents/samples](https://github.com/strands-agents/samples)
