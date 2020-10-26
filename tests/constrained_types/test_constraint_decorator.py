import pytest

from wyrd.constrained_types import add_constraint, ConstrainedInt


def test_fails_if_you_add_constraints_to_a_plain_class():
    class NormalClass:
        pass

    with pytest.raises(SyntaxError):
        add_constraint(lambda x: True, "always okay")(NormalClass)  # type: ignore


def test_fails_if_you_add_constraints_to_a_plain_class_even_if_it_has_constrains():
    class NormalClass:
        _constraints = []

    with pytest.raises(SyntaxError):
        add_constraint(lambda x: True, "always okay")(NormalClass)  # type: ignore


def test_decorated_class_keeps_its_name():
    @add_constraint(lambda x: True, "always okay")
    class NormalClass(ConstrainedInt):
        pass

    assert NormalClass.__name__ == "NormalClass"
