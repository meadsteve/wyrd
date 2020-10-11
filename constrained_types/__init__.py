from typing import Any, Tuple, Callable, List, ClassVar, Type, TypeVar

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore

T = TypeVar("T", bound="Constrained")

ConstraintFunc = Callable[[T], bool]


class UnmetConstraintError(RuntimeError):
    pass


def add_constraint(func: ConstraintFunc, err_msg: str):
    def decorate(original_class):
        new_constraints = original_class._constraints + [(func, err_msg)]

        class NewClass(original_class):  # type: ignore
            _constraints = new_constraints

        return NewClass

    return decorate


class Constrained(Protocol):
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]]

    @classmethod
    def _validate(cls: Type[T], value: T):
        ...


class ConstrainedInt(int, Constrained):
    _raw_value: Any
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]] = []

    def __init__(self, value: Any):
        self._raw_value = value
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls: Type[T], value: T):
        _validate(value, cls._constraints)


class ConstrainedString(str, Constrained):
    _raw_value: Any
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]] = []

    def __init__(self, value: Any):
        self._raw_value = value
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls: Type[T], value: T):
        _validate(value, cls._constraints)


def _validate(value: T, constraints: List[Tuple[ConstraintFunc, str]]):
    for (is_valid, err_msg) in constraints:
        if not is_valid(value):
            raise UnmetConstraintError(err_msg)
