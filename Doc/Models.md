# System Overview
End User -> Client -> Server

Client
- Unique Client-ID
- Secret key

Server
- Collection of Clients

# Network

## UDP

```mermaid
graph LR;
Client
Server
tcpc(TCP Connection)
Client --> |TCP Socket C| tcpc
Server --> |TCP Socket S| tcpc
tcpc --> |TCP Socket C| Client
tcpc --> |TCP Socket S| Server
```

## TCP

Server has a Listening Socket (TCP/UDP???)

Server has a set of TCP sockets, all on the same TCP port.

Server and client negotiate a TCP Connection



Server creates a socketserver and serves forever on a thread

Client creates a TCP socket and CONNECTS to the server address



Client A initiates chat session to client B

```mermaid
sequenceDiagram
A->>Server: CHAT_REQUEST(Client-ID-B)
alt B not availible
Server->>A: UNREACHABLE
end
Server->>A: CHAT_STARTED(session-ID, Client-ID-B)
Server->>B: CHAT_STARTED(session-ID, Client-ID-A)
```

# Chat termination

```mermaid
sequenceDiagram
C->>Server: END_REQUEST(session-ID)
Server->>C: END_NOTIF(session-ID)
Server->>D: CHAT_STARTED(session-ID)
```

# Security

Only clients are authenticated, based on challenge-response.

Server and client run concurrent A8 algorithm

No integrity protection

# History

