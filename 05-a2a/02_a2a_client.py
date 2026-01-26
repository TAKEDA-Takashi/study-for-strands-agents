"""
02_a2a_client.py - A2Aクライアント

A2Aプロトコルでサーバーに接続し、リモートエージェントを呼び出す。

前提条件:
    01_a2a_server.py が別ターミナルで実行中であること

実行方法:
    uv run python 05-a2a/02_a2a_client.py
"""

import asyncio
import uuid

import httpx
from a2a.client import A2AClient
from a2a.types import Message, MessageSendParams, Part, Role, SendMessageRequest, TextPart

A2A_SERVER_URL = "http://127.0.0.1:9000"


async def main():
    print("=== A2Aクライアント ===")
    print(f"接続先: {A2A_SERVER_URL}\n")

    async with httpx.AsyncClient() as httpx_client:
        # A2Aクライアントの作成
        client = A2AClient(httpx_client=httpx_client, url=A2A_SERVER_URL)

        # エージェントカードの取得（サーバー情報の確認）
        print("--- エージェント情報の取得 ---")
        agent_card = await client.get_card()
        print(f"エージェント名: {agent_card.name}")
        print(f"説明: {agent_card.description}")
        print()

        # メッセージの送信
        print("--- メッセージ送信: 計算リクエスト ---")
        message = Message(
            message_id=str(uuid.uuid4()),
            role=Role.user,
            parts=[Part(root=TextPart(text="100 + 200 * 3 を計算してください"))],
        )
        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(message=message),
        )
        response = await client.send_message(request)
        print(f"レスポンス: {response}")
        print()

        print("--- メッセージ送信: 挨拶リクエスト ---")
        message2 = Message(
            message_id=str(uuid.uuid4()),
            role=Role.user,
            parts=[Part(root=TextPart(text="田中さんに挨拶してください"))],
        )
        request2 = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(message=message2),
        )
        response2 = await client.send_message(request2)
        print(f"レスポンス: {response2}")


if __name__ == "__main__":
    asyncio.run(main())
