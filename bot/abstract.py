class DAO:
    @staticmethod
    def default():
        TypeError(reason='use this method with concrete successor')

    @staticmethod
    def from_json(d: dict):
        TypeError(reason='use this method with concrete successor')

    @staticmethod
    def to_json_dict(dao):
        TypeError(reason='use this method with concrete successor')


class AbstractDb:
    def add(self, dao: DAO) -> bool:
        TypeError(reason='use this method with concrete successor')

    def get(self, id) -> DAO:
        TypeError(reason='use this method with concrete successor')

    def remove(self, id) -> bool:
        TypeError(reason='use this method with concrete successor')

    def list(self):
        TypeError(reason='use this method with concrete successor')
