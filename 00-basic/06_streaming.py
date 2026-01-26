"""
06_streaming.py - ストリーミング出力

エージェントの応答をストリーミングでリアルタイムに出力する。
"""

import sys

from strands import Agent
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


# ストリーミングコールバック関数
def stream_callback(**event: object) -> None:
    """ストリーミングイベントを処理するコールバック。"""
    if "data" in event:
        # テキストデータを即座に出力
        sys.stdout.write(str(event["data"]))
        sys.stdout.flush()


# ストリーミング有効のエージェント
agent = Agent(
    model=model,
    system_prompt="あなたは物語を語る詩人です。美しい言葉で短い物語を作ってください。",
    callback_handler=stream_callback,
)

print("=== ストリーミング出力 ===")
# ストリーミングで応答を受け取る
response = agent("桜の木の下で出会った二人の物語を、3文で教えてください。")

print("\n\n=== 最終レスポンス ===")
print(f"完了: {response}")
