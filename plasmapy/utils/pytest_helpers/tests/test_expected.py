import pytest
from plasmapy.utils.pytest_helpers.expected import (
    ExpectedOutcome,
    _is_warning,
    _is_exception,
    _is_warning_and_value,
)



expected_exception = KeyError
expected_warning = UserWarning
expected_value = 42


@pytest.fixture(scope="module")
def expected_outcome_for_an_exception():
    return ExpectedOutcome(expected_exception)


attribute_strings_and_expected_values = [
    ('.exception', expected_exception),
    ('.warning', None),
    ('.value', None),

]

@pytest.mark.parametrize(
    "attribute_string, expected",
    attribute_strings_and_expected_values
)
def test_expected_outcome_attributes_for_an_exception(
        attribute_string,
        expected,
        expected_outcome_for_an_exception,
):
    result = eval("expected_outcome_for_an_exception" + attribute_string)

    assert result is expected or result == expected





def test_for_expected_outcome_attrs_for_exception(expected_outcome_for_an_exception):
    errors = []

    if expected_outcome_for_an_exception.exception is not expected_exception:
        errors.append(
            f"{expected_outcome_exception}.exception should be"
            f"{expected_exception}, but instead is "
            f"{expected_outcome_exception.exception}."
        )

    if expected_outcome_for_an_exception.warning is not None:
        errors.append(
            f"{expected_outcome_for_an_exception}.warning should return None,"
            f"but instead returns ")

    if expected_outcome_for_an_exception.value is not None:
        errors.append(f"{expected_outcome_for_an_exception}.value is not the expected value of None")

#    errors.append('asdfas')
#    errors.append('asdfasadf')

    if errors:


        pytest.fail(' '.join(errors))


#@pytest.mark.parametrize(
#    "arg, attr_string, expected_value",
#    [
#        (KeyError, '.exception', KeyError)
#    ]

#)

#def test_(arg, attr_string, expected_value):

#    ...
"""
class TestExpectedOutcome:
    @classmethod
    def setup_class(cls):
        cls.expected_outcomes = {
            'value': ExpectedOutcome(expected_value),
            'warning': ExpectedOutcome(expected_warning),
            'exception': ExpectedOutcome(expected_exception),
            'value and warning': ExpectedOutcome((expected_value, expected_warning)),
            'warning and value': ExpectedOutcome([expected_warning, expected_value]),
        }

    def test_exception_attrs(self):
        expected_outcome = self.expected_outcomes['exception']
        list_of_errors = []

        if expected_outcome.exception is not ep



        list_of_errors = []

        if expected_outcome.exception is not expected_exception:
            list_of_errors.append()

 #       if expected_outcome.

#        assert self.instances['exception'].exception is expected_exception
#        assert self.instances['exception'].expecting_exception is True
#        assert self.instances['exception'].expecting_value is False
#        assert self.instances['exception']

#        if

"""


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
