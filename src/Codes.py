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
        if _auto_i == 3:  # Skip message term symbol
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
    DISCONNECT = auto()

    def __str__(self):
        return "\t".join(
            map(str, [self.value, bytes([self.value]), self.name])
        )

    # def __str__(self):
    #     return self.__repr__()

def codeno(i):
    for c in Code:
        if c.value == i:
            return c
    raise KeyError(i)

def printCodes():
    print("\n".join(c.__str__() for c in Code))
