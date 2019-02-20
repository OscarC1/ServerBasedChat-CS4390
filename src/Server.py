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
import byteutil
import net

import crypto
from Client import BaseClient as Client


def getSecret(client_id):
    raise NotImplementedError


class BaseServer(object):

    """A basic server with attributes.

    Currently unused. """

    def __init__(self, server_ip, port_udp):
        super().__init__()
        self.ip = server_ip
        self.port_udp = port_udp


class RunnableServer(BaseServer):

    """A stateful server with user interaction"""

    def run(self):
        print("Starting server on {}:{}".format(self.ip, self.port_udp))

        self.login_handles = dict()

        ss_udp = socketserver.UDPServer((self.ip, self.port_udp), UDPListener)
        ss_udp.master = self
        ss_udp.serve_forever()
        # raise NotImplementedError

    def onUDP(self, sock, code, args, client_address):
        if code == Code.HELLO.value:
            (client_id,) = byteutil.consumeStringArgs(args)

            print("Hello with client id", client_id)
            client = Client(client_id)

            # Challenge client
            rand = crypto.cRandom()

            self.login_handles[client.id] = rand

            message = byteutil.message2bytes([
                Code.CHALLENGE,
                rand
            ])
            net.sendUDP(sock, message, client_address)
        elif code == Code.RESPONSE.value:
            (client_id, response) = byteutil.consumeStringArgs(args)
            client = Client(client_id)

            rand = self.login_handles.get(client.id)
            if rand is not None:
                xres = crypto.a3(rand, client.secret)
                print(rand, client.secret, xres)
                print(xres == response)
                if xres == response:
                    pass
                    # Success
            # otherwise, failure
        else:
            print("No behavior for UDP code", code)

    def onHello(arguments, source_address):
        """
        Upon receiving HELLO (Client-ID-A), the server looks up Client A’s secret key K_A.
        Then it generates a random number rand. Rand and K_A are input into an authentication algorithm A3.
        The output, XRES, is stored by the server. Then the server sends rand in the CHALLENGE (rand).
        Client A is expected to run the same algorithm A3 with the same inputs rand and K_A, and produce RES, which is sent to the server in the RESPONSE (Res) message.
        If RES matches XRES, the server has authenticated the client.
        """


class UDPListener(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        client_address = self.client_address
        request = self.request
        master = self.server.master

        message = request[0]
        print(request)
        print(client_address)

        print("┌ Recieved UDP message")
        print("│ Source: {}:{}".format(*client_address))
        print("│ ┌Message (bytes): '{}'".format(message))
        print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

        _code, *rest = byteutil.bytes2message(message)
        code = int.from_bytes(_code, byteorder='big')
        master.onUDP(self.server.socket, code, rest, client_address)