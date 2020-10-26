from typing import List, Tuple, TypeVar

from .core import Constrained, UnmetConstraintError, Constraint

T = TypeVar("T", bound=Constrained)


def validate(value: T, constraints: List[Tuple[Constraint[T], str]]):
    for (is_valid, err_msg) in constraints:
        try:
            valid = is_valid(value)
        except ValueError as e:
            raise UnmetConstraintError(f"{err_msg}: {str(e)}", is_valid) from e
        if not valid:
            raise UnmetConstraintError(err_msg, is_valid)
