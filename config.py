from orjson import loads, dumps, OPT_INDENT_2

from os.path import isfile

EXAMPLE_CONFIG = {
    "token": "",
    "valided_role": 0,
}

if not isfile("config.json"):
    with open("config.json", "wb") as config_file:
        config_file.write(dumps(EXAMPLE_CONFIG, option=OPT_INDENT_2))
    input("未發現設定檔，已重新生成\n請於修改完成後按下Enter...")

with open("config.json", "rb") as config_file:
    config = loads(config_file.read())

TOKEN = config["token"]
VALID_ROLE = config["valided_role"]
