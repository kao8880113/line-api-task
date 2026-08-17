"""Slackメッセージ取得 → OpenAI要約 → LINE push送信の一連処理。"""

from slack_fetch import (
    SLACK_BOT_TOKEN,
    SLACK_CHANNEL,
    fetch_messages,
    format_message,
    messages_to_text,
)
from openai_summarize import summarize_messages
from send_line import send_push_message


def run(limit: int = 20) -> None:
    if not SLACK_BOT_TOKEN:
        print("エラー: SLACK_BOT_TOKEN が設定されていません。.env ファイルを確認してください。")
        return

    print(f"1. チャンネル {SLACK_CHANNEL} からメッセージを取得中...")
    try:
        messages = fetch_messages(limit=limit)
    except (RuntimeError, ValueError) as exc:
        print(f"エラー: {exc}")
        return

    if not messages:
        print("メッセージが見つかりませんでした。")
        return

    print(f"   取得件数: {len(messages)} 件")

    text = messages_to_text(messages)
    if not text.strip():
        print("要約可能なテキストメッセージがありませんでした。")
        return

    print("2. OpenAI APIで要約中...")
    try:
        summary = summarize_messages(text, channel=SLACK_CHANNEL)
    except (RuntimeError, ValueError) as exc:
        print(f"エラー: {exc}")
        return

    print("\n--- 要約結果 ---")
    print(summary)
    print("----------------\n")

    print("3. LINE push messageで送信中...")
    try:
        send_push_message(summary)
    except (RuntimeError, ValueError) as exc:
        print(f"エラー: {exc}")
        return

    print("LINEへの送信が完了しました。")


def main() -> None:
    run()


if __name__ == "__main__":
    main()
