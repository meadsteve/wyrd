from threading import Lock
from typing import TypeVar, Generic, Type

T = TypeVar("T")


class ReadOnce(Generic[T]):
    has_been_read: bool = False
    _lock: Lock
    __contents: T

    def __init__(self, value: T):
        self.__value = value
        self._lock = Lock()

    def get_contents(self) -> T:
        try:
            self._lock.acquire()
            if self.has_been_read:
                raise RuntimeError(
                    "Attempted to read a ReadOnce value for the second time"
                )
            self.has_been_read = True
            return self.__value
        finally:
            self._lock.release()

    @property
    def type(self) -> Type[T]:
        return type(self.__value)

    def isinstance(self, t: Type) -> bool:
        return isinstance(self.__value, t)
