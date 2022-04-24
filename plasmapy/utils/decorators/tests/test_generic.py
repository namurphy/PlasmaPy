import pytest

from typing import Any, Dict, List, Optional, Tuple, Union

from plasmapy.utils.decorators.generic import GenericDecorator
from plasmapy.utils.decorators.generic2 import generic_decorator


@pytest.mark.parametrize("decorator", [generic_decorator, generic_decorator()])
def test_generic_decorator(decorator):
    @generic_decorator
    def return_arg(x):
        return x

    assert return_arg(1) == 1


@pytest.mark.parametrize("decorator", [generic_decorator, generic_decorator()])
@pytest.mark.parametrize("argument", [(), (1,)])
def test_using_generic_decorator_with_and_without_call(decorator, argument):
    @decorator
    def return_argument(argument=None):
        return argument

    assert return_argument(argument) == argument


def return_none():
    return None


@pytest.mark.skip
@pytest.mark.parametrize("args", [(), (1, 2)])
@pytest.mark.parametrize("kwargs", [{}, {"x": 1, "y": 2}])
def test_creating_a_generic_decorator_instance(args, kwargs):
    instance = GenericDecorator(return_none, *args, **kwargs)
    assert instance.args_to_decorator == args
    assert instance.kwargs_to_decorator == kwargs


@pytest.mark.skipif
@pytest.mark.parametrize("decorator", [GenericDecorator, GenericDecorator()])
@pytest.mark.parametrize("argument", [(), (1,)])
def test_using_generic_decorator_with_and_without_call(decorator, argument):
    @decorator
    def return_argument(argument=None):
        return argument

    assert return_argument(argument) == argument


@pytest.mark.skip
@pytest.mark.parametrize("decorator", [GenericDecorator, GenericDecorator()])
def test_class_being_decorated(decorator):
    @decorator
    class DecoratedClass:
        def __init__(self, x, y=3):
            self.x = x
            self.y = y

    instance = DecoratedClass(1)
    assert instance.x == 1
    assert instance.y == 3


@pytest.mark.skip
@pytest.mark.parametrize("decorator", [GenericDecorator, GenericDecorator()])
def test_method_being_decorated(decorator):
    class DecoratedClass:
        def __init__(self):
            pass

        @decorator
        def add(self, x, y):
            return x + y

    instance = DecoratedClass()
    assert instance.add(1, 2) == 3


# def test_process_args():

#    print(f"\n{72*'*'}")
#    print("Running test_process_args")
#    print(72*"*"+'\n')

#    class ReturnArgsAndKwargsToDecorator(GenericDecorator):

#        def process_arguments(
#            self,
#            args_to_function: Optional[Tuple] = None,
#            kwargs_to_function: Optional[Dict[str, Any]] = None,
#        ) -> Tuple[Union[Tuple, List], Dict[str, Any]]:
#
#            print(f"process_arguments: {self.args_to_decorator=}")
#            print(f"process_arguments: {self.kwargs_to_decorator=}")

#            return self.args_to_decorator, self.kwargs_to_decorator

#    args_to_decorator = (1, 2)
#    kwargs_to_decorator = {"x": 3, "y": 4}

#    @ReturnArgsAndKwargsToDecorator(*args_to_decorator, **kwargs_to_decorator)
#    def function(x, y):
#        return x, y

#    returned_args, returned_kwargs = function(1, 2)

#    assert returned_args == args_to_decorator
