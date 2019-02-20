#!/bin/python3
"""Summary
# Description: 
Server module for ServerBasedChat

# Authors:
- Seth Giovanetti


"""


from net import SERVER_IP, SERVER_UDP_PORT
from Server import RunnableServer


def main():
    RunnableServer(SERVER_IP, SERVER_UDP_PORT).run()


if __name__ == "__main__":
    main()
