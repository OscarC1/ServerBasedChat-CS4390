#!/bin/python3

from enum import Enum, auto


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
