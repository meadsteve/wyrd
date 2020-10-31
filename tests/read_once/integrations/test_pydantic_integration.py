import pytest
from pydantic import ValidationError
from pydantic.main import BaseModel

from constrained_types import ConstrainedString, add_constraint
from read_once import ReadOnce


class LoginData(BaseModel):
    username: str
    password: ReadOnce[str]


@add_constraint(lambda s: len(s) != 0, "password can't be empty")
class RawPassword(ConstrainedString):
    pass


class BetterLoginData(BaseModel):
    username: str
    password: ReadOnce[RawPassword]


def test_works_with_well_formed_pydantic_models():
    login_request = LoginData(username="elma", password="hunter1")
    assert login_request.password.get_contents() == "hunter1"


def test_works_with_well_formed_pydantic_models_with_constrained_types():
    login_request = BetterLoginData(username="elma", password="hunter1")
    assert login_request.password.get_contents() == "hunter1"


def test_passes_on_to_normal_pydantic_validation():
    with pytest.raises(ValidationError):
        LoginData(username="elma", password=None)


def test_passes_on_to_normal_pydantic_validation_with_constrained_types():
    with pytest.raises(ValidationError):
        BetterLoginData(username="elma", password="")


def test_badly_formed_models_raise_a_sensible_error():
    class BadLoginData(BaseModel):
        username: str
        password: ReadOnce
    with pytest.raises(SyntaxError):
        BadLoginData(username="elma", password="hunter1")


def test_schemas_can_still_be_generated():
    schema = LoginData.schema_json()
