import pytest

from wyrd.constrained_types import UnmetConstraintError, ConstrainedInt, add_constraint


@add_constraint(lambda x: x == 3, "Only 3 is 3")
class NumberThree(ConstrainedInt):
    pass


def one_or_greater(x: int) -> bool:
    return x >= 1


def ten_or_less(x: int) -> bool:
    return x <= 10


@add_constraint(one_or_greater, "must be greater than or equal to 1")
@add_constraint(ten_or_less, "must be less than or equal to 10")
class OneToTen(ConstrainedInt):
    pass


def test_its_equal_to_an_int():
    assert ConstrainedInt(5) == 5


def test_it_sums_like_an_int():
    assert ConstrainedInt(5) + ConstrainedInt(6) == 11


def test_summing_results_in_a_int_type_not_a_constrained_type():
    # Otherwise we end up with values outside the allowed range
    result = OneToTen(5) + OneToTen(6)
    assert not isinstance(result, OneToTen)
    assert isinstance(result, int)


@pytest.mark.parametrize(
    "cls,value",
    [(NumberThree, 3), (OneToTen, 6)],
)
def test_if_a_constraint_is_defined_and_valid_everything_works(cls, value):
    assert cls(value) == value


@pytest.mark.parametrize(
    "cls,value,expected_error",
    [
        (NumberThree, 4, "Only 3 is 3"),
        (OneToTen, 0, "must be greater than or equal to 1"),
        (OneToTen, 11, "must be less than or equal to 10"),
    ],
)
def test_if_a_constraint_isnt_met_on_construction_an_exception_is_raised(
    cls, value, expected_error
):
    with pytest.raises(UnmetConstraintError) as err:
        cls(value)
    assert str(err.value) == expected_error
