import inspect


def _is_warning(obj) -> bool:
    """Return `True` if the argument is a warning, and `False` otherwise."""
    return inspect.isclass(obj) and issubclass(obj, Warning)


def _is_exception(obj) -> bool:
    """Return `True` if the argument is an exception, and `False` otherwise."""
    return inspect.isclass(obj) and issubclass(obj, Exception) and not issubclass(obj, Warning)


def _is_warning_and_value(obj) -> bool:
    """
    Return `True` if the argument is a `tuple` or `list` containing two
    items: a warning and an `object` that is not a warning; and `False`
    otherwise.
    """
    if not isinstance(obj, (list, tuple)) or len(obj) != 2:
        return False
    return _is_warning(obj[0]) ^ _is_warning(obj[1])


class ExpectedOutcome:

    def __init__(self, expected):
        self.expected = expected

    @property
    def expected(self):
        if self.expecting_exception:
            return self.exception
        elif self.expecting_warning and not self.expecting_value:
            return self.warning
        elif self.expecting_warning and self.expecting_value:
            return self.warning, self.value
        else:
            return self.value

    @expected.setter
    def expected(self, expected_outcome):
        self._info = dict()
        if _is_warning(expected_outcome):
            self._info['warning'] = expected_outcome
        elif _is_exception(expected_outcome):
            self._info['exception'] = expected_outcome
        elif _is_warning_and_value(expected_outcome):
            warning_is_first = _is_warning(expected_outcome[0])
            warning_index, value_index = (0, 1) if warning_is_first else (1, 0)
            self._info['warning'] = expected_outcome[warning_index]
            self._info['value'] = expected_outcome[value_index]
        else:
            self._info['value'] = expected_outcome

    @property
    def expecting_value(self) -> bool:
        return 'value' in self._info.keys()

    @property
    def value(self):
        return self._info['value'] if self.expecting_value else None

    @property
    def expecting_exception(self) -> bool:
        return 'exception' in self._info.keys()

    @property
    def exception(self):
        return self._info['exception'] if self.expecting_exception else None

    @property
    def expecting_warning(self) -> bool:
        return 'warning' in self._info.keys()

    @property
    def warning(self):
        return self._info['warning'] if self.expecting_warning else None

    def __repr__(self):
        return f'ExpectedOutcome({self.expected})'

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        try:
            return self.value == other.value
        except Exception as exc:
            raise TypeError(
                f"Unable to determine equality between {self}.value and"
                f"{other}.value"
            ) from exc

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        try:
            return self.value <= other.value
        except Exception as exc:
            raise TypeError(f"Cannot evaluate {self}.value <= {other}.value") from exc

    def __lt__(self, other):
        try:
            return self.value < other.value
        except Exception as exc:
            raise TypeError(f"Cannot evaluate {self}.value < {other}.value") from exc

    def __ge__(self, other):
        try:
            return self.value >= other.value
        except Exception as exc:
            raise TypeError(f"Cannot evaluate {self}.value <= {other}.value") from exc

    def __gt__(self, other):
        try:
            return self.value > other.value
        except Exception as exc:
            raise TypeError(f"Cannot evaluate {self}.value < {other}.value") from exc

    def __len__(self):
        try:
            return len(self.value)
        except Exception as exc:
            raise TypeError(f"Cannot evaluate len({self}.value)") from exc
