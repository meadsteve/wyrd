from typing import Any, Tuple

ConstraintResult = Tuple[bool, str]


class UnmetConstraintError(RuntimeError):
    pass


class ConstrainedInt(int):
    _raw_value: Any

    def __init__(self, value: Any):
        self._raw_value = value
        super().__init__()
        valid, error_msg = self._validate(self)
        if not valid:
            raise UnmetConstraintError(error_msg)

    @classmethod
    def _validate(cls, value: int) -> ConstraintResult:
        return True, ""
