from plasmapy.utils.pytest_helpers.expected import ExpectedOutcome
from plasmapy.utils.pytest_helpers.exceptions import *
from typing import Optional, Dict, Any, Union, Tuple, List
from plasmapy.utils.pytest_helpers import call_string

class ThingToTest:
    def __init__(self, callable_object, args: Union[Tuple, List, Any] = (), kwargs: Dict[Any, Any] = {}):
        try:
            self.callable_object = callable_object
            self.kwargs = kwargs
            self.args = args
        except Exception as exc:
            raise InvalidTestError(
                f"Cannot "
            ) from exc

    @property
    def callable_object(self):
        return self._callable_object

    def callable_object(self, function_or_class):
        if not callable(function_or_class):
            raise InvalidTestError(f"{function_or_class} is not a callable object")
        self._callable_object = function_or_class

    @property
    def arguments(self):
        return self._arguments

    @args.setter
    def arguments(self, args):
        if isinstance(args, {})

        if not isinstance(args, (list, tuple)):
            args = (args,)


    @property
    def expression(self):
        return call_string()

def run_test(callable_object, args=(), kwargs={}, expected, *, atol=0.0, rtol=0.0):
    __tracebackhide__ = True
    expected_outcome = ExpectedOutcome(expected)
    actual_outcome = ActualOutcome(callable_object, args, kwargs)
    comparison = Comparison(ActualOutcome, ExpectedOutcome)


    comparison = Comparison(actual_outcome, expected_outcome)
    if comparison.failed:
        pytest.fail()


    #if expected_outcome.expecting_exception:
    #    thing_to_test.check_for_exception()


