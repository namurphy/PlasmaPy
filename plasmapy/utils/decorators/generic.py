import wrapt

from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# try:
#    # Python ≥ 3.10
#    from inspect import get_annotations
# except ImportError:
#    # Python ∈ {3.8, 3.9}
def get_annotations(f: Callable):
    return getattr(f, "__annotations__", None)


class GenericDecorator:
    """
    A class-based decorator that may be used for validating and/or
    processing the positional and keyword arguments provided to the
    decorated function.

    Notes
    -----
    This method may make use of attributes such as
    `~plasmapy.utils.decorators.GenericDecorator.function_being_decorated`,
    `~plasmapy.utils.decorators.GenericDecorator.annotations`,
    `~plasmapy.utils.decorators.GenericDecorator.args_to_decorator`,
    and
    `~plasmapy.utils.decorators.GenericDecorator.kwargs_to_decorator`.
    """

    verbose = False

    def process_arguments(
        self,
        args_to_function: Optional[Tuple] = None,
        kwargs_to_function: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Union[Tuple, List], Dict[str, Any]]:
        """
        Process the arguments provided to the decorated function.

        Returns
        -------
        `tuple`, `dict`
        """
        return args_to_function, kwargs_to_function

    def process_result(self, result: Any) -> Any:
        """
        Process the result from calling the decorated function with the
        processed arguments.
        """
        return result

    def __init__(
        self,
        function_being_decorated: Optional[Callable] = None,
        *args_to_decorator,
        **kwargs_to_decorator,
    ):

        self._data = {}

        self.function_being_decorated = function_being_decorated
        self.args_to_decorator = args_to_decorator
        self.kwargs_to_decorator = kwargs_to_decorator

    def __call__(
        self,
        *original_args_to_function,
        **original_kwargs_to_function,
    ):

        if self.verbose:
            print(f"__call__: {original_args_to_function=}")
            print(f"__call__: {original_kwargs_to_function=}")
            print(f"__call__: {self.function_being_decorated=}")
            print(f"__call__: {self.annotations=}")
            print(f"__call__: {self.args_to_decorator=}")
            print(f"__call__: {self.kwargs_to_decorator=}")

        if self.function_being_decorated is None:
            return self.__class__(original_args_to_function[0])

        # @wrapt.decorator
        # def wrapper(wrapped, instance, args, kwargs):
        #    if self.verbose:
        #        print(f"{wrapped=}\n{instance=}\n{args=}\n{kwargs=}")
        #    return wrapped(*args, **kwargs)

        # def wrapped(*args, **kwargs):
        #    return self.function_being_decorated(*args, **kwargs)

        @wrapt.decorator
        def wrapper(wrapped, instance, args, kwargs):
            result = wrapped(*args, **kwargs)
            print(result)
            return self.process_result(result)

        new_args, new_kwargs = self.process_arguments(
            args_to_function=original_args_to_function,
            kwargs_to_function=original_kwargs_to_function,
        )

        if self.verbose:
            print(f"__call__: {new_args=}")
            print(f"__call__: {new_kwargs=}")

        # result = wrapped(*new_args, **new_kwargs)

        # if self.verbose:
        # print(f"__call__: {result=}")

        return wrapper(*new_args, **new_kwargs)

    #        return self.process_result(result)

    @property
    def function_being_decorated(self) -> Optional[Callable]:
        """
        The function that is being decorated.

        Returns
        -------
        function
        """
        return self._data["function_being_decorated"]

    @function_being_decorated.setter
    def function_being_decorated(self, function: Optional[Callable]):
        self._data["function_being_decorated"] = function
        self._data["annotations"] = (
            get_annotations(function) if function is not None else {}
        )

    @property
    def annotations(self) -> Dict[str, Any]:
        """
        The annotations of the decorated function.

        Returns
        -------
        dict
        """
        return self._data["annotations"]

    @property
    def return_annotation(self) -> Any:
        """
        The return annotation of the decorated function, or `None` if
        the decorated function does not have a return annotation.

        Returns
        -------
        object
        """
        return getattr(self.annotations, "return", None)

    @property
    def args_to_decorator(self) -> Tuple:
        """
        Positional arguments provided to the decorator.

        Returns
        -------
        tuple
        """
        return self._data.get("args_to_decorator", ())

    @args_to_decorator.setter
    def args_to_decorator(self, args: tuple):
        if args is None:
            args = ()
        self._data["args_to_decorator"] = args

    @property
    def kwargs_to_decorator(self) -> Dict[str, Any]:
        """
        Keyword arguments provided to the decorator.

        Returns
        -------
        dict
        """
        return self._data.get("kwargs_to_decorator", {})

    @kwargs_to_decorator.setter
    def kwargs_to_decorator(self, kwargs: Dict[str, Any]):
        if kwargs is None:
            kwargs = {}
        self._data["kwargs_to_decorator"] = kwargs


class GenericDecorator2:
    """Base class to easily create convenient decorators.

    Override :py:meth:`setup`, :py:meth:`run` or :py:meth:`decorate` to create
    custom decorators:

    * :py:meth:`setup` is dedicated to setup, i.e. setting decorator's internal
      options.
      :py:meth:`__init__` calls :py:meth:`setup`.

    * :py:meth:`decorate` is dedicated to wrapping function, i.e. remember the
      function to decorate.
      :py:meth:`__init__` and :py:meth:`__call__` may call :py:meth:`decorate`,
      depending on the usage.

    * :py:meth:`run` is dedicated to execution, i.e. running the decorated
      function.
      :py:meth:`__call__` calls :py:meth:`run` if a function has already been
      decorated.

    Decorator instances are callables. The :py:meth:`__call__` method has a
    special implementation in Decorator. Generally, consider overriding
    :py:meth:`run` instead of :py:meth:`__call__`.

    """

    def __init__(
        self,
        function_being_decorated=None,
        *args_to_decorator,
        **kwargs_to_decorator,
    ):
        """Constructor.

        Accepts one optional positional argument: the function to decorate.

        Other arguments **must** be keyword arguments.

        And beware passing ``func`` as keyword argument: it would be used as
        the function to decorate.

        """

        self.args_to_decorator = args_to_decorator
        self.kwargs_to_decorator = kwargs_to_decorator

        self.setup(*args_to_decorator, **kwargs_to_decorator)

        self.function_being_decorated = None
        if function_being_decorated is not None:
            self.decorate(function_being_decorated)

    def decorate(self, func):
        """Remember the function to decorate.

        Raises TypeError if ``func`` is not a callable.

        """
        if not callable(func):
            raise TypeError(
                'Cannot decorate non callable object "{func}"'.format(func=func)
            )
        self.function_being_decorated = func
        return self

    def setup(self, *args, **kwargs):
        """Store decorator's options"""
        self.options = kwargs
        return self

    def __call__(self, *args, **kwargs):
        """Run decorated function if available, else decorate first arg."""
        if self.function_being_decorated is None:
            func = args[0]
            if args[1:] or kwargs:
                raise ValueError(
                    "Cannot decorate and setup simultaneously "
                    "with __call__(). Use __init__() or "
                    "setup() for setup. Use __call__() or "
                    "decorate() to decorate."
                )
            self.decorate(func)
            return self
        else:
            return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        """Actually run the decorator.

        This base implementation is a transparent proxy to the decorated
        function: it passes positional and keyword arguments as is, and returns
        result.

        """
        return self.function_being_decorated(*args, **kwargs)
