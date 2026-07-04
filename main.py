import os

from fastapi import BackgroundTasks, FastAPI


app = FastAPI()


def task():
    print(os.environ.get("SLACK_APP_ID"))


@app.get("/")
def home(background_tasks: BackgroundTasks):
    background_tasks.add_task(task)

    return
