import json
import os
import typing

import fastapi
import pydantic


app = fastapi.FastAPI()


def task():
    print(os.environ.get("SLACK_APP_ID"))


@app.get("/")
def home(background_tasks: fastapi.BackgroundTasks):
    background_tasks.add_task(task)


class User(pydantic.BaseModel):
    username: str


class Action(pydantic.BaseModel):
    action_id: str


class BlockActions(pydantic.BaseModel):
    type_: typing.Literal["block_actions"] = pydantic.Field(..., alias="type")
    user: User
    actions: pydantic.conlist(Action, min_length=1)


@app.post("/interactivity")
async def slack_callback(request: fastapi.Request):
    async with request.form() as form:
        data = json.loads(form["payload"])  # Slack is insane.

    ba = BlockActions(**data)

    return
