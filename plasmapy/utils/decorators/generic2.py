import inspect
import wrapt

from typing import Any, Callable, Dict, List, Optional


def _process_kwargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    return kwargs


def _bind_arguments():
    pass


def generic_decorator(
    wrapped: Callable = None, *args_to_decorator, **kwargs_to_decorator
):

    wrapped_signature = inspect.signature(wrapped)

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):

        annotations = inspect.get_annotations(wrapped)
        bound_args = wrapped_signature.bind(*args, **kwargs)
        default_arguments = bound_args.signature.parameters
        #        arguments = bound_args.arguments
        #        parameters = bound_args.signature.parameters.keys()  # formerly argnames

        return wrapped(*args, **kwargs)

    return wrapper(wrapped)
