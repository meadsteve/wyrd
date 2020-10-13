from typing import Any, ClassVar, List, Tuple, Type

from .core import Constrained, ConstraintFunc, T
from .helpers import validate


class ConstrainedInt(int, Constrained):
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]] = []

    def __init__(self, value: Any):
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls: Type[T], value: T):
        validate(value, cls._constraints)

    # For integration with pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls._validate


class ConstrainedString(str, Constrained):
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]] = []

    def __init__(self, value: Any):
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls: Type[T], value: T):
        validate(value, cls._constraints)

    # For integration with pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls._validate


class ConstrainedFloat(float, Constrained):
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]] = []

    def __init__(self, value: Any):
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls: Type[T], value: T):
        validate(value, cls._constraints)

    # For integration with pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls._validate
