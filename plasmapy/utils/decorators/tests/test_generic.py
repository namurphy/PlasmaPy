"""Tests of generic decorator functionality."""

import pytest

from plasmapy.utils.decorators.generic import GenericDecorator


@GenericDecorator
def decorated_function_without_decorator_call(x, *, y, z=5):
    return x, y, z


@GenericDecorator()
def decorated_function_with_decorator_call(x, *, y, z=5):
    return x, y, z


@pytest.mark.parametrize(
    "decorated_function",
    [
        decorated_function_with_decorator_call,
        decorated_function_without_decorator_call,
    ],
)
def test_decorated_function(decorated_function):
    assert decorated_function(2, y=3) == (2, 3, 5)


@GenericDecorator
class DecoratedClassWithoutDecoratorCall:
    def __init__(self):
        self.x = 1


@GenericDecorator()
class DecoratedClassWithDecoratorCall:
    def __init__(self):
        self.x = 1


@pytest.mark.parametrize(
    "DecoratedClass",
    [
        DecoratedClassWithoutDecoratorCall,
        DecoratedClassWithoutDecoratorCall,
    ],
)
def test_decoration_of_classes(DecoratedClass):
    instance = DecoratedClass()
    assert instance.x == 1


def test_exception():
    with pytest.raises(TypeError):
        GenericDecorator(1)
