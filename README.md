# Constrained Types

Statement: Nothing should ever really be modelled as any String or any integer.


## Example
A user wants to order a number of books. Can it be zero? Can it be negative?
```python
@add_constraint(lambda x: x > 0, "Order must be at least 1")
class OrderQuantity(ConstrainedInt):
    pass
```

now:
```python
quantity = OrderQuantity(5)

# works exactly like an int
total_price = quantity * 5

# but you can't create sneaky discount books
quantity = OrderQuantity(-1)
# !! raises ValueError
```

## Integrates with pydantic
```python
@add_constraint(lambda x: x > 0, "Order must be at least 1")
class OrderQuantity(ConstrainedInt):
    pass


@add_constraint(lambda x: len(x) == 4, "Invalid order id")
class BookId(ConstrainedString):
    pass


class Order(BaseModel):
    book_quantity: OrderQuantity
    book_id: BookId
```

