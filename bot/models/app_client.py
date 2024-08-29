from pyromod import Client


class AppClient:
    client = None

    def __init__(self, name, lang):
        AppClient.client = Client(name=name, lang_code=lang)
