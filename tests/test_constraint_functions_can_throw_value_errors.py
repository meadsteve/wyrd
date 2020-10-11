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
