import json
from src.utils.filenames import database


with open(database.main, "r", encoding="utf-8") as _file:
    data = json.load(_file)

prefix = data['prefix']
token = data['token']
users = data['users']
channel_ids = data["channel_ids"]
