from threading import Lock
from typing import TypeVar, Generic, Type, TYPE_CHECKING

T = TypeVar("T")

if TYPE_CHECKING:
    from pydantic.fields import ModelField


class ReadTwiceError(RuntimeError):
    def __init__(self, thing: "ReadOnce"):
        super().__init__(f"Attempted to read {repr(thing)} value for a second time")


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
                raise ReadTwiceError(self)
            self.has_been_read = True
            return self.__value
        finally:
            self._lock.release()

    def __str__(self):
        return str(self.get_contents())

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.type.__name__}>"

    def __getstate__(self):
        raise RuntimeError("ReadOnce objects can not be pickled")

    def __eq__(self, other):
        if isinstance(other, ReadOnce):
            return self.__value == other.__value
        raise RuntimeError(
            "ReadOnce objects can only be compared to other ReadOnce objects"
        )

    def __hash__(self):
        return hash(self.__value)

    @property
    def type(self) -> Type[T]:
        return type(self.__value)

    def isinstance(self, t: Type) -> bool:
        return isinstance(self.__value, t)

    # Work with pydantic
    @classmethod
    def validate(cls, v, field: "ModelField"):
        if not field.sub_fields:
            return cls(v)
        inner_type = field.sub_fields[0]
        parsed_value, error = inner_type.validate(v, {}, loc="inner?")
        if error or parsed_value is None:
            raise RuntimeError(f"Unable to construct ReadOnce field")
        return cls(parsed_value)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
