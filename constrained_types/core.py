import functools
from typing import TypeVar, Callable, ClassVar, List, Tuple, Type

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore


T = TypeVar("T", bound="Constrained")
ConstraintFunc = Callable[[T], bool]


class UnmetConstraintError(ValueError):
    pass


def add_constraint(func: ConstraintFunc, err_msg: str):
    def decorate(original_class: Type[Constrained]):
        _assert_implements_constrained_protocol(original_class)
        new_constraints = [(func, err_msg)] + original_class._constraints

        class NewClass(original_class):  # type: ignore
            _constraints = new_constraints

        return NewClass

    return decorate


def cache_constraint_results(maxsize: int, typed=False):
    def decorate(original_class: Type[Constrained]):
        _assert_implements_constrained_protocol(original_class)

        class NewClass(original_class):  # type: ignore
            @functools.lru_cache(maxsize, typed)
            def _validate(self, value):
                super()._validate(value)

        return NewClass

    return decorate


def _assert_implements_constrained_protocol(clas: Type):
    if not (hasattr(clas, "_constraints") and hasattr(clas, "_validate")):
        raise SyntaxError("Class must implement Constrained protocol")


class Constrained(Protocol):
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]]

    @classmethod
    def _validate(cls: Type[T], value: T):
        ...
