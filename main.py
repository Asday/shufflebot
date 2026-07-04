import os

import fastapi


app = fastapi.FastAPI()


def task():
    print(os.environ.get("SLACK_APP_ID"))


@app.get("/")
def home(background_tasks: fastapi.BackgroundTasks):
    background_tasks.add_task(task)

    return
