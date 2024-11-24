from abc import ABC, abstractmethod

import redis


class DTO(ABC):
    @staticmethod
    def default():
        raise NotImplemented(reason='use this method with concrete successor')

    @staticmethod
    def from_json(d: dict):
        raise NotImplemented(reason='use this method with concrete successor')

    @staticmethod
    def to_json_dict(dto):
        raise NotImplemented(reason='use this method with concrete successor')


class AbstractDb(ABC):
    def __init__(self, connection_pool):
        self._r_ = redis.Redis(connection_pool=connection_pool)
        self._r_json_ = self._r_.json()

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