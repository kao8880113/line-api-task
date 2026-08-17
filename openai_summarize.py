import os

import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = (
    "あなたはSlackチャンネルのメッセージを要約するアシスタントです。"
    "以下のメッセージを日本語で簡潔に要約してください。"
    "主要なトピック、決定事項、必要なアクションがあれば含めてください。"
)


def summarize_messages(text: str, channel: str = "") -> str:
    """OpenAI Chat Completions APIでメッセージテキストを日本語要約する。"""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY が設定されていません。.env ファイルを確認してください。")

    if not text.strip():
        raise ValueError("要約対象のメッセージがありません。")

    channel_label = channel or "Slack"
    user_prompt = f"チャンネル: {channel_label}\n\n{text}"

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        },
        timeout=60,
    )

    if not response.ok:
        raise RuntimeError(
            f"OpenAI API に失敗しました: {response.status_code} {response.text}"
        )

    result = response.json()
    content = result["choices"][0]["message"]["content"]
    return content.strip()
