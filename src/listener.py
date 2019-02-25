import byteutil
import socketserver


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
        master = self.server.master

        message = request[0]
        print(request)
        print(client_address)

        print("┌ Recieved UDP message")
        print("│ Source: {}:{}".format(*client_address))
        print("│ ┌Message (bytes): '{}'".format(message))
        print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

        code, *rest = byteutil.bytes2message(message)
        master.onUDP(connection, code, rest, client_address)


class TCPListener(socketserver.BaseRequestHandler):
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
        message = self.request.recv(2**16)

        print(request)
        print(client_address)

        print("┌ Recieved TCP message")
        print("│ Source: {}:{}".format(*client_address))
        print("│ ┌Message (bytes): '{}'".format(message))
        print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

        code, *rest = byteutil.bytes2message(message)
        master.onTCP(request, code, rest)
