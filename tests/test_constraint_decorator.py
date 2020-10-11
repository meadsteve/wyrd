import pytest

from constrained_types import add_constraint


def test_fails_if_you_add_constraints_to_a_plain_class():
    class NormalClass:
        pass

    with pytest.raises(SyntaxError):
        add_constraint(lambda x: True, "always okay")(NormalClass)


def test_fails_if_you_add_constraints_to_a_plain_class_even_if_it_has_constrains():
    class NormalClass:
        _constraints = []

    with pytest.raises(SyntaxError):
        add_constraint(lambda x: True, "always okay")(NormalClass)
