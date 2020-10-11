import pytest

from constrained_types import UnmetConstraintError, ConstrainedString, add_constraint


@add_constraint(lambda x: x == "steve", "Only steve is steve")
class Steve(ConstrainedString):
    pass


@add_constraint(lambda x: len(x) >= 1, "must not be empty")
@add_constraint(lambda x: len(x) <= 10, "must not be longer than 10 chars")
class ShortString(ConstrainedString):
    pass


def test_its_equal_to_an_int():
    assert ConstrainedString("boop") == "boop"


def test_it_concats_like_a_string():
    assert ConstrainedString("hello") + ConstrainedString(" you") == ConstrainedString(
        "hello you"
    )


@pytest.mark.parametrize(
    "cls,value",
    [(Steve, "steve"), (ShortString, "okay")],
)
def test_if_a_constraint_is_defined_and_valid_everything_works(cls, value):
    assert cls(value) == value


@pytest.mark.parametrize(
    "cls,value,expected_error",
    [
        (Steve, "stefan", "Only steve is steve"),
        (ShortString, "", "must not be empty"),
        (ShortString, "a" * 11, "must not be longer than 10 chars"),
    ],
)
def test_if_a_constraint_isnt_met_on_construction_an_exception_is_raised(
    cls, value, expected_error
):
    with pytest.raises(UnmetConstraintError) as err:
        cls(value)
    assert str(err.value) == expected_error
