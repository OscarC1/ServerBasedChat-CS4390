#!/bin/python3
"""
# Description
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

import socketserver
from listener import TCPListener
import threading


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
        self.disconnect()

    def login(self, server):
        # Store our associated server
        self.server = server

        # Prepare UDP socket to send and recieve
        sock = net.newUDPSocket()

        # src_address = (net.getOwnIP(), 0,)
        # sock.bind(src_address)
        # print("Socket open on", src_address)

        # Send UDP HELLO to server
        serv_address_udp = (self.server.ip, self.server.port_udp,)
        net.sendUDP(
            sock,
            byteutil.message2bytes([
                Code.HELLO,
                self.id
            ]),
            serv_address_udp
        )

        # Expect CHALLENGE from server
        print("Awaiting CHALLENGE from server")
        response, serv_address_udp = net.awaitUDP(sock, 2**16)
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
            serv_address_udp
        )

        # Expect AUTH_SUCCESS or AUTH_FAIL from server
        print("Awaiting AUTH result from server")
        response, serv_address_udp = net.awaitUDP(sock, 2**16)
        code, *rest = byteutil.bytes2bytemsg(response)  # rest includes raw int data here, don't stringify

        if code == Code.AUTH_FAIL.value:
            raise PermissionError("Server rejected key authentication with code", code)

        assert code == Code.AUTH_SUCCESS.value, "Got non-auth code {}".format(code)
        (token, server_tcp_port_bytes) = rest

        print("Closing UDP socket")
        sock.close()

        # Establish TCP Connection
        print("Establishing TCP connection with cookie")
        self.token = token
        self.server_tcp_port = int.from_bytes(server_tcp_port_bytes, byteorder='big')

        # Create a TCP address with our old IP and our new port
        (server_ip, udp_port) = serv_address_udp
        serv_address_tcp = (server_ip, self.server_tcp_port)

        # print("Starting up TCP listener")
        # self.tcp_server = socketserver.TCPServer(src_address, TCPListener)
        # self.tcp_server.master = self
        # self.tcp_thread = threading.Thread(daemon=True, target=self.tcp_server.serve_forever)
        # self.tcp_thread.start()

        print("Connecting TCP socket", serv_address_tcp)
        # self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # serv_address_tcp = (server_ip, self.server_tcp_port)
#         self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect(serv_address_tcp)

        net.sendTCP(
            self.tcp_socket,
            byteutil.message2bytes([
                Code.CONNECT,
                token
            ])
        )
        # Expect CONNECTED

        message = net.awaitTCP(self.tcp_socket, 2**16)
        code, *rest = byteutil.bytes2message(message)
        assert code == Code.CONNECTED.value, "Got non-connect code {}".format(code)

        print("Logged in successfully.")
        print(self.tcp_socket)

        tcp_thread = threading.Thread(daemon=True, target=self.tcpListener, args=(self.tcp_socket, self.onTCP))
        tcp_thread.start()

    def tcpListener(self, sock, callback):
        # self.listening = threading.Event()
        sock.settimeout(None)
        while True:
            message = sock.recv(1024)
            assert message

            source_address = sock.getpeername()

            print("┌ Recieved TCP message")
            print("│ Source: {}:{}".format(*source_address))
            print("│ ┌Message (bytes): {}".format(message))
            print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

            code, *rest = byteutil.bytes2message(message)
            callback(sock, code, rest, source_address)

    def tcp_say(self, *args):
        print("tcp say:", args)
        net.sendTCP(
            self.tcp_socket,
            byteutil.message2bytes([
                Code.CHAT,
                " ".join(args)
            ])
        )

    def disconnect(self, *args):
        net.sendTCP(
            self.tcp_socket,
            byteutil.message2bytes([
                Code.DISCONNECT
            ])
        )
        raise KeyboardInterrupt

    def onTCP(self, connection, code, args, source_address):
        if False:
            pass
        else:
            print("No behavior for TCP code", code)

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
        p.registerCommand(
            "say",
            self.tcp_say,
            helpstr="Say"
        )
        p.registerCommand(
            "disconnect",
            self.disconnect,
            helpstr="Disconnect session"
        )
        p()
