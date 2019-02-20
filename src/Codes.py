#!/bin/python3

from enum import Enum

try:
    from enum import auto
except ImportError:
    # Not running python 3.6+
    _auto_i = 0
    def auto():
        global _auto_i
        _auto_i += 1
        return _auto_i


class Code(Enum):
    HELLO = auto()
    CHALLENGE = auto()
    RESPONSE = auto()
    AUTH_SUCCESS = auto()
    AUTH_FAIL = auto()
    CONNECT = auto()
    CONNECTED = auto()
    CHAT_REQUEST = auto()
    CHAT_STARTED = auto()
    UNREACHABLE = auto()
    END_REQUEST = auto()
    END_NOTIF = auto()
    CHAT = auto()
    HISTORY_REQ = auto()
    HISTORY_RESP = auto()
