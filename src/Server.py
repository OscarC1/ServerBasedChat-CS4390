#!/bin/python3
"""
# Description: 
Server classes

# Authors:
- Seth Giovanetti
"""

import socketserver
import socket
from Codes import Code
import traceback
import byteutil

import crypto
from Client import BaseClient as Client


def getSecret(client_id):
    raise NotImplementedError


class BaseServer(object):

    """A basic server with attributes.

    Currently unused. """

    def __init__(self, server_ip, port_udp_listen):
        super().__init__()
        self.ip = server_ip
        self.port_udp_listen = port_udp_listen


class RunnableServer(BaseServer):

    """A stateful server with user interaction"""

    def run(self):
        raise NotImplementedError

    def onHello(client_id):
        """
        Upon receiving HELLO (Client-ID-A), the server looks up Client A’s secret key K_A.
        Then it generates a random number rand. Rand and K_A are input into an authentication algorithm A3.
        The output, XRES, is stored by the server. Then the server sends rand in the CHALLENGE (rand).
        Client A is expected to run the same algorithm A3 with the same inputs rand and K_A, and produce RES, which is sent to the server in the RESPONSE (Res) message.
        If RES matches XRES, the server has authenticated the client.
        """

        client = Client(client_id)
        rand = crypto.cRandom()
        xres = crypto.a3(rand, client.secret)
