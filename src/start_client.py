#!/bin/python3
"""Summary
# Description: 
Client module for ServerBasedChat

# Authors:
- Seth Giovanetti


"""

from Client import RunnableClient
from Server import BaseServer

from net import SERVER_IP, SERVER_UDP_PORT

def main():
    server = BaseServer(SERVER_IP, SERVER_UDP_PORT)
    our_client_id = input("ID? > ")
    RunnableClient(our_client_id).run(server)


if __name__ == "__main__":
    main()
