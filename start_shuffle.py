import json

import requests

import settings


for path in (settings.STATE_DIR / "who-up").iterdir():
    path.unlink()

with open(settings.CONFIG_FILE, "r") as f:
    config = json.load(f)
    invite_message = config["invite_message"]
    button_text = config["button_text"]

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
                    "text": invite_message,
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": button_text,
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
