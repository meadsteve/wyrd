import pytest

from wyrd.read_once import ReadOnce


def test_they_are_equal_if_the_contents_is():
    a = ReadOnce("the same")
    b = ReadOnce("the same")
    assert a == b


def test_they_are_not_equal_if_the_contents_isnt():
    a = ReadOnce("the same")
    b = ReadOnce("but different")
    assert a != b


def test_they_cant_be_compared_to_other_types():
    a = ReadOnce("the same")
    b = "the same"
    with pytest.raises(RuntimeError):
        a != b
