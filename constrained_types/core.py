from typing import TypeVar, Callable, ClassVar, List, Tuple, Type

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
