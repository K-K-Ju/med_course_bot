from abc import ABC, abstractmethod
from sqlite3 import Connection
from typing import TypeVar, List

from bot.models.dto.dto import DTO

DTOType = TypeVar('DTOType', bound=DTO)

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class AbstractDb(ABC):
    def __init__(self, connection: Connection):
        self._connection = connection
        self._connection.row_factory = dict_factory

    @abstractmethod
    def add(self, dto: DTOType) -> bool:
        raise NotImplementedError('use this method with concrete successor')

    @abstractmethod
    def get(self, idx: int) -> DTOType:
        raise NotImplementedError('use this method with concrete successor')

    @abstractmethod
    def remove(self, idx: int) -> bool:
        raise NotImplementedError('use this method with concrete successor')

    @abstractmethod
    def list(self) -> List[DTOType]:
        raise NotImplementedError('use this method with concrete successor')

class Handler(ABC):
    ...