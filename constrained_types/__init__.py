from typing import Any, Tuple, Callable, List, ClassVar, Type

ConstraintFunc = Callable[[int], bool]


class UnmetConstraintError(RuntimeError):
    pass


def add_constraint(func: ConstraintFunc, err_msg: str):
    def decorate(original_class):
        new_constraints = original_class._constraints + [(func, err_msg)]

        class NewClass(original_class):  # type: ignore
            _constraints = new_constraints

        return NewClass

    return decorate


class ConstrainedInt(int):
    _raw_value: Any
    _constraints: ClassVar[List[Tuple[ConstraintFunc, str]]] = []

    def __init__(self, value: Any):
        self._raw_value = value
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls, value: int):
        for (is_valid, err_msg) in cls._constraints:
            if not is_valid(value):
                raise UnmetConstraintError(err_msg)

    def __add__(self, other):
        return self.__class__(self._raw_value + other)

    def __radd__(self, other):
        return self.__class__(self._raw_value + other)
