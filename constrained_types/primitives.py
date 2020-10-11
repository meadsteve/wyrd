from typing import Any, ClassVar, List, Tuple, Type

from .core import Constrained, ConstraintFunc, T
from .helpers import validate


class ConstrainedInt(int, Constrained):
    _raw_value: Any
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]] = []

    def __init__(self, value: Any):
        self._raw_value = value
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls: Type[T], value: T):
        validate(value, cls._constraints)


class ConstrainedString(str, Constrained):
    _raw_value: Any
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]] = []

    def __init__(self, value: Any):
        self._raw_value = value
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls: Type[T], value: T):
        validate(value, cls._constraints)
