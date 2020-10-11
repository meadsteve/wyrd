import pytest

from constrained_types import add_constraint, ConstrainedString, UnmetConstraintError


@add_constraint(lambda x: len(x) >= 2, "must be longer than 2 chars")
@add_constraint(lambda x: len(x) >= 1, "must be longer than 1 char")
class SomeString(ConstrainedString):
    pass


def test_the_first_listed_constraint_is_checked_first():
    with pytest.raises(UnmetConstraintError) as err:
        SomeString("")
    assert str(err.value) == "must be longer than 2 chars"
