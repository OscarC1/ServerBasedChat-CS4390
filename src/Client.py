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

from Codes import Code, printCodes
from pprint import pprint
import prompt
# import socketserver
from listener import tcpListen
import threading


def formatChatMessage(id, msg, id2=""):
    return "{ident:>{size}} {msg}".format(
        size=max(len(id), len(id2)),
        ident="[{id}]".format(id=id),
        msg=(msg if msg and msg[-1] != "\n" else msg[:-1])
    )


class BaseClient():

    """A basic client with attributes

    Attributes:
        id (str): Unique client ID
    """

    def __init__(self, id):
        self.id = id
        self._secret = None
        self.address = tuple()
        self.session_partner = None
        self.session_id = None

    @property
    def availible(self):
        return self.session_partner is None

    @property
    def secret(self):
        """
        Returns:
            str: The client's secret key, if we know it. 
        """
        if self._secret is None:
            self.loadSecret()
        return self._secret

    def loadSecret(self, gen_on_fail=False):
        """Load our stored secret key from crypto

        Args:
            gen_on_fail (bool, optional): Generate and save a new key if we don't already have one stored.

        Raises:
            KeyError: We can't generate a new key, and we don't have one stored.
        """
        try:
            self._secret = crypto.getKey(self.id)
            print("Loaded stored key for ID " + self.id)
        except KeyError as e:
            if gen_on_fail:
                self.genSecret()
            else:
                raise e

    def genSecret(self):
        """Generate a new secret key and store it in crypto
        """
        new_secret = crypto.cRandom(128)
        crypto.storeKey(new_secret, self.id)
        print("New key generated for client ID " + self.id)
        self._secret = new_secret


