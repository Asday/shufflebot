import os

import requests


requests.post(
    "https://slack.com/api/chat.postMessage",
    headers={
        "Authorization": f"Bearer {os.environ['SLACK_BOT_USER_OATH_TOKEN']}",
    },
    json={
        "channel": os.environ["SLACK_WHO_UP_CHANNEL"],
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Hello world",
                }
            }
        ]
    }
)
