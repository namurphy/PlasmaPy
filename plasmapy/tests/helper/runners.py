from typing import Callable, Union, Optional, Any, Dict, NoReturn
from numbers import Number

from astropy import units as u

from plasmapy.tests.helper.inputs import (
    AbstractTestInputs,
    FunctionTestInputs,
    ClassAttributeTestInputs,
    ClassMethodTestInputs,
)

from plasmapy.tests.helper.actual import ActualTestOutcome
from plasmapy.tests.helper.expected import ExpectedTestOutcome
from plasmapy.tests.helper.comparators import CompareActualExpected
from plasmapy.tests.helper.exceptions import InvalidTestError

from plasmapy.tests.helper.cases import (
    BaseTestCase,
    AttrTestCase,
    MethodTestCase,
    FunctionTestCase,
)

__all__ = ["function_test_runner", "method_test_runner", "attr_test_runner"]


def _get_test_inputs(case: BaseTestCase) -> AbstractTestInputs:
    """
    Select and instantiate the appropriate subclass of
    ~plasmapy.tests.helper.inputs.

    """

    if isinstance(case, FunctionTestCase):

        inputs = FunctionTestInputs(
            function=case.function, args=case.args, kwargs=case.kwargs
        )

    elif isinstance(MethodTestCase):

        inputs = ClassMethodTestInputs(
            cls=case.cls,
            method=case.method,
            cls_args=case.cls_args,
            cls_kwargs=case.cls_kwargs,
            method_args=case.method_args,
            method_kwargs=case.method_kwargs,
        )

    elif isinstance(AttrTestCase):

        inputs = ClassAttributeTestInputs(
            cls=case.cls,
            attribute=case.attribute,
            cls_args=case.cls_args,
            cls_kwargs=case.cls_kwargs,
        )

    else:

        raise TypeError(
            "A test case must be an instance of FunctionTestCase, "
            "MethodTestCase, or AttrTestCase."
        )

    return inputs


def test_runner(case: BaseTestCase) -> NoReturn:

    __tracebackhide__ = True

    try:
        test_inputs = _get_test_inputs(case)
        actual_outcome = ActualTestOutcome(test_inputs)
        expected_outcome = ExpectedTestOutcome(case.expected)
        comparison = CompareActualExpected(
            actual_outcome=actual_outcome,
            expected_outcome=expected_outcome,
            rtol=case.rtol,
            atol=case.atol,
        )
    except Exception as exc:

        raise InvalidTestError("Unable to run test.") from exc

    if not comparison.test_passed:
        raise comparison.exception(comparison.error_message)


def _test_runner(
    inputs: AbstractTestInputs,
    expected,
    *,
    rtol: Union[Number, u.Quantity] = 1e-8,
    atol: Optional[Union[Number, u.Quantity]] = None,
) -> NoReturn:
    """
    Perform the parts of the test that are common among the different
    test runners for the result test pattern.
    """

    __tracebackhide__ = True

    try:
        actual_outcome = ActualTestOutcome(inputs)
        expected_outcome = ExpectedTestOutcome(expected)
        comparison = CompareActualExpected(
            actual_outcome, expected_outcome, rtol=rtol, atol=atol
        )
    except Exception as exc:
        raise InvalidTestError("Unable to run test.") from exc

    if not comparison.test_passed:
        raise comparison.exception(comparison.error_message)


