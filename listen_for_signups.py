import json
import os
import typing

import fastapi
import fastapi.staticfiles
import pydantic
import requests

import settings


app = fastapi.FastAPI()


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


class ShufflebotConfig(pydantic.BaseModel):
    invite_message: str
    button_text: str
    confirmation_message: str
    welcome_message: str

    @classmethod
    def load(cls):
        with open(settings.CONFIG_FILE, "r") as f:
            return cls.model_validate_json(f.read())

    def save(self):
        with open(settings.CONFIG_FILE, "w") as f:
            f.write(self.model_dump_json(indent=2))


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
            "text": ShufflebotConfig.load().confirmation_message,
        },
    )


@app.get("/config")
def config() -> ShufflebotConfig:
    return ShufflebotConfig.load()


class ShufflebotConfigPOST(pydantic.BaseModel):
    config: ShufflebotConfig
    passkey: str


@app.post("/config")
def config(scp: ShufflebotConfigPOST) -> ShufflebotConfig:
    if scp.passkey != settings.CONFIG_PASSKEY:
        raise fastapi.HTTPException(status_code=403)

    scp.config.save()

    return scp.config


app.mount(
    "/",
    fastapi.staticfiles.StaticFiles(directory="static", html=True),
    name="static",
)
