import pickle

import pytest

from wyrd.read_once import ReadOnce
from wyrd.read_once.core import ReadTwiceError


def test_it_returns_the_value_stored():
    something = ReadOnce("hello - only once")
    assert something.get_contents() == "hello - only once"


def test_it_raise_an_exception_the_second_time_its_read():
    something = ReadOnce("hello - only once")
    _first = something.get_contents()
    with pytest.raises(ReadTwiceError):
        _second = something.get_contents()


def test_the_exception_message_does_not_contain_the_value():
    something = ReadOnce("secret")
    _first = something.get_contents()
    with pytest.raises(ReadTwiceError) as error:
        _second = something.get_contents()
    assert "secret" not in str(error.value)


def test_type_information_can_still_be_accessed():
    assert ReadOnce("hello - only once").type == str
    assert ReadOnce(5).type == int


def test_an_isinstance_equiv_is_provided():
    assert ReadOnce("hello - only once").isinstance(str)
    assert ReadOnce(5).isinstance(object)


def test_turning_it_into_a_string_turns_the_underlying_value_into_a_string():
    something = ReadOnce("the actual value")
    assert str(something) == "the actual value"


def test_turning_it_into_a_string_only_works_once():
    something = ReadOnce("the actual value")
    _first_usage = str(something)
    with pytest.raises(ReadTwiceError):
        _second_usage = str(something)


def test_it_can_be_used_in_f_strings():
    something = ReadOnce("Hello!")
    assert f"you said: {something}" == "you said: Hello!"


def test_the_repr_it_returns_indicates_the_type():
    something = ReadOnce("Hello!")
    assert repr(something) == "ReadOnce<str>"


def test_they_cannot_be_pickled():
    contents = ReadOnce("the actual value")
    with pytest.raises(RuntimeError):
        pickle.dumps(contents)