def function_test_runner(
    expected,
    function: Callable,
    args=None,
    kwargs: Optional[Dict[str, Any]] = None,
    *,
    rtol: Union[Number, u.Quantity] = 1e-8,
    atol: Optional[Union[Number, u.Quantity]] = None,
) -> NoReturn:
    """
    Test that calling a function with particular arguments results in
    the expected outcome.

    Parameters
    ----------
    expected
        The expected outcome of the test, which can be an exception,
        a warning, the resulting object, or a tuple that contains
        a warning and the resulting object.

    function
        The function to be tested.

    args : optional
        The positional arguments to be provided to the function that is
        being tested.  If this is a `tuple` or `list`, then the
        arguments will be each of the items in the collection. If there
        is only one positional argument, then it may be inputted as is
        without being put into a `tuple` or `list`.

    kwargs : `dict`, optional
        The keyword arguments to be provided to the function that is
        being tested. If provided, the keys of this `dict` must be
        strings.

    rtol : dimensionless number, optional, keyword-only
        The relative tolerance to be used in `astropy.units.allclose`.
        Defaults to ``1e-8``.  If ``rtol`` is a `~astropy.units.Quantity`
        instance, then it must be dimensionless.

    atol : number or `~astropy.units.Quantity`, optional, keyword-only
        The absolute tolerance to be supplied to `astropy.units.isclose`
        or `~astropy.units.allclose`.  If ``atol`` is a
        `~astropy.units.Quantity`, then it must have the same units as
        ``this`` and ``that``.  Defaults to zero in the appropriate units.

    Raises
    ------
    ~plasmapy.tests.helper.exceptions.InvalidTestError
        If the test is not set up correctly.

    ~plasmapy.tests.helper.exceptions.UnexpectedResultError
        If the value returned by the test does not match the expected value.

    ~plasmapy.tests.helper.exceptions.InconsistentTypeError
        If the type of the value returned by the test is not the same
        type as the expected value.

    ~plasmapy.tests.helper.exceptions.UnexpectedExceptionError
        If an exception was raised unexpectedly.

    ~plasmapy.tests.helper.exceptions.MissingExceptionError
        If an exception was expected to be raised, but was not.

    ~plasmapy.tests.helper.exceptions.ExceptionMismatchError
        If an exception was raised that was different from the expected exception.

    ~plasmapy.tests.helper.exceptions.UnexpectedWarningError
        If a warning was issued unexpectedly.

    ~plasmapy.tests.helper.exceptions.MissingWarningError
        If a warning was expected to be issued, but was not.

    ~plasmapy.tests.helper.exceptions.WarningMismatchError
        If the expected warning was not issued, but one or more different warnings were.

    ~plasmapy.tests.helper.exceptions.Failed
        If the test fails in a different way or more than one way.

    See Also
    --------
    method_test_runner
    attr_test_runner

    Examples
    --------
    This test runner checks that calling a function supplied with certain
    positional and keyword arguments results in the expected outcome. The
    expected outcome may be a value, a warning, an exception, or a
    combination of a warning and a value.

    Suppose we create a function that takes no arguments and returns ``42``.

    >>> return_42 = lambda: 42

    To test that this function is behaving properly, we run:

    >>> function_test_runner(expected=42, function=return_42)

    No exception is raised when running the test, which means that this
    test passes.

    Next we wish to test a function that adds the values of the positional
    argument and the expected argument.

    >>> def add_arg_and_kwarg(arg, kwarg=None):
    ...     return arg + kwarg

    Positional arguments are generally given as a `tuple` or `list`
    while keyword arguments are provided as a `dict`.  If there is only
    one positional argument, then it may be supplied as itself if it is
    not a `tuple` or `list`.

    >>> args = (5,)
    >>> kwargs = {"kwarg": 4}

    >>> function_test_runner(expected=9, function=add_arg_and_kwarg, args=args, kwargs=kwargs)

    We may use this function to test that the expected exception is raised.

    >>> def raise_syntax_error():
    ...     raise SyntaxError

    >>> function_test_runner(expected=SyntaxError, function=raise_syntax_error)

    Similarly, we may test that a function issues a particular warning.
    If ``expected`` is a `tuple` containing a warning and a value in
    either order, then ``function_test_runner`` will check that the
    warning is issued and that that value is returned.

    >>> import warnings
    >>> def issue_warning_and_return_6():
    ...     warnings.warn("...", UserWarning)
    ...     return 6

    >>> function_test_runner(expected=UserWarning, function=issue_warning_and_return_6)
    >>> function_test_runner(expected=(UserWarning, 6), function=issue_warning_and_return_6)

    This test runner works well in combination with `~pytest.mark.parametrize`.
    """

    __tracebackhide__ = True
    inputs = FunctionTestInputs(function, args, kwargs)
    _test_runner(inputs, expected, rtol=rtol, atol=atol)


