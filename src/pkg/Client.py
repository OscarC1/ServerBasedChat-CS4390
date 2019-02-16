#!/bin/python3


class BaseClient(object):

    """A basic client with attributes"""

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.secret_key = None

    def setKey(self, secret_key):
        self.secret_key = secret_key

    def generateKey(self):
        raise NotImplementedError


class RunnableClient(BaseClient):

    """A stateful client with user interaction"""

    def run(self, server_ip):
        self.login(server_ip)
        self.prompt()

    def login(self, server_ip):
        raise NotImplementedError

    def prompt(self):
        """Interactive prompt
        """
        while True:
            user_input = input("> ")
            print(user_input)
