import pytest
from plasmapy.utils.pytest_helpers import ExpectedOutcome

expected_exception = KeyError
expected_warning = UserWarning
expected_value = 42


@pytest.fixture(scope="module")
def expected_outcome_exception():
    return ExpectedOutcome(expected_exception)


attr_strings_and_expected_values = [
    ('.exception', expected_exception),
    ('.warning', None),
]

def test_for_expected_outcome_attrs_for_exception(expected_outcome_exception):
    errors = []

    if expected_outcome_exception.exception is not expected_exception:
        errors.append(f"{expected_outcome_exception}.exception is not {expected_exception}")

    if expected_outcome_exception.warning is not None:
        errors.append(f"{expected_outcome_exception}.warning is not None")

    if expected_outcome_exception.value is not None:
        errors.append(f"{expected_outcome_exception}.value is not None")

    if errors:
        pytest.fail(' '.join(errors))


@pytest.mark.parametrize(
    "arg, attr_string, expected_value",
    [
        (KeyError, '.exception')
    ]

)

def test_klfsljk(arg, attr_string, expected_value):


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