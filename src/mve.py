import socket
import prompt
import threading


class Mve(prompt.Interactable):
    """docstring for Mve"""

    def __init__(self):
        super(Mve, self).__init__(start=False)
        self.socket = socket.socket()
        print("Opened TCP socket on", self.socket.getsockname())
        self.target_port = None

    def cmd_bind(self, *args):
        self.socket = socket.socket()
        self.socket.bind(('localhost', 0,))
        print("Hosting TCP on address", self.socket.getsockname())
        return self.socket

    def cmd_send(self, *args):
        self.socket.sendall(" ".join(args).encode('utf-8'))

    def cmd_await(self, *args):
        """
        Listen for connections. It's
        a whole thing.
        """
        def listen():
            connectionSocket, addr = self.socket.accept()
            while True:
                message = connectionSocket.recv(1024)
                if message:
                    print(message.decode('utf-8'))
        self.socket.listen(5)
        threading.Thread(target=listen).start()

    def cmd_connect(self, *args):
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
