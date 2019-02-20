#!/bin/python3
"""Summary
# Description: 
Client module for ServerBasedChat

# Authors:
- Seth Giovanetti


"""

from Client import RunnableClient
from Server import BaseServer

SERVER_IP = "192.168.1.1"
SERVER_UDP_LISTEN = 64


def main():
    server = BaseServer(SERVER_IP, SERVER_UDP_LISTEN)
    our_client_id = input("ID? > ")
    RunnableClient(our_client_id).run(server)


if __name__ == "__main__":
    main()
