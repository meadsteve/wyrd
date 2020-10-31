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
                    f"Attempted to read {repr(self)} value for a second time"
                )
            self.has_been_read = True
            return self.__value
        finally:
            self._lock.release()

    def __str__(self):
        return str(self.get_contents())

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.type.__name__}>"

    @property
    def type(self) -> Type[T]:
        return type(self.__value)

    def isinstance(self, t: Type) -> bool:
        return isinstance(self.__value, t)

    # Pydantic integration follows
    @classmethod
    def __get_validators__(cls):
        yield cls._pydantic_validate

    @classmethod
    def _pydantic_validate(cls, raw_value, field):
        # Defer to the inner model type to validate
        if not field.sub_fields:
            raise SyntaxError("No inner field type specified")
        value, error = field.sub_fields[0].validate(raw_value, {}, loc='')
        if error:
            raise error
        # If everything was okay wrap the inner type with ReadOnce
        return cls(value)
