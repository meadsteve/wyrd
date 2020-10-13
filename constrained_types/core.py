import functools
from typing import TypeVar, Callable, ClassVar, List, Tuple, Type, Any

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore


T = TypeVar("T")


class UnmetConstraintError(ValueError):
    pass


def add_constraint(func: Callable[[Any], bool], err_msg: str):
    def decorate(original_class: Type[Constrained[T]]):
        _assert_implements_constrained_protocol(original_class)
        new_constraints = [(func, err_msg)] + original_class._constraints

        class NewClass(original_class):  # type: ignore
            _constraints = new_constraints

        return NewClass

    return decorate


def cache_constraint_results(maxsize: int, typed=False):
    def decorate(original_class: Type[Constrained[T]]):
        _assert_implements_constrained_protocol(original_class)

        class NewClass(original_class):  # type: ignore
            @classmethod
            @functools.lru_cache(maxsize, typed)
            def _validate(cls, value):
                super()._validate(value)

        return NewClass

    return decorate


def _assert_implements_constrained_protocol(clas: Type):
    if not (hasattr(clas, "_constraints") and hasattr(clas, "_validate")):
        raise SyntaxError("Class must implement Constrained protocol")


class Constrained(Protocol[T]):
    _constraints: ClassVar[List[Tuple[Callable[[T], bool], str]]]

    @classmethod
    def _validate(cls: Type[T], value: T):
        ...
