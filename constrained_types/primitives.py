from typing import Any, ClassVar, List, Tuple

from .core import Constrained, Constraint
from .helpers import validate


class ConstrainedInt(int, Constrained[int]):
    _constraints: ClassVar[List[Tuple[Constraint[int], str]]] = []

    def __init__(self, value: Any):
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls, value):
        validate(value, cls._constraints)

    # For integration with pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls._validate


class ConstrainedString(str, Constrained[str]):
    _constraints: ClassVar[List[Tuple[Constraint[str], str]]] = []

    def __init__(self, value: Any):
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls, value):
        validate(value, cls._constraints)

    # For integration with pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls._validate


class ConstrainedFloat(float, Constrained[float]):
    _constraints: ClassVar[List[Tuple[Constraint[float], str]]] = []

    def __init__(self, value: Any):
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls, value):
        validate(value, cls._constraints)

    # For integration with pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls._validate
