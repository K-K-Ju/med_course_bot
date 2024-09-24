import json
import logging

config = {}


def __load_config__(path):
    with open(path) as secrets_file:
        cfg: dict = json.load(secrets_file)
        return cfg


def init_config(path):
    cfg = __load_config__(path)
    config['LOG_LVL'] = logging.getLevelNamesMapping()[cfg['LOG_LVL']]
    config['LOG_FILE_PATH'] = cfg['LOG_FILE_PATH']
    config['REDIS_HOST'] = cfg['REDIS_HOST']
    config['REDIS_PORT'] = cfg['REDIS_PORT']
    try:
        config['ADMIN_KEY'] = cfg['ADMIN_KEY']
    except KeyError:
        config['ADMIN_KEY'] = ''
