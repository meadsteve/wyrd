import pytest

from constrained_types import ConstrainedInt, UnmetConstraintError


class NumberThree(ConstrainedInt):
    _constraints = [(lambda x: x == 3, "Only 3 is 3")]


def test_its_equal_to_an_int():
    assert ConstrainedInt(5) == 5


def test_it_sums_like_an_int():
    assert ConstrainedInt(5) + ConstrainedInt(6) == ConstrainedInt(11)


def test_if_a_constraint_is_defined_and_valid_everything_works():
    assert NumberThree(3) == 3


def test_if_a_constraint_isnt_met_on_construction_an_exception_is_raised():
    with pytest.raises(UnmetConstraintError) as err:
        NumberThree(4)
    assert str(err.value) == "Only 3 is 3"
