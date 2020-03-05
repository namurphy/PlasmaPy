"""..."""

from typing import Any, Optional, Dict, Callable
from numbers import Real

__all__ = ["BaseTestCase", "FunctionTestCase", "MethodTestCase", "AttrTestCase"]


class BaseTestCase:

    pass


class FunctionTestCase(BaseTestCase):
    """..."""

    def __init__(
        self,
        expected: Any,
        function: Callable,
        args=(),
        kwargs: Optional[Dict[str, Any]] = None,
        purpose: Optional[str] = None,
        *,
        rtol: Real = 1e-8,
        atol=None,
    ):

        self.expected = expected
        self.function = function
        self.args = args
        self.kwargs = {} if kwargs is None else kwargs
        self.purpose = purpose
        self.atol = atol
        self.rtol = rtol


class MethodTestCase(BaseTestCase):
    """..."""

    def __init__(
        self,
        expected: Any,
        cls,
        method: str,
        *,
        cls_args=(),
        cls_kwargs: Optional[Dict[str, Any]],
        method_args=(),
        method_kwargs: Optional[Dict[str, Any]],
        atol=None,
        rtol=1e-8,
        purpose: Optional[str] = None,
    ):

        self.expected = expected
        self.cls = cls
        self.method = method
        self.cls_args = cls_args
        self.cls_kwargs = {} if cls_kwargs is None else cls_kwargs
        self.method_args = method_args
        self.method_kwargs = method_kwargs
        self.purpose = str(purpose)
        self.atol = atol
        self.rtol = rtol


class AttrTestCase(BaseTestCase):
    """..."""

    def __init__(
        self,
        expected: Any,
        cls,
        attribute: str,
        *,
        cls_args=(),
        cls_kwargs: Optional[Dict[str, Any]] = None,
        purpose: Optional[str] = None,
        atol=None,
        rtol=1e-8,
    ):

        self.expected = expected
        self.cls = cls
        self.attribute = attribute
        self.cls_args = cls_args
        self.cls_kwargs = {} if cls_kwargs is None else cls_kwargs
        self.purpose = purpose
        self.atol = atol
        self.rtol = rtol
