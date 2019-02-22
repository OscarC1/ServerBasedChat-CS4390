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

​```mermaid
graph LR;
Client
Server
tcpc(TCP Connection)
Client --> |TCP Socket C| tcpc
Server --> |TCP Socket S| tcpc
tcpc --> |TCP Socket C| Client
tcpc --> |TCP Socket S| Server

```



# Connection to the Server

​```mermaid
sequenceDiagram
participant Client
participant Server
Client->>Server: UDP HELLO
Server->Server: Verify client ID with subscriber list
Server->>Client: UDP CHALLENGE
Client->>Server: UDP RESPONSE
Server->>Client: AUTH_SUCCESS(cookie, port)
Client->Client: CK-A
Client->>Server: TCP CONNECT(cookie, port)
```

# Client A initiates chat session to client B

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

