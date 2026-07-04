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
                    "type": "mrkdwn",
                    "text": "Are you free for the shuffle this Friday?"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Yeah"
                    },
                    "style": "primary",
                    "value": "yeah",
                    "action_id": "waoooooooooo"
                }
            }
        ]
    }
)
