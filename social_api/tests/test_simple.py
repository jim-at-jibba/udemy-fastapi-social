# test one thing
def test_add_two():
    x = 1
    y = 2
    assert x + y == 3


def test_dict_contains():
    x = {"a": 1, "b": 2}

    expected = {"a": 1}
    # .items gives you a view into the dictionary
    # This gives us a view in to the dictionary and makes sure
    # the x is in expected
    assert expected.items() <= x.items()
