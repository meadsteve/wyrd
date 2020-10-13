import functools
from typing import TypeVar, ClassVar, List, Tuple, Type

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore


T = TypeVar("T")
U = TypeVar("U", contravariant=True)


class Constraint(Protocol[U]):
    def __call__(self, value: U) -> bool:
        ...


class Constrained(Protocol[T]):
    _constraints: ClassVar[List[Tuple[Constraint[T], str]]]

    @classmethod
    def _validate(cls: Type[T], value: T):
        ...


class UnmetConstraintError(ValueError):
    failing_constraint: Constraint

    def __init__(self, msg: str, failing_constraint: Constraint):
        super().__init__(msg)
        self.failing_constraint = failing_constraint


def add_constraint(func: Constraint[T], err_msg: str):
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
