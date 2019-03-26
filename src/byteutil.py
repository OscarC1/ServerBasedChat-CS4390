#!/bin/python3
"""
# Description:
Byte utilities

# Authors:
- Seth Giovanetti
- Oscar Contreras
"""

from enum import Enum

NULL_BYTE = bytes(1)
MESSAGE_SEP = bytes('\x1f', 'utf-8')


def x2bytes(object):
    # print(object)
    if isinstance(object, str):
        return str2bytes(object)
    if isinstance(object, Enum):
        return bytes([object.value])
    # if isinstance(object, int):
    #     return object.to_bytes(8, byteorder='big')
    if isinstance(object, bytes):
        return object
    raise AssertionError("Cannot coerce object '{}' to bytes".format(object))

# def int_to_bytes(i: int, *, signed: bool = False) -> bytes:
#     length = (i.bit_length() + 7 + int(signed)) // 8
#     return i.to_bytes(length, byteorder='big', signed=signed)


def str2bytes(string):
    return bytes(string.encode('utf-8'))


def split(bytes):
    return bytes.split(NULL_BYTE)


def bytes2message(bytes):
    print("bytes2message got", repr(bytes))
    code, *rest = bytes.split(NULL_BYTE)
    codePlusMsg = [int.from_bytes(code, byteorder='big')] + [b.decode('utf-8') for b in rest]
    return codePlusMsg


def bytes2message2(mybytes):
    # print("bytes2message2 got "+ repr(mybytes))
    for byteMsg in mybytes.split(MESSAGE_SEP):
        # print("byteMsg " + repr(byteMsg))
        if(byteMsg == b'\x0f\x00'):
            print("", end='')
            # print("empty byteMsg " + repr(byteMsg)) # history byte stream was interrupted/delayed
        else:
            # print("good byteMsg" + repr(byteMsg))
            code, *rest = byteMsg.split(NULL_BYTE)
            # print("code " + repr(code))
            # print("rest" + repr(rest))

            if(code == b'\x0f'):
                (person, msg, *extraNull) = rest
                # print("person " + repr(person))
                # print("msg " + repr(msg))
                (rmsg, *empty) = msg.split(b'\x0f')
                rest2 = (person, rmsg)
            else:
                rest2 = rest

            (code, *msg) = [int.from_bytes(code, byteorder='big')] + [b.decode('utf-8') for b in rest2]
            yield (code, *msg)


def bytes2bytemsg(bytes):
    code, *rest = bytes.split(NULL_BYTE)
    codePlusMsg = [int.from_bytes(code, byteorder='big')] + rest
    return codePlusMsg


def message2bytes(message):
    return NULL_BYTE.join(map(x2bytes, message))


def formatBytesMessage(message):
    from Codes import codeno
    code, *rest = bytes2message(message)
    return ", ".join([codeno(code).name] + rest)
