import byteutil
import socketserver
from net import MSG_SIZE


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

        message = request[0]
        print(request)
        print(client_address)

        print("┌ Recieved UDP message")
        print("│ Source: {}:{}".format(*client_address))
        print("│ ┌Message (bytes): '{}'".format(message))
        print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

        code, *rest = byteutil.bytes2message(message)
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
        message = sock.recv(MSG_SIZE)
        assert message

        source_address = sock.getpeername()

        print("┌ Recieved TCP message")
        print("│ Source: {}:{}".format(*source_address))
        print("│ ┌Message (bytes): {}".format(message))
        print("└ └Message (print): {}".format(
            byteutil.formatBytesMessage(message)))

        code, *rest = byteutil.bytes2message(message)
        callback(sock, code, rest, source_address)
