import os

import requests
from dotenv import load_dotenv

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID")
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
LINE_BROADCAST_URL = "https://api.line.me/v2/bot/message/broadcast"
LINE_TEXT_MAX_LENGTH = 5000


def _line_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    }


def send_push_message(message: str, user_id: str = LINE_USER_ID) -> dict:
    """LINE Messaging APIのpush messageで指定ユーザーにテキストを送信する。"""
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError(
            "LINE_CHANNEL_ACCESS_TOKEN が設定されていません。.env ファイルを確認してください。"
        )
    if not user_id:
        raise ValueError("LINE_USER_ID が設定されていません。.env ファイルを確認してください。")

    if len(message) > LINE_TEXT_MAX_LENGTH:
        message = message[:LINE_TEXT_MAX_LENGTH - 3] + "..."

    response = requests.post(
        LINE_PUSH_URL,
        headers=_line_headers(),
        json={
            "to": user_id,
            "messages": [{"type": "text", "text": message}],
        },
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"LINE push message に失敗しました: {response.status_code} {response.text}"
        )

    return response.json()


def send_broadcast_message(message: str) -> None:
    """LINE Messaging APIのbroadcastで全フォロワーにテキストを送信する。"""
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError(
            "LINE_CHANNEL_ACCESS_TOKEN が設定されていません。.env ファイルを確認してください。"
        )

    if len(message) > LINE_TEXT_MAX_LENGTH:
        message = message[:LINE_TEXT_MAX_LENGTH - 3] + "..."

    response = requests.post(
        LINE_BROADCAST_URL,
        headers=_line_headers(),
        json={"messages": [{"type": "text", "text": message}]},
        timeout=30,
    )
    print(response.status_code, response.text)


if __name__ == "__main__":
    send_broadcast_message("こんにちは!シェアスペース案内BOTからのテストメッセージです。")
