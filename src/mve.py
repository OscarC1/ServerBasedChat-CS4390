import socket
import prompt
import threading
from sys import byteorder


class Mve(prompt.Interactable):
    """docstring for Mve"""

    def __init__(self):
        super(Mve, self).__init__(start=False)
        self.socket = socket.socket()
        print("Opened TCP socket on", self.socket.getsockname())
        self.target_port = None

    def cmd_bind(self, *args):
        """Create socket, bind. """
        self.socket = socket.socket()
        self.socket.bind(('localhost', 0,))
        print("Hosting TCP on address", self.socket.getsockname())
        ip, port = self.socket.getsockname()
        print(port, type(port))
        with open("port", "wb") as portfile:
            portfile.write(port.to_bytes(8, byteorder))
        return self.socket

    def cmd_send(self, *args):
        """Send a message along socket."""
        self.socket.sendall(" ".join(args).encode('utf-8'))

    def cmd_await(self, *args):
        """
        Listen for connections. Threaded.
        """
        def listen():
            connectionSocket, addr = self.socket.accept()
            while True:
                message = connectionSocket.recv(8)
                if message:
                    print(message.decode('utf-8'))
                else:
                    break
        self.socket.listen(2)
        threading.Thread(target=listen).start()

    def cmd_autocon(self, *args):
        """Automatically connect to a port"""
        with open("port", "rb") as portfile:
            portno = int.from_bytes(portfile.read(), byteorder)
        self.cmd_connect(portno)

    def cmd_connect(self, *args):
        """Connect to host at port PORT"""
        (self.target_port,) = args
        print("Connecting to port", self.target_port)
        self.socket.connect(('localhost', int(self.target_port),))
        print("Connected to TCP socket", self.socket.getpeername())

    def cmd_vars(self, *args):
        print(vars(self))


def interactive():
    Mve().prompt()


def runner():
    from time import sleep

    server = Mve()
    client = Mve()

    server.cmd_bind()
    server.cmd_await()

    client.cmd_connect(server.socket.getsockname()[1])
    client.cmd_send("Message 1A\n")
    client.cmd_send("Message 1B\n")
    client.cmd_send("Message 1C\n")

    sleep(1)

    print("Server:", server.socket)
    print("Client:", client.socket)

    # server.cmd_send("Message 2A\n")
    server.cmd_connect(client.socket.getsockname()[1])
    server.cmd_send("Message 2B\n")



if __name__ == "__main__":
    # runner()
    interactive()
