from typing import List, Tuple

from .core import T, ConstraintFunc, UnmetConstraintError


def validate(value: T, constraints: List[Tuple[ConstraintFunc, str]]):
    for (is_valid, err_msg) in constraints:
        if not is_valid(value):
            raise UnmetConstraintError(err_msg)
