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
        new_secret = crypto.cRandom(2048)
        crypto.storeKey(new_secret, self.id)
        print("New key generated for client ID " + self.id)
        self.secret = new_secret


class RunnableClient(BaseClient):

    """A stateful client with user interaction"""

    def run(self, server):
        self.login(server)
        self.prompt()

    def login(self, server):
        # Prepare socket
        src_port = 128
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = socket.gethostname()
        src_address = (host, src_port,)
        sock.bind(src_address)

        # Send UDP HELLO to server
        dest_address = (self.ip, self.port_udp_listen,)
        message = byteutil.message2bytes([
            Code.HELLO,
            self.id
        ])
        net.sendUDP(sock, message, dest_address)

        # Expect CHALLENGE from server
        raise NotImplementedError

        # Decrypt

        # Send RESPONSE to server
        
        # Expect AUTH_SUCCESS or AUTH_FAIL from server

        # Establish TCP Connection

        # Expect CONNECTED

    def prompt(self):
        """Interactive prompt
        """
        while True:
            user_input = input("> ")
            print(user_input)
