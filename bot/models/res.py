from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class Res(Generic[T]):
    def __init__(self, val: Optional[T] = None):
        self.val: Optional[T] = val


class Ok(Res):
    ...


class Error(Res):
    ...
