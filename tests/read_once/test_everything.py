import pytest

from wyrd.read_once import ReadOnce


def test_it_returns_the_value_stored():
    something = ReadOnce("hello - only once")
    assert something.get_contents() == "hello - only once"


def test_it_raise_an_exception_the_second_time_its_read():
    something = ReadOnce("hello - only once")
    _first = something.get_contents()
    with pytest.raises(RuntimeError):
        _second = something.get_contents()


def test_type_information_can_still_be_accessed():
    assert ReadOnce("hello - only once").type == str
    assert ReadOnce(5).type == int


def test_an_isinstance_equiv_is_provided():
    assert ReadOnce("hello - only once").isinstance(str)
    assert ReadOnce(5).isinstance(object)
