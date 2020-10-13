import pytest

from constrained_types import UnmetConstraintError, ConstrainedFloat, add_constraint


@add_constraint(lambda x: x == 3.0, "Pi is exactly 3")
class PiNumber(ConstrainedFloat):
    pass


@add_constraint(lambda x: x >= 1.5, "must be greater than or equal to 1.5")
@add_constraint(lambda x: x <= 10, "must be less than or equal to 9.5")
class OneIshToTenIsh(ConstrainedFloat):
    pass


def test_its_equal_to_a_float():
    assert ConstrainedFloat(3.14159) == 3.14159


def test_it_sums_like_a_float():
    assert ConstrainedFloat(5.0) + ConstrainedFloat(1.5) == ConstrainedFloat(6.5)


@pytest.mark.parametrize(
    "cls,value",
    [(PiNumber, 3), (OneIshToTenIsh, 6.2)],
)
def test_if_a_constraint_is_defined_and_valid_everything_works(cls, value):
    assert cls(value) == value


@pytest.mark.parametrize(
    "cls,value,expected_error",
    [
        (PiNumber, 4, "Pi is exactly 3"),
        (OneIshToTenIsh, 0.3, "must be greater than or equal to 1.5"),
        (OneIshToTenIsh, 10.2, "must be less than or equal to 9.5"),
    ],
)
def test_if_a_constraint_isnt_met_on_construction_an_exception_is_raised(
    cls, value, expected_error
):
    with pytest.raises(UnmetConstraintError) as err:
        cls(value)
    assert str(err.value) == expected_error
