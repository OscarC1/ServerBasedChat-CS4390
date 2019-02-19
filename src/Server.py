#!/bin/python3

import crypto


def getSecret(client_id):
    raise NotImplementedError


class BaseServer(object):

    """A basic server with attributes.

    Currently unused. """

    pass


class RunnableServer(BaseServer):

    """A stateful server with user interaction"""

    def run(self):
        raise NotImplementedError

    def onHello(client_id):
        """
                Upon receiving HELLO (Client-ID-A), the server looks up Client A’s secret key K_A.
                Then it generates a random number rand. Rand and K_A are input into an authentication algorithm A3.
                The output, XRES, is stored by the server. Then the server sends rand in the CHALLENGE (rand).
                Client A is expected to run the same algorithm A3 with the same inputs rand and K_A, and produce RES, which is sent to the server in the RESPONSE (Res) message.
                If RES matches XRES, the server has authenticated the client.
                """
        client_secret = getSecret(client_id)
        rand = crypto.cRandom()
