import os
import pathlib


STATE_DIR = pathlib.Path(os.environ["STATE_DIRECTORY"])
TOKEN = os.environ['SHUFFLE_TOKEN']
CHANNEL = os.environ["SHUFFLE_WHO_UP_CHANNEL"]
