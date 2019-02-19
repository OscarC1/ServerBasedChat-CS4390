#!/bin/python3
"""
# Description: 
Client classes

# Authors:
- Seth Giovanetti
"""

import crypto


class BaseClient(object):

    """A basic client with attributes"""

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.loadSecret(gen_on_fail=True)

    def loadSecret(self, gen_on_fail=False):
        try:
            self.secret = crypto.getKey(self.id)
            print("Loaded stored key for ID " + self.id)
        except KeyError as e:
            if gen_on_fail:
                self.genSecret()
            else:
                raise

    def genSecret(self):
        new_secret = crypto.cRandom(2048)
        crypto.storeKey(new_secret, self.id)
        print("New key generated for client ID " + self.id)
        self.secret = new_secret


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
