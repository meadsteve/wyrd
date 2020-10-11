import pytest

from constrained_types import (
    ConstrainedString,
    cache_constraint_results,
    add_constraint,
    UnmetConstraintError,
)


checks_made = 0


def some_expensive_check(value):
    global checks_made
    checks_made = checks_made + 1
    return value == "hello" or value == "bye"


@add_constraint(some_expensive_check, "must be the string hello or bye")
@cache_constraint_results(maxsize=10)
class SomeString(ConstrainedString):
    pass


def test_check_is_only_made_for_each_value():
    global checks_made
    checks_made = 0
    one = SomeString("hello")
    two = SomeString("bye")
    three = SomeString("hello")

    assert checks_made == 2


def test_check_can_still_fail():
    one = SomeString("hello")
    two = SomeString("bye")

    with pytest.raises(UnmetConstraintError):
        three = SomeString("woooooo!")