def method_test_runner(
    expected,
    cls,
    method: str,
    *,
    cls_args=None,
    cls_kwargs: Optional[Dict[str, Any]] = None,
    method_args=None,
    method_kwargs: Optional[Dict[str, Any]] = None,
    rtol: Union[Number, u.Quantity] = 1e-8,
    atol: Optional[Union[Number, u.Quantity]] = None,
) -> NoReturn:
    """
    Test that calling a class method results in the expected outcome.

    Parameters
    ----------
    expected
        The expected outcome of the test, which can be an exception,
        a warning, the resulting object, or a tuple that contains
        a warning and the resulting object.

    cls
        The class containing the method to be tested.

    cls_args : optional
        The positional arguments to be provided to the class that is
        being tested during instantiation. If this is a `tuple` or
        `list`, then the arguments will be each of the items in the
        collection. If there is only one positional argument, then it
        may be inputted as is without being put into a `tuple` or `list`.

    cls_kwargs : `dict`, optional
        The keyword arguments to be provided to the class that is
        being tested during instantiation. If provided, the keys of
        this `dict` must be strings.

    method : str
        The name of the method contained in ``cls`` to be tested.

    method_args : optional
        The positional arguments to be provided to the method that is
        being tested.  If this is a `tuple` or `list`, then the
        arguments will be each of the items in the collection. If there
        is only one positional argument, then it may be inputted as is
        without being put into a `tuple` or `list`.

    method_kwargs : `dict`, optional
        The keyword arguments to be provided to the method that is being
        tested. If provided, the keys of this `dict` must be strings.

    rtol : dimensionless number, optional, keyword-only
        The relative tolerance to be used in `astropy.units.allclose`.
        Defaults to ``1e-8``.  If ``rtol`` is a `~astropy.units.Quantity`
        instance, then it must be dimensionless.

    atol : number or `~astropy.units.Quantity`, optional, keyword-only
        The absolute tolerance to be supplied to `astropy.units.isclose`
        or `~astropy.units.allclose`.  If ``atol`` is a
        `~astropy.units.Quantity`, then it must have the same units as
        ``this`` and ``that``.  Defaults to zero in the appropriate units.

    Raises
    ------
    ~plasmapy.tests.helper.exceptions.InvalidTestError
        If the test is not set up correctly.

    ~plasmapy.tests.helper.exceptions.UnexpectedResultError
        If the value returned by the test does not match the expected value.

    ~plasmapy.tests.helper.exceptions.InconsistentTypeError
        If the type of the value returned by the test is not the same
        type as the expected value.

    ~plasmapy.tests.helper.exceptions.UnexpectedExceptionError
        If an exception was raised unexpectedly.

    ~plasmapy.tests.helper.exceptions.MissingExceptionError
        If an exception was expected to be raised, but was not.

    ~plasmapy.tests.helper.exceptions.ExceptionMismatchError
        If an exception was raised that was different from the expected exception.

    ~plasmapy.tests.helper.exceptions.UnexpectedWarningError
        If a warning was issued unexpectedly.

    ~plasmapy.tests.helper.exceptions.MissingWarningError
        If a warning was expected to be issued, but was not.

    ~plasmapy.tests.helper.exceptions.WarningMismatchError
        If the expected warning was not issued, but one or more different warnings were.

    ~plasmapy.tests.helper.exceptions.Failed
        If the test fails in a different way or more than one way.

    See Also
    --------
    function_test_runner
    attr_test_runner

    Examples
    --------
    This test runner checks that calling a method attached to a class
    instance results in the expected outcome.  Positional and keyword
    arguments can be supplied to each of the class (to be used during
    instantiation) and to the method itself.

    >>> class SimpleClass:
    ...     def method(self):
    ...         return 42

    >>> method_test_runner(expected=42, cls=SimpleClass, method="method")

    No exception is raised when running the test, which means that this
    test passes.

    The ``cls_args`` and ``cls_kwargs`` arguments, if given, are passed
    to the class during instantiation.

    >>> class SomeClass:
    ...     def __init__(self, cls_arg, cls_kwarg=None):
    ...         self.cls_arg = cls_args
    ...         self.cls_kwarg = cls_kwarg
    ...     def f(self, method_arg, method_kwarg=None):
    ...         return self.cls_arg + 2 * self.cls_kwarg + 3 * method_arg + 4 * method_kwarg

    >>> cls_args = 4  # This should be a tuple for more than one argument
    >>> cls_kwargs = {"cls_kwarg": 1}
    >>> method_args = 3
    >>> method_kwargs = {"method_kwarg": 2}

    >>> method_test_runner(
    ...     23,
    ...     SomeClass,
    ...     "f",
    ...     cls_args=cls_args,
    ...     cls_kwargs=cls_kwargs,
    ...     method_args=method_args,
    ...     method_kwargs=method_kwargs,
    ... )

    This test runner works well in combination with `~pytest.mark.parametrize`.
    """

    __tracebackhide__ = True
    inputs = ClassMethodTestInputs(
        cls, method, cls_args, cls_kwargs, method_args, method_kwargs
    )
    _test_runner(inputs, expected, rtol=rtol, atol=atol)


