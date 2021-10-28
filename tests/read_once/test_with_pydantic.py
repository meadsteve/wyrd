import pytest
from pydantic import BaseModel

from wyrd.read_once import ReadOnce
from wyrd.read_once.core import ReadTwiceError


class SomeData(BaseModel):
    secret: ReadOnce[str]


def test_values_can_be_set_and_read():
    something = SomeData(secret="cinnamon")
    assert something.secret.get_contents() == "cinnamon"


def test_values_can_be_set_and_a_second_read_fails():
    something = SomeData(secret="cinnamon")
    _first = something.secret.get_contents()
    with pytest.raises(ReadTwiceError):
        something.secret.get_contents()


def test_pydantic_validation_occurs_on_the_inner_type():
    with pytest.raises(RuntimeError):
        SomeData(secret=object())


def test_pydantic_type_coecerian_happens():
    something = SomeData(secret=6)
    assert something.secret.get_contents() == "6"
