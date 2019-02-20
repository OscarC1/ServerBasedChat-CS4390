from enum import Enum

NULL_BYTE = bytes(1)


def x2bytes(object):
    if isinstance(object, str):
        return str2bytes(object)
    if isinstance(object, Enum):
        return bytes([object.value])
    if isinstance(object, int):
        return bytes([object])
    if isinstance(object, bytes):
        return object
    raise AssertionError("Cannot coerce object '{}' to bytes".format(object))


def str2bytes(string):
    return bytes(string.encode('utf-8'))


def split(bytes):
    return bytes.split(NULL_BYTE)


def bytes2message(bytes):
    code, *rest = bytes.split(NULL_BYTE)
    codePlusMsg = [int.from_bytes(code, byteorder='big')] + [b.decode('utf-8') for b in rest]
    return codePlusMsg

def bytes2bytemsg(bytes):
    code, *rest = bytes.split(NULL_BYTE)
    codePlusMsg = [int.from_bytes(code, byteorder='big')] + rest
    return codePlusMsg

def message2bytes(message):
    return NULL_BYTE.join(map(x2bytes, message))


def formatBytesMessage(message):
    return ", ".join(map(str, bytes2message(message)))
