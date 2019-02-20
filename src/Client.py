#!/bin/python3
"""
# Description: 
Client classes

# Authors:
- Seth Giovanetti
"""

import byteutil
import crypto
import net
import socket

from Codes import Code
from pprint import pprint
from prompt import Prompt


class BaseClient(object):

    """A basic client with attributes"""

    def __init__(self, id):
        super().__init__()
        self.id = id
        self._secret = None

    @property
    def secret(self):
        if self._secret is None:
            self.loadSecret()
        return self._secret
        
    def loadSecret(self, gen_on_fail=False):
        try:
            self._secret = crypto.getKey(self.id)
            print("Loaded stored key for ID " + self.id)
        except KeyError as e:
            if gen_on_fail:
                self.genSecret()
            else:
                raise e

    def genSecret(self):
        new_secret = crypto.cRandom(128)
        crypto.storeKey(new_secret, self.id)
        print("New key generated for client ID " + self.id)
        self._secret = new_secret


class RunnableClient(BaseClient):

    """A stateful client with user interaction"""
    def run(self, server):
        self.loadSecret(gen_on_fail=True)
        self.login(server)
        self.prompt()

    def login(self, server):
        # Store our associated server
        self.server = server

        # Prepare UDP socket to send and recieve
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        host = net.getOwnIP()
        src_address = (host, 0,)
        sock.bind(src_address)
        print("Socket open on", src_address)

        # Send UDP HELLO to server
        server_address = (self.server.ip, self.server.port_udp,)
        net.sendUDP(
            sock,
            byteutil.message2bytes([
                Code.HELLO,
                self.id
            ]),
            server_address
        )

        # Expect CHALLENGE from server
        response, server_address = net.awaitUDP(sock, 2**16)
        code, rand = byteutil.bytes2message(response)

        assert code == Code.CHALLENGE.value, "Got non-challenge code {}".format(code)

        # Decrypt challenge with our secret
        response = crypto.a3(rand, self.secret)

        # Send RESPONSE to server
        net.sendUDP(
            sock,
            byteutil.message2bytes([
                Code.RESPONSE,
                self.id,
                response
            ]),
            server_address
        )

        # Expect AUTH_SUCCESS or AUTH_FAIL from server
        response, server_address = net.awaitUDP(sock, 2**16)
        code, *rest = byteutil.bytes2bytemsg(response)  # rest includes raw int data here, don't stringify

        if code == byteutil.x2bytes(Code.AUTH_FAIL):
            raise PermissionError("Server rejected key authentication.")

        assert code == Code.AUTH_SUCCESS.value, "Got non-auth code {}".format(code)
        (token, server_tcp_port) = rest
        sock.close()

        # Establish TCP Connection
        self.token = token
        self.server_tcp_port = int.from_bytes(server_tcp_port, byteorder='big')

        (server_ip, udp_port) = server_address
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, self.server_tcp_port)
        print(server_address)
        self.tcp_socket.connect(server_address)

        net.sendTCP(
            self.tcp_socket,
            byteutil.message2bytes([
                Code.CONNECT,
                token
            ])
        )
        # Expect CONNECTED
        message = self.tcp_socket.recv(2**16)
        code, *rest = byteutil.bytes2message(message)
        assert code == Code.CONNECTED.value, "Got non-connect code {}".format(code)

        print("Logged in successfully.")

    def prompt(self):
        """Interactive prompt
        """

        p = Prompt()
        p.registerCommand(
            "codes",
            lambda *a: print("\n".join(c.__str__() for c in Code)),
            helpstr="Print protocol codes"
        )
        p.registerCommand(
            "vars",
            lambda *a: pprint(vars(self)),
            helpstr="Show own variables"
        )
        p()
