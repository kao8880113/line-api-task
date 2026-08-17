import os
import requests

SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
CHANNEL = "#all-kao"

def post_slack_message(text: str, channel: str = CHANNEL):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if result.get("ok"):
        print("メッセージ送信に成功しました")
    else:
        print(f"送信失敗: {result.get('error')}")

    return result

if __name__ == "__main__":
    post_slack_message("こんにちは!Slack APIからの投稿テストです。")
