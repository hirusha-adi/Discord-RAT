import os

_cwd = os.getcwd()
_database = os.path.join(_cwd, "bot", "database")


main = os.path.join(
    _database,
    "data",
    "main.json"
)
