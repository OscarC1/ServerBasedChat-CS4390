# Lecture Material

### Socket programming with UDP (6)

No "connection" between client and server

- no handshaking before sending data
- sender explicitly attaches IP destination and port # to each packet
- receiver extracts sender IP address and port # from received packet

![1550859345486](../../../Computer%20Networking/ServerBasedChat-CS4390/Doc/assets/1550859345486.png)

![1550859374189](../../../Computer%20Networking/ServerBasedChat-CS4390/Doc/assets/1550859374189.png)

![1550859390867](../../../Computer%20Networking/ServerBasedChat-CS4390/Doc/assets/1550859390867.png)

### Socket Programming with TCP (6)

Client must contact server

- Server process must first be running
- Server must have created socket that welcomes client contact

Client contacts server by

- Creating TCP socket, specifying IP address, port number of server
- Client then establishes connection to server TCP
- When contacted by client, **server TCP creates new socket** for server process to communicate with that particular client
  - Allows server to communicate with multiple client
  - Source port numbers used to distinguish clients

![1550859532041](../../../Computer%20Networking/ServerBasedChat-CS4390/Doc/assets/1550859532041.png)

![1550859655027](assets/1550859655027.png)

![1550859670069](assets/1550859670069.png)

Connection negotiation

Server runs tcpAccept on an existing welcome socket. This creates a new socket on the same port, bound to the client. 

Client runs tcpConnect and connects 

![1551373644542](assets/1551373644542.png)



## Multiplexing (7)

### UDP Demultiplexing

Connectionless

When sending datagram, sender must specify destination IP and port

When host receives UDP segment:

- Host checks destination port # in segment
- Directs UDP segment to socket with that port #
- IP datagrams with same dest, port #, but different source IP and/or source port will be directed to same dest socket.

![1550859968832](assets/1550859968832.png)

## TCP Demultiplexing

Connection-oriented

TCP socket is identified by a 4-tuple: source IP, source port, dest IP, and dest port

Receiver uses all four values to direct segment to the appropriate socket

Server may host many simultaneous TCP sockets

Web servers have different sockets for each connecting client

![1550860065922](assets/1550860065922.png)

![1550860080580](assets/1550860080580.png)

