import json

config = {}


def __load_config__(path):
    with open(path) as secrets_file:
        secrets = json.load(secrets_file)
        return secrets


def init_config(path):
    secrets = __load_config__(path)
    config['ADMIN_KEY'] = secrets.get('ADMIN_KEY')