#!/bin/python3
"""Summary
# Description: 
Client module for ServerBasedChat

# Authors:
- Seth Giovanetti


"""

from types.Client import RunnableClient

SERVER_IP = "192.168.1.1"


def main():
    our_client_id = input("ID? > ")
    RunnableClient(our_client_id).run(SERVER_IP)


if __name__ == "__main__":
    main()
