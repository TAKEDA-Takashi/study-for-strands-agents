"""
02_a2a_client.py - A2Aクライアント

A2Aプロトコルでサーバーに接続し、リモートエージェントを呼び出す。

前提条件:
    01_a2a_server.py が別ターミナルで実行中であること

実行方法:
    uv run python 05-a2a/02_a2a_client.py
"""

import asyncio
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, TextPart

A2A_SERVER_URL = "http://127.0.0.1:9000"


async def main():
    print("=== A2Aクライアント ===")
    print(f"接続先: {A2A_SERVER_URL}\n")

    async with httpx.AsyncClient(timeout=300) as httpx_client:
        # エージェントカードの取得（サーバー情報の確認）
        print("--- エージェント情報の取得 ---")
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=A2A_SERVER_URL)
        agent_card = await resolver.get_agent_card()
        print(f"エージェント名: {agent_card.name}")
        print(f"説明: {agent_card.description}")
        print()

        # ClientFactoryでクライアントを作成
        config = ClientConfig(httpx_client=httpx_client, streaming=False)
        factory = ClientFactory(config)
        client = factory.create(agent_card)

        # メッセージの送信
        print("--- メッセージ送信: 計算リクエスト ---")
        message = Message(
            role=Role.user,
            parts=[Part(TextPart(text="100 + 200 * 3 を計算してください"))],
            message_id=uuid4().hex,
        )
        async for event in client.send_message(message):
            print(f"レスポンス: {event}")
        print()

        print("--- メッセージ送信: 挨拶リクエスト ---")
        message2 = Message(
            role=Role.user,
            parts=[Part(TextPart(text="田中さんに挨拶してください"))],
            message_id=uuid4().hex,
        )
        async for event in client.send_message(message2):
            print(f"レスポンス: {event}")


if __name__ == "__main__":
    asyncio.run(main())
