import json
import logging


class AppConfig:
    admin_key: str
    api_hash: str
    api_id: int
    bot_token: str
    log_lvl: str
    log_file_path: str
    redis_host: str
    redis_port: int


app_config = AppConfig()


def __load_config__(path):
    with open(path) as secrets_file:
        cfg: dict = json.load(secrets_file)
        return cfg


def init_config(path):
    cfg = __load_config__(path)
    app_config.api_hash = cfg['API_HASH']
    app_config.api_id = cfg['API_ID']
    app_config.bot_token = cfg['BOT_TOKEN']
    app_config.log_lvl = logging.getLevelNamesMapping()[cfg['LOG_LVL']]
    app_config.log_file_path = cfg['LOG_FILE_PATH']
    app_config.redis_port = cfg['REDIS_PORT']
    app_config.redis_host = cfg['REDIS_HOST']

    try:
        app_config.admin_key = cfg['ADMIN_KEY']
    except KeyError:
        app_config.admin_key = ''
