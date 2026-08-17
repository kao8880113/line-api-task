import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1535385432160731196/5LGzd47Lmwr0aJqGl2sgZpeTNesZxnVDyuAk0a4kmfL2Yzdyxg8Z3IOWtoxJwc6nYzk5"

message = "これは自動通知のテストです！"

requests.post(WEBHOOK_URL, json={"content": message})

print("送りました！")
