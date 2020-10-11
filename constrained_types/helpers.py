from typing import List, Tuple

from .core import T, ConstraintFunc, UnmetConstraintError


def validate(value: T, constraints: List[Tuple[ConstraintFunc, str]]):
    for (is_valid, err_msg) in constraints:
        try:
            valid = is_valid(value)
        except ValueError as e:
            raise UnmetConstraintError(f"{err_msg}: {str(e)}") from e
        if not valid:
            raise UnmetConstraintError(err_msg)
