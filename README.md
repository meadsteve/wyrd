# Wyrd - Helpers for Domain driven security


## Constrained Types

Statement: Nothing should ever really be modelled as any String or any integer.


#### Example
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

### Multiple constraints
```python
@add_constraint(lambda x: x > 0, "Order must be at least 1")
@add_constraint(lambda x: x < 200, "Our shipping system can't send more then 200")
class OrderQuantity(ConstrainedInt):
    pass
```

In addition the constraints are guaranteed to execute in order so any
expensive checks to run can be listed further down.

### Cache results
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

### Works well with mypy (or other static type checkers)
```python
# The following will type check fine. OrderId is a real type
def retrieve_order(order_id: OrderId):
    ...
```
maybe something further down only accepts strings:

```python
def _fetch_item_from_db(table_name: str, item_id: str):
    ...

def retrieve_order(order_id: OrderId):
    # The following will type check fine. OrderId extends str
    return _fetch_item_from_db("orders", order_id)
```



### Integrates with pydantic
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

#### Why not use the pydantic version of these constrained types?
The pydantic types only really work with pydantic. Invalid instances
can be created by constructing directly. Since constraint checking
is triggered by the constructor the constraints will *always* be
true for any instance of the class.
