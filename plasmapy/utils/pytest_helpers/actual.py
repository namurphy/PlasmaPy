import pytest
from typing import List, Optional, Dict, Tuple, Any, Union
#import collections

class _TestParameters:
    def __init__(self):
        ...

    @property
    def callable_object(self):
        return self._callable_object

    @callable_object.setter
    def callable_object(self, obj):
        if callable(obj):
            self._callable_object = obj
        else:
            raise TypeError(f"{repr(obj)} is not callable.")

    @property
    def positional_arguments(self):
        return self._positional_arguments

    @args.setter
    def keyword_arguments(self, kwargs: Dict[str, Any]):


class ActualOutcome:

    def __init__(self, callable_object, args=tuple(), kwargs=dict()):

        if not isinstance(args, (tuple, list)):
            args = (args,)

        self._info = {}

        try:
            with pytest.warns(None) as warnings_record:
                result = callable_object(*args, **kwargs)
        except Exception as exception_record:
            ...




    @property
    def exception(self) -> Optional[Exception]:
        return self._info['exception'] if self.got_an_exception else None

    @property
    def warnings(self) -> Optional[List]:
        return self._info['warnings'] if self.got_a_warning else None

    @property
    def value(self) -> Optional[object]:
        return self._info['value'] if self.got_a_value else None

    @property
    def got_an_exception(self) -> bool:
        return 'exception' in self._info.keys()

    @property
    def got_a_warning(self) -> bool:
        return 'warnings' in self._info.keys()

    @property
    def got_a_value(self) -> bool:
        return 'value' in self._info.keys()
