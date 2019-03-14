#!/bin/python3
"""
# Description:
History management

# Authors:
- Seth Giovanetti
"""

import os

os.makedirs("history", exist_ok=True)

SEP = chr(7)


def getFile(session_id):
    return os.path.join("history", "{}.txt".format(session_id))


def append(session_id, sender, message):
    with open(getFile(session_id), "a", newline="\n") as histfile:
        histfile.write(sender + SEP + message + "\n")


def get(session_id):
    with open(getFile(session_id), "r", newline="\n") as histfile:
        for line in histfile:
            (cid, msg) = line.split(SEP)
            yield (cid, msg)
