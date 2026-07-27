import json
import os
import pathlib


STATE_DIR = pathlib.Path(os.environ["STATE_DIRECTORY"])
(STATE_DIR / "who-up").mkdir(exist_ok=True)
CONFIG_DIR = pathlib.Path(os.environ["CONFIGURATION_DIRECTORY"])
CONFIG_FILE = CONFIG_DIR / "config.json"

if not CONFIG_FILE.exists():
    with open(CONFIG_FILE, "w") as f:
        json.dump(
            {
                "invite_message": (
                    "Are you free for the shuffle this Friday?  If so,"
                    " click the button.  The shuffle's in your calendar"
                    " for 12:45 (UK time), and you'll be grouped up"
                    " with some other team members to talk about"
                    " anything other than work for 15 minutes."
                ),
                "button_text": "Yeah",
                "confirmation_message": (
                    "You're signed up for this Friday.  You'll be"
                    " shuffled into groups on the day."
                ),
                "welcome_message": (
                    "Welcome to the shuffle, where we discuss anything"
                    " not work related for fifteen minutes, to better"
                    " maintain company culture even in a remote"
                    " setting.\n"
                    "\n"
                    "When the time comes (it's in your calendar), any"
                    " one of you should start a huddle in here."
                ),
            },
            f,
            indent=2,
        )

TOKEN = os.environ["SHUFFLE_TOKEN"]
CONFIG_PASSKEY = os.environ["SHUFFLE_CONFIG_PASSKEY"]
CHANNEL = os.environ["SHUFFLE_WHO_UP_CHANNEL"]
GROUP_SIZE = int(os.environ["SHUFFLE_GROUP_SIZE"])

assert GROUP_SIZE <= 8, "dingus the maximum people in a group slack DM is 8"
