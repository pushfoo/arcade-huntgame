from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    TypeVar,
    Tuple
)
from typing_extensions import ParamSpec
from functools import lru_cache as _lru_cache


from loguru import logger


_PS = ParamSpec("_PS")
_RT = TypeVar("_RT")
_CallableT = Callable[_PS, _RT]
# This might not work fully until later Python versions due to the
# limitations placed on typing_extensions by earlier Python releases.
#_ArgsT = _PS.args
#_KwargsT = _PS.kwargs


def cache(fn: _CallableT) -> _CallableT:
    """
    Backport of cache decorator added in 3.9.

    :param fn: A callable
    :return:
    """
    return _lru_cache(maxsize=None)(fn)


# The 'ordinary' call template type for backward-compatibility with
# tuples when writing code rapidly.
CallTemplate = Tuple[_CallableT, Tuple, Dict]


class DeferredCall(CallTemplate):
    """
    An ugly kludge for GL initialization problems.

    This is mostly to work around problems with initializing views.
    """
    DEFAULT_CALL_LOG_TEMPLATE: str = "Deferred call of {} with: args={}, kwargs={}"

    def __new__(cls, _callable: _CallableT, *args: Any, **kwargs: Any):
        return super().__new__(cls, (_callable, args, kwargs))

    @property
    def callable(self) -> _CallableT:
        return self[0]

    @property
    def args(self) -> Tuple[Any, ...]:
        return self[1]

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self[2]

    def __call__(self, log_message: Optional[str] = None) -> _RT:
        result = self.callable(*self.args, **self.kwargs)

        # Log the result
        log_message = log_message or self.DEFAULT_CALL_LOG_TEMPLATE
        logger.debug(log_message, self.callable, self.args, self.kwargs)

        return result
