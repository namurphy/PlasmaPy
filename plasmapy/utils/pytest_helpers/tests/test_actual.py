import pytest
import warnings

from plasmapy.utils.pytest_helpers import ActualOutcome


def raise_runtimeerror(error_message: str):
    raise RuntimeError(error_message)


def return_argument_and_issue_warning(arg, warning_message, *, kwarg=Warning):
    warnings.warn(warning_message, kwarg)
    return arg


def issue_two_warnings_and_return_value(
        value: object,
        arg_warning: Warning,
        arg_warning_message: str,
        *,
        kwarg_warning: Warning = Warning,
        kwarg_warning_message: str = '',
):
    warnings.warn(arg_warning_message, arg_warning)
    warnings.warn(kwarg_warning_message, kwarg_warning)
    return value


def return_arg(arg):
    return arg

@pytest.fixture
def actual_outcome_runtimeerror():
    return ActualOutcome(raise_runtimeerror)


@pytest.fixture
def actual_outcome_warning():
    return ActualOutcome(UserWarning)


@pytest.fixture
def actual_outcome_two_warnings():
    return ActualOutcome(iss)
