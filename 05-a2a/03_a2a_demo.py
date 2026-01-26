"""
03_a2a_demo.py - A2Aサーバー・クライアント統合デモ

サーバーをバックグラウンドで起動し、クライアントからアクセスするデモ。
単一スクリプトでA2Aの動作を確認できる。

実行方法:
    uv run python 05-a2a/03_a2a_demo.py
"""

import asyncio
import threading
import uuid

import httpx
from a2a.client import A2AClient
from a2a.types import Message, MessageSendParams, Part, Role, SendMessageRequest, TextPart
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands.multiagent.a2a import A2AServer

model = BedrockModel(
    model_id="jp.anthropic.claude-haiku-4-5-20251001-v1:0",
    region_name="ap-northeast-1",
)


@tool
def translate_to_english(text: str) -> str:
    """日本語テキストを英語に翻訳します。

    Args:
        text: 翻訳する日本語テキスト

    Returns:
        英語に翻訳されたテキスト
    """
    # 簡易的な翻訳（実際にはLLMが処理）
    translations = {
        "こんにちは": "Hello",
        "ありがとう": "Thank you",
        "さようなら": "Goodbye",
    }
    return translations.get(text, f"[Translated: {text}]")


# サーバー用エージェント
server_agent = Agent(
    model=model,
    name="TranslatorAgent",
    description="日本語から英語への翻訳を行うアシスタントエージェント",
    system_prompt="""あなたは翻訳アシスタントです。
日本語から英語への翻訳を行います。
translate_to_englishツールを使用して翻訳してください。""",
    tools=[translate_to_english],
)


def run_server():
    """サーバーを別スレッドで起動"""
    server = A2AServer(
        agent=server_agent,
        host="127.0.0.1",
        port=9001,
    )
    server.serve()


async def run_client():
    """クライアントからサーバーにアクセス"""
    # サーバー起動を待機
    await asyncio.sleep(2)

    print("--- クライアントからサーバーに接続 ---\n")

    async with httpx.AsyncClient() as httpx_client:
        client = A2AClient(httpx_client=httpx_client, url="http://127.0.0.1:9001")

        # エージェント情報の取得
        try:
            agent_card = await client.get_card()
            print(f"接続成功！エージェント: {agent_card.name}")
            print()
        except Exception as e:
            print(f"接続エラー: {e}")
            return

        # 翻訳リクエスト
        print("--- 翻訳リクエスト送信 ---")
        message = Message(
            message_id=str(uuid.uuid4()),
            role=Role.user,
            parts=[Part(root=TextPart(text="「こんにちは」を英語に翻訳してください"))],
        )
        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(message=message),
        )
        response = await client.send_message(request)
        print(f"レスポンス: {response}")


async def main():
    print("=== A2A統合デモ ===")
    print("サーバー: http://127.0.0.1:9001")
    print()

    # サーバーをバックグラウンドスレッドで起動
    print("--- サーバー起動中 ---")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # クライアント実行
    await run_client()

    print("\n--- デモ完了 ---")
    print("（サーバースレッドは自動終了します）")


if __name__ == "__main__":
    asyncio.run(main())
