from typing import Any, Callable
from log.LoggerSetUp import logger
import typing


CallbackType = Callable[[dict[str, typing.Any]], None]

_event_map: dict[str, CallbackType] = dict()


def FeishuEventListener(event_type: str):
    '''
    ## DECORATOR
    To register a handler with specific Feishu Event

    usage: 

    @FeishuEventListener("im.message.receive_v1")
    def OnEventABC(data: object):
        pass
    '''
    def inner_decorator(f: CallbackType):
        if event_type in _event_map:
            logger.warning(
                "double declearation of EventListener: "+event_type)
        _event_map[event_type] = f
        return f
    return inner_decorator
