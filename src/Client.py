#!/bin/python3
"""
# Description: 
Client classes

# Authors:
- Seth Giovanetti
"""

import crypto
import socket
from Codes import Code
import byteutil
import net


class BaseClient(object):

    """A basic client with attributes"""

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.loadSecret(gen_on_fail=True)

    def loadSecret(self, gen_on_fail=False):
        try:
            self.secret = crypto.getKey(self.id)
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
        self.secret = new_secret


class RunnableClient(BaseClient):

    """A stateful client with user interaction"""

    def run(self, server):
        self.login(server)
        self.prompt()

    def login(self, server):
        # Store our associated server
        self.server = server

        # Prepare socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # host = socket.gethostname()
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
        code, _rand = byteutil.bytes2message(response)
        rand = _rand.decode('utf-8')

        assert code == byteutil.x2bytes(Code.CHALLENGE), "Got non-challenge code {}".format(int.from_bytes(code))

        # Decrypt
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
        code, *rest = byteutil.bytes2message(response)

        if code == byteutil.x2bytes(Code.AUTH_FAIL):
            raise PermissionError("Server rejected key authentication.")

        assert code == byteutil.x2bytes(Code.AUTH_SUCCESS), "Got non-auth code {}".format(int.from_bytes(code))
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
        assert code == byteutil.x2bytes(Code.CONNECTED), "Got non-connect code {}".format(int.from_bytes(code))

        print("Logged in successfully.")

    def prompt(self):
        """Interactive prompt
        """
        while True:
            user_input = input("> ")
            print(user_input)
