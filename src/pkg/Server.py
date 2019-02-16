#!/bin/python3


class BaseServer(object):

    """A basic server with attributes. 

    Currently unused. """

    pass


class RunnableServer(BaseServer):

    """A stateful server with user interaction"""

    def run(self):
        raise NotImplementedError
