import pytest
import warnings
from collections import namedtuple

from plasmapy.utils.pytest_helpers import ActualOutcome


def return_douglas_adams_number():
    """A sample function with no positional or keyword arguments."""
    return 42


def add(a, *, b=2):
    """A sample function that has an argument and a keyword argument."""


def return_argument_and_issue_warning(arg, warning_message, *, kwarg=UnicodeWarning):
    """A sample function that has positional and keyword arguments and issues a warning."""
    warnings.warn(warning_message, kwarg)
    return arg


def raise_exception(error_message: str):
    """A sample function that raises a `RuntimeError`."""
    raise RuntimeError(error_message)


def issue_two_warnings_and_return_value(arg_warning, *, kwarg_warning=BytesWarning):
    """A sample function that issues multiple warnings and returns 22."""
    warnings.warn('α', arg_warning)
    warnings.warn('β', kwarg_warning)
    return 22


Case = namedtuple('Case', ['func', 'args', 'kwargs', 'attribute', 'correct_outcome'])


cases = [
    Case(return_douglas_adams_number, (), {}, 'value', 42),
    Case(return_douglas_adams_number, (), {}, 'exception', None),
    Case(return_douglas_adams_number, (), {}, 'warnings', None),
]


@pytest.mark.parametrize('case', cases)
def test_actual_outcome(case):
    try:
        actual_outcome = ActualOutcome(case.func, case.args, case.kwargs)
    except Exception:
        pytest.fail(
            f'Unable to instantiate ActualOutcome for {case.func} with '
            f'args = {case.args} and kwargs = {case.kwargs}'
        )
    else:
        result =



#    def test_expected_outcome(case):
#        try:
#            expected_outcome = ExpectedOutcome(case.argument)
#        except Exception:
#            pytest.fail(f'Unable to instantiate ExpectedOutcome for {case.argument}')
#        else:
#            result = eval(f'expected_outcome.{case.attribute}')#

#        if result is not case.correct_outcome and result != case.correct_outcome:
#            pytest.fail(f"ExpectedOutcome({case.argument}) results in {repr(result)} "
#                        f"but should result in {case.correct_outcome}.")


"""


@pytest.fixture(scope='module')
def actual_outcome_no_args():
    return ActualOutcome(return_douglas_adams_number)

@pytest.fixture(scope='module')
def actual_outcome_runtimeerror():
    return ActualOutcome(raise_exception)


@pytest.fixture(scope='module')
def actual_outcome_warning():
    return ActualOutcome(return_douglas_adams_number)


@pytest.fixture(scope='module')
def actual_outcome_two_warnings():
    return ActualOutcome(
        issue_two_warnings_and_return_value,
        (RuntimeWarning, '...'),
        {'kwarg_warning': SyntaxWarning, 'kwarg_warning_message': '---'}
    )

"""