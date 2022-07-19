from log.LoggerSetUp import logger
import yaml
from os import path

# Read config in $(CWD)/config.yaml

APP_ID = ""
APP_SECRET = ""
VERIFICATION_TOKEN = ""
ENCRYPT_KEY = ""
LARK_HOST = ""
PORT = -1
SOFT_DEPT_ID = ""
HARD_DEPT_ID = ""

_cfg = dict()


def readConfig(filename: str = "config.yaml"):
    global APP_ID, APP_SECRET, VERIFICATION_TOKEN, ENCRYPT_KEY, LARK_HOST, PORT
    
    if not _init_yaml(filename):
        logger.fatal("cannot init config")

    feishu: dict = _cfg.get("feishu") or dict()
    APP_ID = str(feishu.get("APP_ID"))
    APP_SECRET = str(feishu.get("APP_SECRET"))
    VERIFICATION_TOKEN = str(feishu.get("VERIFICATION_TOKEN"))
    ENCRYPT_KEY = str(feishu.get("ENCRYPT_KEY"))
    LARK_HOST = str(feishu.get("LARK_HOST"))

    server: dict = _cfg.get("server") or dict()
    PORT = int(server.get("PORT", -1))


    logger.info("Config loading success")

def _init_yaml(filename:str) -> bool:
    global _cfg
    filepath = path.join(path.curdir, filename)
    file = open(filepath, encoding="UTF-8")
    _cfg = yaml.load(file, Loader=yaml.FullLoader)  # 添加后就不警告了
    if not isinstance(_cfg, dict):
        return False
    return True
