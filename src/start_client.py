#!/bin/python3
"""Summary
# Description: 
Client module for ServerBasedChat

# Authors:
- Seth Giovanetti


"""

from Client import RunnableClient
from Server import BaseServer

from net import SERVER_IP, SERVER_UDP_PORT, SERVER_TCP_PORT

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--id")
    args = parser.parse_args()
    
    server = BaseServer(SERVER_IP, SERVER_UDP_PORT, SERVER_TCP_PORT)
    if args.id:
        our_client_id = args.id
    else:
        our_client_id = input("ID? > ")
    RunnableClient(our_client_id).run(server)


if __name__ == "__main__":
    main()
