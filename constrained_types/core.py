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
    def decorate(original_class):
        if not (
            hasattr(original_class, "_constraints")
            and hasattr(original_class, "_validate")
        ):
            raise SyntaxError("Class must implement Constrained protocol")
        new_constraints = [(func, err_msg)] + original_class._constraints

        class NewClass(original_class):  # type: ignore
            _constraints = new_constraints

        return NewClass

    return decorate


class Constrained(Protocol):
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]]

    @classmethod
    def _validate(cls: Type[T], value: T):
        ...
