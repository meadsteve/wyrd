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

## Multiple constraints
```python
@add_constraint(lambda x: x > 0, "Order must be at least 1")
@add_constraint(lambda x: x < 200, "Our shipping system can't send more then 200")
class OrderQuantity(ConstrainedInt):
    pass
```

In addition the constraints are guaranteed to execute in order so any
expensive checks to run can be listed further down.

## Cache results
If you expect the same value multiple times you can add caching for
the validation. The actual caching is passed to `functools.lru_cache`.

```python
@add_constraint(lambda x: len(x) > 0, "The order id must be set")
@add_constraint(lambda x: len(x) < 10, "Order ids are under 10 chars")
@add_constraint(some_really_complicated_checksum, "The order number was invalid")
@cache_constraint_results(maxsize=100)
class OrderId(ConstrainedString):
    pass
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

