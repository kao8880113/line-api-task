import requests

CHANNEL_ACCESS_TOKEN = "stWyGsWDC0po62b4MEeEcjYRQ/iiY4xwQkTytzLjmkuysZHRFzFawQsQuY+hJ1w+FjElKZIFGjxNSxvzXleuA0zYjJ67zIvNl1nmBjtCuusH9VOkedsOosLJol7tlGY2Hdp7cDyoxLgG3nqVGbRj+QdB04t89/1O/w1cDnyilFU="

def send_broadcast_message(message):
    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.text)

if __name__ == "__main__":
    send_broadcast_message("こんにちは!シェアスペース案内BOTからのテストメッセージです。")
