import pytest
from typeguard import typechecked

from constrained_types import ConstrainedInt, add_constraint


@add_constraint(lambda x: x > 0, "must be at least 1")
class Quantity(ConstrainedInt):
    pass


@typechecked
def total_quantity(a: Quantity, b: Quantity) -> Quantity:
    return Quantity(a + b)


def test_everything_is_fine_when_the_types_are_correct():
    assert total_quantity(Quantity(1), Quantity(2)) == Quantity(3)


def test_error_raised_for_incorrect_types():
    with pytest.raises(TypeError):
        total_quantity(Quantity(1), 2)  # type: ignore
