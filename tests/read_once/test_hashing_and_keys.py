from wyrd.read_once import ReadOnce


def test_they_can_be_hashed_if_the_inner_type_can_be():
    a = ReadOnce("the same")
    b = ReadOnce("the same")

    assert hash(a) == hash(b)


def test_they_can_be_used_as_a_dict_key():
    lookup = {ReadOnce("a"): "success", ReadOnce("b"): "another"}

    assert lookup[ReadOnce("a")] == "success"