class RunnableClient(BaseClient):

    """A stateful client with user interaction

    Attributes:
        server (Server): A BaseServer to connect our client to
        server_tcp_port (int): The port number of our TCP connection
        tcp_socket (Socket): The TCP socket cooresponding to the TCP connection with the server
        token (str): Session token for authentication
    """

    # def __init__(self, id):
    #     prompt.Interactable.__init__(self, start=False)
    #     # super().__init__(self)
    #     BaseClient.__init__(self, id)

    # Connect, login, run

    def run(self, server):
        """Run client interactively.
        Load our secret, generating if needed.
        Login, run prompt until user exits, then disconnect.

        Args:
            server (BaseServer): BaseServer to connect our client to
        """
        self.loadSecret(gen_on_fail=True)
        self.login(server)
        self.prompt()
        self.disconnect()

    def sendTCP(self, message):
        assert self.tcp_socket
        return net.sendTCP(
            self.tcp_socket,
            byteutil.message2bytes(message)
        )

    def login(self, server):
        """Attempt to login to the server and establish a TCP connection.
        This is the UDP handshake process.

        Args:
            server (BaseServer): Server target

        Raises:
            PermissionError: Authentication failure
        """
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
        response, serv_address_udp = net.awaitUDP(sock, net.UDP_MSG_SIZE)
        code, rand = byteutil.bytes2message(response)

        assert code == Code.CHALLENGE.value, "Got non-challenge code {}".format(
            code)

        print("Challenge rand:", rand)

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
        response, serv_address_udp = net.awaitUDP(sock, net.UDP_MSG_SIZE)
        # rest includes raw int data here, don't stringify
        code, *rest = byteutil.bytes2bytemsg(response)

        if code == Code.AUTH_FAIL.value:
            raise PermissionError(
                "Server rejected key authentication with code", code)

        assert code == Code.AUTH_SUCCESS.value, "Got non-auth code {}".format(
            code)
        (token, server_tcp_port) = rest

        print("Closing UDP socket")
        sock.close()

        # Establish TCP Connection
        print("Establishing TCP connection with cookie")
        self.token = token

        # Create a TCP address with our old IP and our new port
        (server_ip, udp_port) = serv_address_udp
        serv_address_tcp = (server_ip, int(server_tcp_port))

        # print("Starting up TCP listener")
        # self.tcp_server = socketserver.TCPServer(src_address, TCPListener)
        # self.tcp_server.master = self
        # self.tcp_thread = threading.Thread(daemon=True, target=self.tcp_server.serve_forever)
        # self.tcp_thread.start()

        print("Connecting TCP socket", serv_address_tcp)
        # self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # serv_address_tcp = (server_ip, self.server_tcp_port)
        # self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_socket = net.newTCPSocket()
            self.tcp_socket.connect(serv_address_tcp)
        except ConnectionRefusedError as e:
            print("Could not connect!")
            print(serv_address_tcp)
            raise

        self.sendTCP([
            Code.CONNECT,
            token
        ])
        # Expect CONNECTED

        message = net.awaitTCP(self.tcp_socket, 2**16)
        code, *rest = byteutil.bytes2message(message)
        assert code == Code.CONNECTED.value, "Got non-connect code {}".format(
            code)

        print("Logged in successfully.")

        def _listenUntilExit():
            tcpListen(self.tcp_socket, self.onTCP)
            self.disconnect(None)

        tcp_thread = threading.Thread(
            daemon=True, target=_listenUntilExit)
        tcp_thread.start()

    def disconnect(self, *args):
        """Disconnect from server and exit

        Args:
            *args: None

        Raises:
            KeyboardInterrupt: Disconnect signal
        """
        self.sendTCP([
            Code.DISCONNECT
        ])
        self.p.cmd_exit(None)
        raise KeyboardInterrupt

    # TCP networking

    # def tcpListener(self, sock, callback):
    #     """Listen for TCP messages on a socket and pass messages to a callback function.
    #     This is a blocking call in an infinite loop; run this in a thread.

    #     Args:
    #         sock (socket): TCP socket to listen
    #         callback (func): Callback function with args (socket, code, args, source_address,)
    #     """
    #     # self.listening = threading.Event()
    #     sock.settimeout(None)
    #     while True:
    #         message = sock.recv(net.MSG_SIZE)
    #         assert message

    #         source_address = sock.getpeername()

    #         print("┌ Recieved TCP message")
    #         print("│ Source: {}:{}".format(*source_address))
    #         print("│ ┌Message (bytes): {}".format(message))
    #         print("└ └Message (print): {}".format(
    #             byteutil.formatBytesMessage(message)))

    #         code, *rest = byteutil.bytes2message(message)
    #         callback(sock, code, rest, source_address)

    def onTCP(self, connection, code, args, source_address):
        """Callback to handle TCP messages

        Args:
            connection (socket): TCP socket of incomming message
            code (Code): The protocol code of the message
            args (list): The non-code parts of the message
            source_address (ip, port): INET address of the message source
        """
        #print("args"+ " ".join(str(x) for x in args));

        if code == Code.CHAT_STARTED.value:
            (sessid, clientid,) = args
            self.session_partner = clientid
            self.session_id = sessid

            print("Chat started with user", clientid)

            # try:
            #     self.ps.app.exit()
            # except AssertionError:
            #     pass
            # print('Exited.')
            # self.promptChat()

        elif code == Code.END_NOTIF.value:
            (sessid,) = args
            self.session_partner = None
            self.session_id = None

            print("Chat terminated.")

            # self.p.pstr = "> ".format(self.id)

            # self.ps.app.exit()
            # self.prompt()

        elif code == Code.UNREACHABLE.value:
            print("Cannot connect.")
        elif code == Code.CHAT.value:
            (message,) = args
            print(formatChatMessage(self.session_partner, message, self.id))
        elif code == Code.HISTORY_RESP.value:
            # print("client got args" + repr(args))
            (client_id_b, message, *rest) = args
            # print("msg only: "+ message)
            # print("msg split: " + messagef)
            # print("final hist msg: " + formatChatMessage(client_id_b, message))
            print(formatChatMessage(client_id_b, message))
        else:
            print("No behavior for TCP code", code)

    def onChatInput(self, inp):
        if inp.lower() == "end chat":
            self.sendTCP([
                Code.END_REQUEST
            ])
        elif inp:
            self.sendTCP([
                Code.CHAT,
                inp
            ])
            print(formatChatMessage(self.id, inp, self.session_partner))
    # User interactivity

    def bottomToolbar(self):
        if self.session_partner:
            return "[{}] Chatting with user '{}'. Send 'end chat' to disconnect.".format(self.id, self.session_partner)
        else:
            return "[{}] Type 'help' for help. 'chat [user]' to initiate chat.".format(self.id)

    def prompt(self):
        """Interactive prompt
        """
        from prompt_toolkit import PromptSession
        # from prompt_toolkit.completion import WordCompleter
        from prompt_toolkit.patch_stdout import patch_stdout
        
        self.p = p = prompt.Prompt()
        p.pstr = "{} > ".format(self.id)
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
        p.registerCommand(
            "disconnect",
            self.disconnect,
            helpstr="Disconnect session"
        )

        # prompt_completer = WordCompleter(self.p.commands.keys())
        self.ps = PromptSession(
            # completer=prompt_completer,
            # reserve_space_for_menu=3,
            bottom_toolbar=self.bottomToolbar,
            erase_when_done=True
        )
        # self.prompt_event = threading.Event()

        # We implement our own prompt system that differentiates between
        # chat input and command input. 
        try:
            while True:
                with patch_stdout():
                    rawin = self.ps.prompt(self.p.pstr)  # prompt(self.pstr)
                    try:
                        if self.session_partner:
                            self.onChatInput(rawin)
                        else:
                            self.p.handleCommand(rawin)
                    except BrokenPipeError as e:
                        self.login(self.server)
        except (KeyboardInterrupt, EOFError) as e:
            # Catch Ctrl-C, Ctrl-D, and exit.
            print("User interrupt.")
        finally:
            # Cleanup
            pass

    # def promptChat(self):
    #     """Interactive prompt
    #     """
    #     from prompt_toolkit import PromptSession
    #     from prompt_toolkit.patch_stdout import patch_stdout
        
    #     self.ps = PromptSession(
    #         bottom_toolbar=self.bottomToolbar
    #     )
    #     try:
    #         while True:
    #             with patch_stdout():
    #                 rawin = self.ps.prompt(self.p.pstr)  # prompt(self.pstr)
    #                 self.onChatInput(rawin)
    #     except (KeyboardInterrupt, EOFError) as e:
    #         # Catch Ctrl-C, Ctrl-D, and exit.
    #         print("User interrupt.")
    #     finally:
    #         # Cleanup
    #         pass

    def cmd_say(self, *args):
        """Send a CHAT message

        Args:
            Message
        """
        print("tcp say:", args)
        self.sendTCP([
            Code.CHAT,
            " ".join(args)
        ])

    def cmd_history(self, *args):
        """Request chat history between you and another user.
        Args:
            Other user id
        """
        if len(args) == 0:
            print("History: No user specified.")
            return
        (client_id_b,) = args
        print("History for " + client_id_b + ": \n")
        self.sendTCP([
            Code.HISTORY_REQ,
            client_id_b
        ])


    def cmd_chat(self, *args):
        """Start a chat session with another user.

        Args: client-id
        """
        (client_id_b,) = args
        self.sendTCP([
            Code.CHAT_REQUEST,
            client_id_b
        ])

    def cmd_panic(self, *args):
        """
        Terminate without cleaning up.
        """
        import os
        os.abort()
