#!/bin/python3
"""
# Description:
Byte utilities

# Authors:
- Seth Giovanetti
- Oscar Contreras
"""

from enum import Enum

MESSAGE_TERM = bytes(chr(3), 'utf-8')
NULL_BYTE = bytes(1)


def x2bytes(object):
    """Coerces an object to bytes, generically.
    
    Args:
        object
    
    Returns:
        bytes
    
    Raises:
        AssertionError: No known coercion method.
    """
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
    """Encode string."""
    return bytes(string.encode('utf-8'))


def split(bytes):
    """Split on the null byte.

    Returns:
        List
    """
    return bytes.split(NULL_BYTE)


def bytes2message(bytes):
    """Decodes a message.
    Should return a (code, *message) object.
    
    Args:
        bytes (bytes): Byte-encoded message.
    
    Returns:
        Tuple
    """
    # print("bytes2message got", repr(bytes))
    code, *rest = bytes.split(NULL_BYTE)
    codePlusMsg = [int.from_bytes(code, byteorder='big')] + [b.decode('utf-8') for b in rest]
    return codePlusMsg


def bytes2messages(mybytes):
    """Given a bytes object, generates messages contained. 
    
    Args:
        mybytes (bytes): Terminated messages
    
    Yields:
        message: See bytes2message
    """
    # print("bytes2messages got", repr(mybytes))
    messages = mybytes.split(MESSAGE_TERM)[:-1]
    # print(messages)
    for byteMsg in messages:
        # print("byteMsg", repr(byteMsg))
        yield bytes2message(byteMsg)


def bytes2bytemsg(bytes):
    """Decodes the CODE part of the message."""
    code, *rest = bytes.split(NULL_BYTE)
    codePlusMsg = [int.from_bytes(code, byteorder='big')] + rest
    return codePlusMsg


def message2bytes(message):
    """Encodes a message as bytes"""
    return NULL_BYTE.join(map(x2bytes, message))


def formatBytesMessage(message):
    # print(message)
    from Codes import codeno
    
    return " | ".join(
        ", ".join([codeno(code).name] + rest)
        for code, *rest in bytes2messages(message)
    )
