import json
import logging

config = {}


def __load_config__(path):
    with open(path) as secrets_file:
        cfg = json.load(secrets_file)
        return cfg


def init_config(path):
    cfg = __load_config__(path)
    config['ADMIN_KEY'] = cfg.get('ADMIN_KEY')
    config['LOG_LVL'] = logging.getLevelNamesMapping()[cfg.get('LOG_LVL')]
    config['LOG_FILE_PATH'] = cfg.get('LOG_FILE_PATH')

