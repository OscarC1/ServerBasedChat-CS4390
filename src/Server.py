#!/bin/python3
"""
# Description:
Server classes

# Authors:
- Seth Giovanetti
"""

import byteutil
import net
# import socket
import socketserver
import threading

from Codes import Code, printCodes
from pprint import pprint
from prompt import Prompt
from itertools import permutations

import crypto

from Client import BaseClient as Client

# from listener import TCPListener
from listener import UDPListener
from listener import tcpListen


class BaseServer():

    """A basic server with attributes."""

    def __init__(self, server_ip, port_udp, port_tcp):
        # super().__init__()
        self.ip = server_ip
        self.port_udp = port_udp
        self.port_tcp = port_tcp


class RunnableServer(BaseServer):

    """A stateful server with user interaction"""

    # Networking internals

    def run(self):
        self.login_handles = dict()
        self.challenge_handles = dict()

        self.connections_by_id = dict()
        self.clients_by_address = dict()

        print("Starting UDP server on {}:{}".format(self.ip, self.port_udp))
        ss_udp = socketserver.UDPServer(('', self.port_udp), UDPListener)
        ss_udp.callback = self.onUDP
        udp_thread = threading.Thread(daemon=True, target=ss_udp.serve_forever)
        udp_thread.start()

        tcp_welcome_thread = threading.Thread(
            daemon=True, target=self.tcpListen)
        tcp_welcome_thread.start()

        self.prompt()

    def tcpListen(self):
        self.welcome_tcp = net.newTCPSocket()
        self.welcome_tcp.bind((self.ip, 0,))
        self.port_tcp = self.welcome_tcp.getsockname()[1]
        self.welcome_tcp.listen(5)
        print("Starting TCP server on {}:{}".format(self.ip, self.port_tcp))
        while True:
            connection, address = self.welcome_tcp.accept()
            print("Tcp accepted", connection)
            # Client should connect back, so no need to keep track of address here.
            tcp_thread = threading.Thread(
                daemon=True, target=tcpListen, args=(connection, self.onTCP))
            tcp_thread.start()

    def startTCPConnection(self, udp_socket, client, client_address):

        # Configure TCP connection
        # print("Spinning up new TCP socket")
        # try:
        #     client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # except OSError as e:
        #     if e.errno == 98:  # OSErorr 98: Address already in use
        #         existing_client = self.clients_by_address[client_address]
        #         self.disconnectClient(existing_client, client_address)
        #         client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     else:
        #         raise

        # client_tcp.bind(('', self.port_tcp,))
        # client_tcp = client_tcp.accept()
        # # client_tcp.connect(client_address)

        # self.connections_by_id[client.id] = client_tcp

        print("Configuring TCP cookie")
        token = crypto.cRandom()
        self.login_handles[token] = client.id

        net.sendUDP(
            udp_socket,
            byteutil.message2bytes([
                Code.AUTH_SUCCESS,
                token,
                str(self.port_tcp)
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
            self.connections_by_id[client.id] = connection
            self.clients_by_address[client_address] = client
            # Cleanup
            self.login_handles.pop(token)
        else:
            print("Bad login information")
            print("No token")
            print(token)

    def disconnectClient(self, client, client_address):
        client_tcp = self.connections_by_id[client.id]
        print("Closing", client_tcp)

        # TODO: Shut down properly
        # client_tcp.shutdown()
        client_tcp.close()

        print("Unregistering client")
        self.connections_by_id.pop(client.id)
        self.clients_by_address.pop(client_address)

        print("Disconnected client", client_address)

    # Callbacks and reactions

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
            # return
            print("Got TCP DISCONNECT message")
            if client.session_partner:
                net.sendTCP(
                    self.connections_by_id[client.session_partner.id],
                    byteutil.message2bytes([
                        Code.END_NOTIF,
                        b'*',
                    ])
                )
                client.session_partner.session_partner = None
            self.disconnectClient(client, client_address)

        elif code == Code.CHAT.value:
            print("Got TCP CHAT message")
            (message,) = args
            print(message)
            recipient = self.connections_by_id[client.session_partner.id]
            if recipient:
                net.sendTCP(
                    recipient,
                    byteutil.message2bytes([
                        Code.CHAT,
                        message
                    ])
                )
            else:
                net.sendTCP(
                    recipient,
                    byteutil.message2bytes([
                        Code.UNREACHABLE
                    ])
                )

        elif code == Code.CHAT_REQUEST.value:
            """
            If the server determines client-B is connected and not
            already engaged in another chat session, the server sends CHAT_STARTED(session-ID,
            Client-ID-B) to client A, and CHAT_STARTED(session-ID, Client-ID-A) to client B. Client A
            and Client B are now engaged in a chat session and can send chat messages with each
            other, through the server. The clients display “Chat started” to the end user at A and B. If
            client B is not available, the server sends UNREACHABLE (Client-ID-B) to client A
            """
            print("Got chat request")
            (client_id_b,) = args
            print(client.id, "->", client_id_b)

            # Check if client b is connected and availible
            try:
                (client_b,) = [c for (k, c) in self.clients_by_address.items() if c.id == client_id_b and c.availible]
                print(client_b)

                # Create a session
                client.session_partner = client_b
                client_b.session_partner = client
                # Inform clients of results
                for (c1, c2) in permutations([client, client_b]):
                    net.sendTCP(
                        self.connections_by_id[c1.id],
                        byteutil.message2bytes([
                            Code.CHAT_STARTED,
                            b'*',
                            c2.id,
                        ])
                    )

            except ValueError:
                # Client B is not connected
                print(self.clients_by_address.items())
                print("No such client availible")
                net.sendTCP(
                    connection,
                    byteutil.message2bytes([
                        Code.UNREACHABLE
                    ])
                )
                return

        elif code == Code.END_REQUEST.value:
            client_b = client.session_partner
            client.session_partner = None
            client_b.session_partner = None
            for (c1, c2) in permutations([client, client_b]):
                net.sendTCP(
                    self.connections_by_id[c1.id],
                    byteutil.message2bytes([
                        Code.END_NOTIF,
                        b'*',
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

    # Chat server

    # User prompt

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

    def cmd_net(self, *args):
        print("Network status: ")
        print("UDP: \t{}:{}".format(self.ip, self.port_udp))
        print("TCP: \t{}:{}".format(self.ip, self.port_tcp))
        print("Active TCP connections: ")
        for key, sock in self.connections_by_id.items():
            print(key, net.reprTCPSocket(sock), sep="\t")
