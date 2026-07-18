import itertools
import json
import random

import requests

import settings


user_ids = [p.name for p in (settings.STATE_DIR / "who-up").iterdir()]
random.shuffle(user_ids)
batches = [list(b) for b in itertools.batched(user_ids, n=settings.GROUP_SIZE)]

# `itertools.batched()` fills all the groups by leaving the last one
# short.  This is a lonely shuffle experience, so if the last group is
# short, redistribute its members into other groups.
if batches and len(batches[-1]) != settings.GROUP_SIZE and len(batches) > 1:
    invaders = batches.pop()
    for i, invader in enumerate(invaders):
        batches[i % len(batches)].append(invader)

channel_ids = []

for batch in batches:
    response = requests.post(
        "https://slack.com/api/conversations.open",
        headers={"Authorization": f"Bearer {settings.TOKEN}"},
        json={"users": ", ".join(batch)},
    )
    data = response.json()

    # TODO: if a user gets booted between reacting to the shuffle signup
    # message and the shuffle finalisation, their whole group will
    # silently not be invited to a shuffle.  Sad times.
    #
    # Ways round this would be:
    #
    #   retry the call repeatedly, removing people until it works; or
    #   get the `users.read` permission and
    #     list all the users in the workspace, filtering them from the
    #       list before shuffling; or
    #     iterate through the list and query user info for each user
    #       before shuffling.
    #
    # Best option seems to be the middle one, but I didn't set that
    # permission and I can't currently be bothered because it will
    # hopefully be rare.
    if data["ok"]: channel_ids.append(data["channel"]["id"])

for channel_id in channel_ids:
    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {settings.TOKEN}"},
        json={
            "channel": channel_id,
            "text": (
                "Welcome to the shuffle, where we discuss anything not"
                " work related for fifteen minutes, to better maintain"
                " company culture even in a remote setting.\n"
                "\n"
                "When the time comes (it's in your calendar), any one"
                " of you should start a huddle in here."
            ),
        }
    )

with open(settings.STATE_DIR / "shuffle-message.json", "r") as f:
    shuffle_message = json.load(f)

requests.post(
    "https://slack.com/api/chat.delete",
    headers={"Authorization": f"Bearer {settings.TOKEN}"},
    json=shuffle_message,
)
