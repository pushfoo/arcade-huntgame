from unittest.mock import Mock

import pytest

from huntgame.utils import DeferredCall


@pytest.fixture(params=(None, 1, 'string'))
def return_value(request):
    return request.param


@pytest.fixture
def mock_callable(return_value):
    return Mock(return_value=return_value)


@pytest.fixture(params=[
    (),
    (1, 2, 3),
    ({1: 2},)
])
def c_args(request):
    return request.param


@pytest.fixture(params=[
    {},
    {"str": "dict"},
    {"long": 0, "dict": 1, "with": 2, "many": dict, "values": ()}
])
def c_kwargs(request):
    return request.param


@pytest.fixture
def logger(monkeypatch) -> Mock:
    logger = Mock()
    monkeypatch.setattr('huntgame.utils.logger', logger)

    return logger


@pytest.fixture
def deferred_call_instance(mock_callable, c_args, c_kwargs):
    return DeferredCall(mock_callable, *c_args, **c_kwargs)


def test_new_uses_passed_callable(deferred_call_instance, mock_callable):
    assert deferred_call_instance.callable is mock_callable
    assert deferred_call_instance[0] is mock_callable


def test_new_uses_passed_args(deferred_call_instance, c_args):
    assert deferred_call_instance.args == c_args
    assert deferred_call_instance[1] == c_args


def test_new_uses_passed_kwargs(deferred_call_instance, c_kwargs):
    assert deferred_call_instance.kwargs == c_kwargs
    assert deferred_call_instance[2] == c_kwargs


def test_calling_instance_returns_expected_return_value(deferred_call_instance, return_value):
    assert deferred_call_instance() == return_value


def test_calling_instance_uses_expected_values(deferred_call_instance, mock_callable, c_args, c_kwargs):
    _ = deferred_call_instance()
    mock_callable.assert_called_with(*c_args, **c_kwargs)


@pytest.mark.parametrize('message_arg,expected_message', [
    (None, DeferredCall.DEFAULT_CALL_LOG_TEMPLATE),
    ('Test', 'Test')
 ])
def test_calling_instance_uses_appropriate_message_and_args(
    message_arg,
    expected_message,
    deferred_call_instance,
    logger
):
    deferred_call_instance(message_arg)
    logger.debug.assert_called_once_with(
        expected_message,
        deferred_call_instance.callable,
        deferred_call_instance.args,
        deferred_call_instance.kwargs
    )
