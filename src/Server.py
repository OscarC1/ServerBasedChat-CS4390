#!/bin/python3
"""
# Description: 
Server classes

# Authors:
- Seth Giovanetti
"""

import byteutil
import net
import socketserver
import threading

from Codes import Code, printCodes
from pprint import pprint
from prompt import Prompt

import crypto

from Client import BaseClient as Client

from listener import TCPListener
from listener import UDPListener


class BaseServer():

    """A basic server with attributes."""

    def __init__(self, server_ip, port_udp, port_tcp):
        # super().__init__()
        self.ip = server_ip
        self.port_udp = port_udp
        self.port_tcp = port_tcp


class RunnableServer(BaseServer):

    """A stateful server with user interaction"""

    def run(self):
        print("Starting server on {}:{}".format(self.ip, self.port_udp))

        self.login_handles = dict()
        self.challenge_handles = dict()

        self.connections_by_id = dict()
        self.clients_by_address = dict()

        ss_udp = socketserver.UDPServer(('', self.port_udp), UDPListener)
        ss_udp.callback = self.onUDP
        udp_thread = threading.Thread(daemon=True, target=ss_udp.serve_forever)
        udp_thread.start()

        self.prompt()

    def cmd_net(self, *args):
        print("Network status: ")
        print("UDP: \t{}:{}".format(self.ip, self.port_udp))
        print("TCP: \t{}:{}".format(self.ip, self.port_tcp))
        print("Active TCP connections: ")
        for key, server in self.connections_by_id.items():
            print(key, net.reprSocketServer(server), sep="\t")

    def prompt(self):
        p = Prompt()
        p.registerCommandsFromNamespace(self, "cmd_")
        p.registerCommand(
            "codes",
            printCodes,
            helpstr="Print protocol codes"
        )
        p.registerCommand(
            "vars",
            lambda *a: pprint(vars(self)),
            helpstr="Show own variables"
        )
        p()

        # raise NotImplementedError

    def startTCPConnection(self, udp_socket, client, client_address):

        # Configure TCP connection
        print("Spinning up new TCP socket")
        ss_tcp = socketserver.TCPServer(('', self.port_tcp), TCPListener)
        ss_tcp.callback = self.onTCP
        tcp_thread = threading.Thread(daemon=True, target=ss_tcp.serve_forever)
        tcp_thread.start()
        self.connections_by_id[client.id] = ss_tcp

        print("Configuring TCP cookie")
        token = crypto.cRandom()
        self.login_handles[token] = client.id

        net.sendUDP(
            udp_socket,
            byteutil.message2bytes([
                Code.AUTH_SUCCESS,
                token,
                self.port_tcp
            ]),
            client_address
        )

    def finalizeTCPConnection(self, connection, token, client_address):

        if self.login_handles.get(token):
            client = Client(self.login_handles.get(token))
            print("Client", client.id, "logged in")
            net.sendTCP(
                connection,
                byteutil.message2bytes([
                    Code.CONNECTED
                ])
            )
            # Register client
            self.clients_by_address[client_address] = client
            # Cleanup
            self.login_handles.pop(token)
        else:
            print("Bad login information")
            print("No token")
            print(token)

    def onTCP(self, connection, code, args, client_address):
        # Register new clients
        if code == Code.CONNECT.value:
            print("Got TCP CONNECT code")
            (token,) = args
            self.finalizeTCPConnection(connection, token, client_address)
            return

        # Identify client
        try:
            client = self.clients_by_address[client_address]
        except KeyError as e:
            print("Connection attempted by unknown address", client_address)
            return

        # Act on client
        if code == Code.DISCONNECT.value:
            print("Got TCP DISCONNECT message")

            ss_tcp = self.connections_by_id[client.id]
            print("Closing", ss_tcp)

            # TODO: Shut down properly
            # ss_tcp.shutdown()
            ss_tcp.server_close()

            print("Unregistering client")
            self.connections_by_id.pop(client.id)
            self.clients_by_address.pop(client_address)

            print("Disconnected client", client_address)

        elif code == Code.CHAT.value:
            print("Got TCP CHAT message")
            (message,) = args
            print(message)
            net.sendTCP(
                connection, 
                byteutil.message2bytes([
                    Code.CHAT,
                    "Hi back"
                ])
            )
        else:
            print("No behavior for TCP code", code)

    def onUDP(self, sock, code, args, client_address):
        if code == Code.HELLO.value:
            (client_id,) = args

            print("Got Hello with client id", client_id)
            client = Client(client_id)

            # Challenge client
            self.challenge_handles[client.id] = rand = crypto.cRandom()

            print("Sending challenge")
            net.sendUDP(
                sock,
                byteutil.message2bytes([
                    Code.CHALLENGE,
                    rand
                ]),
                client_address
            )
        elif code == Code.RESPONSE.value:
            (client_id, response) = args
            client = Client(client_id)

            print("Got response from client", client.id)

            rand = self.challenge_handles.pop(client.id)
            if rand is not None:
                xres = crypto.a3(rand, client.secret)
                # print(rand, client.secret, xres)
                # print(xres == response)
                if xres == response:
                    # Success
                    print("Authentication success")
                    # TODO: Destroy any loose connections on this address.
                    self.startTCPConnection(sock, client, client_address)
                    return
            # otherwise, failure
            print("Authentication failure")
            net.sendUDP(
                sock,
                byteutil.message2bytes([
                    Code.AUTH_FAIL
                ]),
                client_address
            )
        else:
            print("No behavior for UDP code", code)
