import nested_validator

def test_nested_location():
    nested_location = nested_validator.NestedLocation()
    assert '' == str(nested_location)
    nested_location.push('a')
    nested_location.push(1)
    assert 'a.1' == str(nested_location)
    assert 1 == nested_location.pop()
    assert 'a' == str(nested_location)

def test_nested_validator():
    validator = nested_validator.NestedValidator()
    assert '' == validator({}, dict)
    assert 'Missing key "x"' == validator({}, dict(x=1))
    assert "Not a <class 'dict'>: []" == validator([], {})
    assert '' == validator([1, 2], [int])
    assert "1: Not a <class 'int'>: a" == validator([1, 'a'], [int])
    assert '' == validator(dict(a=1), (int, str, {'a': object}))
    result = validator(
            dict(a=1),
            (int, str, {'a': str}))
    assert result.endswith("a: Not a <class 'str'>: 1")
    assert "Not a <class 'str'>: 1\nNot a <class 'list'>: 1" == validator(
            1,
            (str, [int]))
