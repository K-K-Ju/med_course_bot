from abc import ABC, abstractmethod
from sqlite3 import Connection

from bot.models.dto.dto import DTO


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class AbstractDb(ABC):
    def __init__(self, connection: Connection):
        self._connection_ = connection
        self._connection_.row_factory = dict_factory

    @abstractmethod
    def add(self, dto: DTO) -> bool:
        raise NotImplemented(reason='use this method with concrete successor')

    @abstractmethod
    def get(self, idx) -> DTO:
        raise NotImplemented(reason='use this method with concrete successor')

    @abstractmethod
    def remove(self, idx) -> bool:
        raise NotImplemented(reason='use this method with concrete successor')

    @abstractmethod
    def list(self):
        raise NotImplemented(reason='use this method with concrete successor')

class Handler(ABC):
    ...