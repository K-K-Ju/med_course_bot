from typing import Generic, TypeVar, Union

T = TypeVar('T')
ExcType = TypeVar('ExcType', bound=Exception)


class Res(Generic[T, ExcType]):
    def __init__(self, val: Union[T, ExcType] = None):
        self.val: Union[T, ExcType] = val


class Ok(Res):
    ...


class Error(Res):
    ...
