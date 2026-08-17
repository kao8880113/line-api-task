import os
from datetime import datetime
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "#all-kao")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
SLACK_API_BASE = "https://slack.com/api"


def _slack_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8",
    }


def _format_slack_error(method: str, result: dict) -> str:
    error = result.get("error", "unknown")
    message = f"{method} に失敗しました: {error}"
    if result.get("needed"):
        message += f" (必要なスコープ: {result['needed']})"
    if result.get("provided"):
        message += f" (付与済みスコープ: {result['provided']})"
    return message


def _find_channel_id_by_type(channel_name: str, channel_type: str) -> Optional[str]:
    """指定タイプのチャンネル一覧から名前でチャンネルIDを検索する。"""
    name = channel_name.lstrip("#")
    cursor = None

    while True:
        params: dict = {
            "types": channel_type,
            "limit": 200,
            "exclude_archived": True,
        }
        if cursor:
            params["cursor"] = cursor

        response = requests.get(
            f"{SLACK_API_BASE}/conversations.list",
            headers=_slack_headers(),
            params=params,
            timeout=30,
        )
        result = response.json()

        if not result.get("ok"):
            raise RuntimeError(_format_slack_error("conversations.list", result))

        for channel in result.get("channels", []):
            if channel.get("name") == name:
                return channel["id"]

        cursor = result.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    return None


def get_channel_id(channel_name: str) -> str:
    """チャンネル名（例: #all-kao）からチャンネルIDを取得する。"""
    if SLACK_CHANNEL_ID:
        return SLACK_CHANNEL_ID

    # types に public_channel と private_channel を同時指定すると
    # channels:read と groups:read の両方が必要になるため、個別に検索する。
    channel_id = _find_channel_id_by_type(channel_name, "public_channel")
    if channel_id:
        return channel_id

    channel_id = _find_channel_id_by_type(channel_name, "private_channel")
    if channel_id:
        return channel_id

    raise ValueError(f"チャンネル '{channel_name}' が見つかりません")


def fetch_messages(channel: str = SLACK_CHANNEL, limit: int = 20) -> list[dict]:
    """conversations.history で指定チャンネルの直近メッセージを取得する。"""
    channel_id = get_channel_id(channel)

    response = requests.get(
        f"{SLACK_API_BASE}/conversations.history",
        headers=_slack_headers(),
        params={"channel": channel_id, "limit": limit},
        timeout=30,
    )
    result = response.json()

    if not result.get("ok"):
        raise RuntimeError(_format_slack_error("conversations.history", result))

    return result.get("messages", [])


def format_timestamp(ts: str) -> str:
    return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")


def format_message(message: dict) -> str:
    ts = format_timestamp(message["ts"])
    user = message.get("user") or message.get("bot_id") or "unknown"
    text = message.get("text") or "(テキストなし)"
    return f"[{ts}] {user}: {text}"


def messages_to_text(messages: list[dict]) -> str:
    """要約用にメッセージをテキスト化する（古い順）。"""
    lines = []
    for message in reversed(messages):
        if message.get("subtype") in ("channel_join", "channel_leave"):
            continue
        text = message.get("text")
        if not text:
            continue
        lines.append(format_message(message))
    return "\n".join(lines)


def main() -> None:
    if not SLACK_BOT_TOKEN:
        print("エラー: SLACK_BOT_TOKEN が設定されていません。.env ファイルを確認してください。")
        return

    print(f"チャンネル {SLACK_CHANNEL} からメッセージを取得中...")

    try:
        messages = fetch_messages()
    except (RuntimeError, ValueError) as exc:
        print(f"エラー: {exc}")
        return

    if not messages:
        print("メッセージが見つかりませんでした。")
        return

    print(f"\n取得件数: {len(messages)} 件（新しい順）\n")
    for message in messages:
        print(format_message(message))


if __name__ == "__main__":
    main()
