import pytest
from pydantic import BaseModel

from constrained_types import add_constraint, ConstrainedString, ConstrainedInt


@add_constraint(lambda x: x > 0, "Order must be at least 1")
class OrderQuantity(ConstrainedInt):
    pass


@add_constraint(lambda x: len(x) == 4, "Invalid order id")
class BookId(ConstrainedString):
    pass


class Order(BaseModel):
    book_quantity: OrderQuantity
    book_id: BookId


def test_pydantic_passes_on_validation_failure_as_expected():
    with pytest.raises(Exception):
        _discount_trick = Order(book_quantity=-1, book_id="ab12")
