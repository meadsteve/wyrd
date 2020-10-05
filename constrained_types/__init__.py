from typing import Any, Tuple, Callable, List, NoReturn, ClassVar


class UnmetConstraintError(RuntimeError):
    pass


class ConstrainedInt(int):
    _raw_value: Any
    _constraints: ClassVar[List[Tuple[Callable[[int], bool], str]]] = []

    def __init__(self, value: Any):
        self._raw_value = value
        super().__init__()
        self._validate(self)

    @classmethod
    def _validate(cls, value: int):
        for (is_valid, err_msg) in cls._constraints:
            if not is_valid(value):
                raise UnmetConstraintError(err_msg)
