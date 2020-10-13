import pytest

from constrained_types import add_constraint, ConstrainedString, UnmetConstraintError
from constrained_types.helpers import validate


def some_complicated_check(_value):
    raise ValueError("I was always going to fail")


def test_constraint_functions_can_throw_value_errors():
    with pytest.raises(UnmetConstraintError) as err:
        validate(
            ConstrainedString("anything"),
            [(some_complicated_check, "Complicated check")],
        )
    assert str(err.value) == "Complicated check: I was always going to fail"


def test_failing_constraint_is_available_in_exception():
    with pytest.raises(UnmetConstraintError) as err:
        validate(
            ConstrainedString("anything"),
            [(some_complicated_check, "Complicated check")],
        )
    assert err.value.failing_constraint == some_complicated_check
