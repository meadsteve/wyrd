from typing import List, Tuple, TypeVar, Callable

from .core import Constrained, UnmetConstraintError

T = TypeVar("T", bound=Constrained)


def validate(value: T, constraints: List[Tuple[Callable[[T], bool], str]]):
    for (is_valid, err_msg) in constraints:
        try:
            valid = is_valid(value)
        except ValueError as e:
            raise UnmetConstraintError(f"{err_msg}: {str(e)}") from e
        if not valid:
            raise UnmetConstraintError(err_msg)
