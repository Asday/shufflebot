import json
import os

import requests

import settings


response = requests.post(
    "https://slack.com/api/chat.postMessage",
    headers={
        "Authorization": f"Bearer {settings.TOKEN}",
    },
    json={
        "channel": settings.CHANNEL,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "Are you free for the shuffle this Friday?"
                        "  It's in your calendar for 12:45 (UK time),"
                        " and you'll be grouped up with some other"
                        " temsters to talk about anything other than"
                        " work for 15 minutes."
                    ),
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

data = response.json()

with open(settings.STATE_DIR / "shuffle-message.json", "w") as f:
    json.dump({"channel": data["channel"], "ts": data["ts"]}, f)
