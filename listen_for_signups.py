import json
import os
import typing

import fastapi
import pydantic
import requests

import settings


app = fastapi.FastAPI()


def task():
    print(os.environ.get("SLACK_APP_ID"))


@app.get("/")
def home(background_tasks: fastapi.BackgroundTasks):
    background_tasks.add_task(task)


class User(pydantic.BaseModel):
    id_: str = pydantic.Field(..., alias="id")


class Action(pydantic.BaseModel):
    action_id: str


class BlockActions(pydantic.BaseModel):
    type_: typing.Literal["block_actions"] = pydantic.Field(..., alias="type")
    user: User
    actions: pydantic.conlist(Action, min_length=1)


@app.post("/interactivity")
async def slack_callback(rq: fastapi.Request, bt: fastapi.BackgroundTasks):
    # TODO: verify request.
    # docs.slack.dev/authentication/verifying-requests-from-slack/
    async with rq.form() as form:
        data = json.loads(form["payload"])  # Slack is insane.

    bt.add_task(callback_task, data=data)


def callback_task(data: typing.Any):
    ba = BlockActions(**data)

    (settings.STATE_DIR / "who-up" / ba.user.id_).touch()

    requests.post(
        "https://slack.com/api/chat.postEphemeral",
        headers={
            "Authorization": f"Bearer {settings.TOKEN}",
        },
        json={
            "user": ba.user.id_,
            "channel": settings.CHANNEL,
            "text": (
                "You're signed up for this Friday.  You'll be shuffled"
                " into groups on the day."
            ),
        },
    )
