"""
Generic classes for decorators that process arguments based on
annotations.
"""

__all__ = ["GenericDecorator", "OriginalGenericDecorator"]

import collections
import functools
import inspect

from typing import AbstractSet, Any, Callable, Dict, Mapping, NoReturn, Optional, Tuple


class GenericDecorator:
    """
    A decorator that can be subclassed to perform operations on the
    positional arguments, keyword arguments, and return values based on
    annotations.

    Parameters
    ----------
    function_to_decorate : callable, positional-only
        The function being decorated.

    *args_to_decorator
        The positional arguments provided to the decorator.

    **kwargs_to_decorator
        The keyword arguments provided to the decorator.

    """

    def __init__(
        self,
        function_to_decorate: Optional[Callable] = None,
        /,
        *args_to_decorator,
        **kwargs_to_decorator,
    ):
        self.initialize()
        self.args_to_decorator = args_to_decorator
        self.kwargs_to_decorator = kwargs_to_decorator
        self.function_being_decorated = function_to_decorate
        print("Ending __init__")

    def initialize(self):
        print("Initializing GenericDecorator")
        self._data = {}

    @property
    def args_to_decorator(self) -> tuple:
        """The positional arguments provided to the decorator."""
        print(f"Accessing args_to_decorator: {args_to_decorator}")
        return self._data["args_to_decorator"]

    @args_to_decorator.setter
    def args_to_decorator(self, args: dict):
        print(f"Storing args_to_decorator: {args}")
        self._data["args_to_decorator"] = args

    @property
    def kwargs_to_decorator(self):
        """The keyword arguments provided to the decorator."""
        print(f"Accessing kwargs_to_decorator: {self._data['kwargs_to_decorator']}")
        return self._data["kwargs_to_decorator"]

    @kwargs_to_decorator.setter
    def kwargs_to_decorator(self, kwargs: Dict[str, Any]):
        print(f"Storing kwargs_to_decorator: {kwargs}")
        self._data["kwargs_to_decorator"] = kwargs

    @property
    def function_being_decorated(self) -> Optional[Callable]:
        """The function being decorated."""
        print(
            f"Accessing function_being_decorated: {self._data['function_being_decorated']}"
        )
        try:
            return self._data["function_being_decorated"]
        except KeyError:
            return None

    @function_being_decorated.setter
    def function_being_decorated(self, function_to_decorate):
        print(f"Setting function_being_decorated: {function_to_decorate}")
        if function_to_decorate is not None and not callable(function_to_decorate):
            raise TypeError("The function being decorated is not callable.")
        self._data["function_being_decorated"] = function_to_decorate

    def __call__(self, *args, **kwargs):
        """Run decorated function if available, else decorate first arg."""

        if self.function_being_decorated is not None:
            return self.run_decorated_function(*args, **kwargs)

        if args[1:] or kwargs:
            raise ValueError("Placeholder exception; not sure if this is needed.")

        self.function_being_decorated = args[0]
        return self

    def run_decorated_function(self, *args, **kwargs):
        """
        Run
        :meth:`~plasmapy.utils.decorators.generic.GenericDecorator.function_being_decorated`.

        Parameters
        ----------
        *args
            Positional arguments to be passed to the decorated function.

        **kwargs
            Keyword arguments to be passed to the decorated function
        """
        return self.function_being_decorated(*args, **kwargs)


class OriginalGenericDecorator:
    @classmethod
    def as_decorator(cls, func: Callable = None, **kwargs_to_decorator):
        print("calling as_decorator")
        try:
            self = cls(**kwargs_to_decorator)
        except KeyError:
            raise RuntimeError("Incorrect argument to decorator")  # add test for this
        return self if func is None or kwargs_to_decorator else self(func)

    def __init__(self, func=None, **kwargs_to_init):
        print("calling __init__")
        self._data = collections.defaultdict(lambda: None)
        self._data["new_kwargs"] = {}

    def __call__(self, wrapped_function: Callable):
        self._data["new_kwargs"] = {}
        self.wrapped_function = wrapped_function
        # TODO: give better name to assigned since I don't know what it means
        assigned = list(functools.WRAPPER_ASSIGNMENTS)
        assigned.append("__signature__")

        @functools.wraps(wrapped_function, assigned=assigned)
        def wrapper(*original_args_to_func, **original_kwargs_to_func):
            print("Inside wrapper")
            self.original_args_to_func = original_args_to_func
            self.original_kwargs_to_func = original_kwargs_to_func
            self.process_arguments()
            return wrapped_function(**self.new_kwargs)

        return wrapper

    @property
    def wrapped_function(self) -> Optional[Callable]:
        """The function that is being decorated."""
        return self._data["wrapped_function"]

    @wrapped_function.setter
    def wrapped_function(self, function: Callable):
        self._data["wrapped_function"] = function
        self._data["wrapped_signature"] = inspect.signature(function)
        self._data["annotations"] = getattr(function, "__annotations__", {}).copy()
        if "return" in self._data["annotations"]:
            del self._data["annotations"]["return"]

    @property
    def annotations(self) -> Optional[Mapping[str, Any]]:
        """
        Annotations for arguments in the decorated function.
        The keys are the arguments to the decorated function that have
        annotations.  The associated values are the annotations themselves.
        Only arguments with annotations are included.
        """
        return self._data["annotations"]

    @property
    def wrapped_signature(self) -> Optional[inspect.Signature]:
        return self._data["wrapped_signature"]

    @property
    def bound_args(self) -> Optional[inspect.BoundArguments]:
        bound_args_ = self.wrapped_signature.bind(
            *self.original_args_to_func, **self.original_kwargs_to_func
        )
        bound_args_.apply_defaults()
        return bound_args_

    @property
    def default_arguments(self) -> Mapping[str, inspect.Parameter]:
        return self.bound_args.signature.parameters

    @property
    def new_kwargs(self) -> Optional[Mapping[str, Any]]:
        """The revised keyword arguments to be supplied to the decorated function."""
        return self._data["new_kwargs"]

    @new_kwargs.setter
    def new_kwargs(self, kwargs: Mapping[str, Any]) -> NoReturn:
        if isinstance(kwargs, collections.abc.Mapping):
            self._data["new_kwargs"] = kwargs
        else:
            raise TypeError("new_kwargs must be a mapping such as a dictionary")

    @property
    def original_args_to_func(self) -> Optional[Tuple]:
        """Positional arguments as originally supplied to the decorated function."""
        return self._data["original_args_to_func"]

    @original_args_to_func.setter
    def original_args_to_func(self, value: Tuple):
        self._data["original_args_to_func"] = value

    @property
    def original_kwargs_to_func(self) -> Optional[Mapping[str, Any]]:
        """Keyword arguments as originally supplied to the decorated function."""
        return self._data["original_kwargs_to_func"]

    @original_kwargs_to_func.setter
    def original_kwargs_to_func(self, value: Mapping[str, Any]):
        self._data["original_kwargs_to_func"] = value

    @property
    def original_values(self) -> Mapping[str, Any]:
        """
        The values that were originally passed as positional and keyword
        arguments to the decorated function.
        """
        return self.bound_args.arguments

    @property
    def argument_names(self) -> AbstractSet:
        """The names of the arguments to the original function."""
        return self.bound_args.signature.parameters.keys()

    def process_arguments(self) -> NoReturn:
        self.new_kwargs = self.original_values
