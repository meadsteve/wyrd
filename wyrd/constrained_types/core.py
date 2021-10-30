import functools
from typing import TypeVar, ClassVar, List, Tuple, Type, Callable, Any

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore


try:
    from typing import runtime_checkable
except ImportError:
    from typing_extensions import runtime_checkable  # type: ignore


T = TypeVar("T", contravariant=True)


ConstraintFunc = Callable[[Any], bool]
Constraint = Tuple[ConstraintFunc, str]


@runtime_checkable
class Constrained(Protocol[T]):
    _constraints: ClassVar[List[Constraint]]

    @classmethod
    def _validate(cls: Type[T], value: T):
        ...


class UnmetConstraintError(ValueError):
    failing_constraint: Any

    def __init__(self, msg: str, failing_constraint: ConstraintFunc):
        super().__init__(msg)
        self.failing_constraint = failing_constraint


def add_constraint(
    func: Callable[[Any], bool], err_msg: str
) -> Callable[[Type[Constrained[T]]], Type[Constrained[T]]]:
    def decorate(original_class: Type[Constrained[T]]) -> Type[Constrained[T]]:
        _assert_implements_constrained_protocol(original_class)
        new_constraints = [(func, err_msg)] + original_class._constraints

        class NewClass(original_class):  # type: ignore
            _constraints = new_constraints

        NewClass.__name__ = original_class.__name__
        return NewClass

    return decorate


def cache_constraint_results(
    maxsize: int, typed=False
) -> Callable[[Type[Constrained[T]]], Type[Constrained[T]]]:
    def decorate(original_class: Type[Constrained[T]]) -> Type[Constrained[T]]:
        _assert_implements_constrained_protocol(original_class)

        class NewClass(original_class):  # type: ignore
            @classmethod
            @functools.lru_cache(maxsize, typed)
            def _validate(cls, value):
                super()._validate(value)

        NewClass.__name__ = original_class.__name__
        return NewClass

    return decorate


def _assert_implements_constrained_protocol(clas: Type):
    if not (hasattr(clas, "_constraints") and hasattr(clas, "_validate")):
        raise SyntaxError("Class must implement Constrained protocol")
