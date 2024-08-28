class AppUser:
    def __init__(self, _user_id_, _chat_id_, _username_, _state_):
        self.user_id = _user_id_
        self.chat_id = _chat_id_
        self.user_name = _username_
        self.state = _state_

    @staticmethod
    def from_dict(d: dict):
        AppUser(d['chat_id'], d['username'], d['state'])
