#!/bin/python3
"""
# Description:
Abstract network listeners

# Authors:
- Seth Giovanetti
- Oscar Contreras
"""

import byteutil
import socketserver
from net import MSG_SIZE, reprTCPSocket, SHOW_NET_INFO


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
        connection = self.server.socket
        callback = self.server.callback

        bytesin = request[0]

        # For the sake of internal consistancy, we are treating
        # UDP messages like they might contain multiple messages,
        # like TCP.

        for message in byteutil.bytes2messages(bytesin):
            print(request)
            print(client_address)

            if SHOW_NET_INFO:
                print("┌ Recieved UDP message")
                print("│ Source: {}:{}".format(*client_address))
                # print("│ ┌Message (bytes): '{}'".format(message))
                # print("└ └Message: {}".format(byteutil.formatBytesMessage(message)))
                print("└ Message: {}".format(message))

            code, *rest = message  # byteutil.bytes2message(message)
            callback(connection, code, rest, client_address)


class TCPListener(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        # Use standard listener
        tcpListen(self.request, self.server.callback)

        # while True:
        #     client_address = self.client_address
        #     request = self.request
        #     callback = self.server.callback
        #     message = self.request.recv(2**16)

        #     assert message != 0

        #     print(request)
        #     print(client_address)

        #     print("┌ Recieved TCP message")
        #     print("│ Source: {}:{}".format(*client_address))
        #     print("│ ┌Message (bytes): '{}'".format(message))
        #     print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

        #     code, *rest = byteutil.bytes2message(message)
        #     callback(request, code, rest, client_address)


def tcpListen(sock, callback):
    """Listen for TCP messages on a socket and pass messages to a callback function.
    This is a blocking call in an infinite loop; run this in a thread.

    Args:
        sock (socket): TCP socket to listen
        callback (func): Callback function with args (socket, code, args, source_address,)
    """
    # self.listening = threading.Event()
    sock.settimeout(None)
    while True:
        try:
            bytesin = sock.recv(MSG_SIZE)
            # print("listener got bytesin " + repr(bytesin))
            if not bytesin:
                print("Detected null bytesin")
                print("Closing socket on", reprTCPSocket(sock))
                return

            source_address = sock.getpeername()

            # code, *rest = byteutil.bytes2message(bytesin)
            # callback(sock, code, rest, source_address)
            for message in byteutil.bytes2messages(bytesin):

                if SHOW_NET_INFO:
                    print("┌ Recieved TCP message")
                    print("│ Source: {}:{}".format(*source_address))
                    # print("│ ┌message (bytes): {}".format(message))
                    # print("└ └message (print): {}".format(
                    #     byteutil.formatBytesMessage(message)))
                    print("└ Message: {}".format(message))

                code, *rest = message
                callback(sock, code, rest, source_address)

        except OSError as e:
            if e.errno == 9:  # Bad file descriptor
                return
            else:
                raise
