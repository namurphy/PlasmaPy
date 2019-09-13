import collections
import pytest
from plasmapy.utils.pytest_helpers.expected import (
    ExpectedOutcome,
    _is_warning,
    _is_exception,
    _is_warning_and_value,
)


@pytest.mark.parametrize(
    "argument, expected",
    [
        (Warning, True)  ,
        (UserWarning, True),
        (Exception, False),
        ('', False),
    ]
)
def test__is_warning(argument, expected):
    """
    Test that `~plasmapy.utils.pytest_helpers.expected._is_warning`
    returns `True` for warnings and `False` for other objects.
    """
    assert _is_warning(argument) is expected


@pytest.mark.parametrize(
    "argument, expected",
    [
        (Warning, False)  ,
        (UserWarning, False),
        (Exception, True),
        ('', False),
    ]
)
def test__is_exception(argument, expected):
    """
    Test that `~plasmapy.utils.pytest_helpers.expected._is_exception`
    returns `True` for exceptions and `False` for other objects.
    """
    assert _is_exception(argument) is expected


@pytest.mark.parametrize(
    "argument, expected",
    [
        ((Warning, ''), True),
        (['', UserWarning], True),
        ((Warning, UserWarning), False),
        (Warning, False)  ,
        (UserWarning, False),
        (Exception, False),
        ('', False),
    ]
)
def test__is_warning_and_value(argument, expected):
    """
    Test that `~plasmapy.utils.pytest_helpers.expected._is_warning_and_value`
    returns `True` for a `tuple` or `list` containing a warning and an
    object that is not a warning, and `False` for other objects.
    """
    assert _is_warning_and_value(argument) is expected


expected_exception = KeyError
expected_warning = UserWarning
expected_value = 42

Case = collections.namedtuple('Case', ['argument', 'attribute', 'correct_outcome'])

cases = [
    Case(expected_exception, 'exception', expected_exception),
    Case(expected_exception, 'warning', None),
    Case(expected_exception, 'value', None),
    Case(expected_exception, 'expected', expected_exception),
    Case(expected_exception, 'expecting_exception', True),
    Case(expected_exception, 'expecting_warning', False),
    Case(expected_exception, 'expecting_value', False),
    Case(expected_warning, 'exception', None),
    Case(expected_warning, 'warning', expected_warning),
    Case(expected_warning, 'value', None),
    Case(expected_warning, 'expected', expected_warning),
    Case(expected_warning, 'expecting_exception', False),
    Case(expected_warning, 'expecting_warning', True),
    Case(expected_warning, 'expecting_value', False),
    Case(expected_value, 'exception', None),
    Case(expected_value, 'warning', None),
    Case(expected_value, 'value', expected_value),
    Case(expected_value, 'expected', expected_value),
    Case(expected_value, 'expecting_exception', False),
    Case(expected_value, 'expecting_warning', False),
    Case(expected_value, 'expecting_value', True),
    Case((expected_value, expected_warning), 'exception', None),
    Case((expected_value, expected_warning), 'warning', expected_warning),
    Case((expected_value, expected_warning), 'value', expected_value),
    Case((expected_value, expected_warning), 'expecting_exception', False),
    Case((expected_value, expected_warning), 'expecting_warning', True),
    Case((expected_value, expected_warning), 'expecting_value', True),
    Case((expected_value, expected_warning), 'expected', (expected_warning, expected_value)),
    Case((expected_warning, expected_value), 'exception', None),
    Case((expected_warning, expected_value), 'warning', expected_warning),
    Case((expected_warning, expected_value), 'value', expected_value),
    Case((expected_warning, expected_value), 'expecting_exception', False),
    Case((expected_warning, expected_value), 'expecting_warning', True),
    Case((expected_warning, expected_value), 'expecting_value', True),
    Case((expected_warning, expected_value), 'expected', (expected_warning, expected_value)),
]


@pytest.mark.parametrize("case", cases)
def test_expected_outcome(case):
    try:
        expected_outcome = ExpectedOutcome(case.argument)
    except Exception:
        pytest.fail(f'Unable to instantiate ExpectedOutcome for {case.argument}')
    else:
        result = eval(f'expected_outcome.{case.attribute}')

    if result is not case.correct_outcome and result != case.correct_outcome:
        pytest.fail(
            f"ExpectedOutcome({case.argument}) results in {repr(result)} "
            f"but should result in {case.correct_outcome}."
        )
