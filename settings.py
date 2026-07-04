import os
import pathlib


STATE_DIR = pathlib.Path(os.environ["STATE_DIRECTORY"])
TOKEN = os.environ['SHUFFLE_TOKEN']
CHANNEL = os.environ["SHUFFLE_WHO_UP_CHANNEL"]
GROUP_SIZE = int(os.environ["SHUFFLE_GROUP_SIZE"])

if GROUP_SIZE > 8:
    raise ValueError("dingus the maximum people in a group slack DM is 8")