def attr_test_runner(
    expected,
    cls,
    attribute: str,
    cls_args=None,
    cls_kwargs: Optional[Dict[str, Any]] = None,
    *,
    rtol: Union[Number, u.Quantity] = 1e-8,
    atol: Optional[Union[Number, u.Quantity]] = None,
) -> NoReturn:
    """
    Test that accessing a class attribute results in the expected outcome.

    Parameters
    ----------
    expected
        The expected outcome of the test, which can be an exception,
        a warning, the resulting object, or a tuple that contains
        a warning and the resulting object.

    cls
        The class containing the method to be tested.

    attribute : str
        The name of the attribute contained in ``cls`` to be tested.

    cls_args : optional
        The positional arguments to be provided to the class that is
        being tested during instantiation. If this is a `tuple` or
        `list`, then the arguments will be each of the items in the
        collection. If there is only one positional argument, then it
        may be inputted as is without being put into a `tuple` or `list`.

    cls_kwargs : `dict`, optional
        The keyword arguments to be provided to the class that is
        being tested during instantiation. If provided, the keys of
        this `dict` must be strings.

    rtol : dimensionless number, optional, keyword-only
        The relative tolerance to be used in `astropy.units.allclose`.
        Defaults to ``1e-8``.  If ``rtol`` is a `~astropy.units.Quantity`
        instance, then it must be dimensionless.

    atol : number or `~astropy.units.Quantity`, optional, keyword-only
        The absolute tolerance to be supplied to `astropy.units.isclose`
        or `~astropy.units.allclose`.  If ``atol`` is a
        `~astropy.units.Quantity`, then it must have the same units as
        ``this`` and ``that``.  Defaults to zero in the appropriate units.

    Raises
    ------
    ~plasmapy.tests.helper.exceptions.InvalidTestError
        If the test is not set up correctly.

    ~plasmapy.tests.helper.exceptions.UnexpectedResultError
        If the value returned by the test does not match the expected value.

    ~plasmapy.tests.helper.exceptions.InconsistentTypeError
        If the type of the value returned by the test is not the same
        type as the expected value.

    ~plasmapy.tests.helper.exceptions.UnexpectedExceptionError
        If an exception was raised unexpectedly.

    ~plasmapy.tests.helper.exceptions.MissingExceptionError
        If an exception was expected to be raised, but was not.

    ~plasmapy.tests.helper.exceptions.ExceptionMismatchError
        If an exception was raised that was different from the expected exception.

    ~plasmapy.tests.helper.exceptions.UnexpectedWarningError
        If a warning was issued unexpectedly.

    ~plasmapy.tests.helper.exceptions.MissingWarningError
        If a warning was expected to be issued, but was not.

    ~plasmapy.tests.helper.exceptions.WarningMismatchError
        If the expected warning was not issued, but one or more different warnings were.

    ~plasmapy.tests.helper.exceptions.Failed
        If the test fails in a different way or more than one way.

    See Also
    --------
    function_test_runner
    method_test_runner

    Examples
    --------
    This test runner checks that accessing an attribute attached to a
    class instance results in the expected outcome.  Positional and
    keyword arguments can be supplied to the class to be used upon
    instantiation.

    >>> class SimpleClass:
    ...     @property
    ...     def attr(self):
    ...         return 42
    >>> attr_test_runner(expected=42, cls=SimpleClass, attribute="attr")

    No exception is raised when running the test, which means that this
    test passes.

    The ``cls_args`` and ``cls_kwargs`` arguments, if given, are passed
    to the class during instantiation.

    >>> class SomeClass:
    ...     def __init__(self, cls_arg, cls_kwarg=None):
    ...         self.cls_arg = cls_args
    ...         self.cls_kwarg = cls_kwarg
    ...     @property
    ...     def attr(self):
    ...         return self.cls_arg + 2 * self.cls_kwarg
    >>> cls_args = 2
    >>> cls_kwargs = {"cls_kwarg": 3}
    >>> attr_test_runner(8, SomeClass, "attr", cls_args, cls_kwargs)

    This test runner works well in combination with `~pytest.mark.parametrize`.
    """

    __tracebackhide__ = True
    inputs = ClassAttributeTestInputs(cls, attribute, cls_args, cls_kwargs)
    _test_runner(inputs, expected, rtol=rtol, atol=atol)
