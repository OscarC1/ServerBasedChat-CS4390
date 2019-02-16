# System Overview
<p>End User -&gt; Client -&gt; Server</p>
<p>Client</p>
<ul>
<li>Unique Client-ID</li>
<li>Secret key (provided by server)</li>
</ul>
<p>Server</p>
<ul>
<li>Collection&lt;Client&gt;</li>
</ul>
# Connection to the Server

```mermaid
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

# Protocol

- HELLO(Client-ID)
- CHALLENGE(rand)
- RESPONSE(Client_ID, Res)
- AUTH_SUCCESS(cookie, port_number)
- AUTH_FAIL()
- CONNECT(cookie)
- CONNECTED()
- CHAT_REQUEST(Client-ID)
- CHAT_STARTED(Session-ID, Client-ID)
- UNREACHABLE(Client-ID)
- END_REQUEST(Session-ID)
- END_NOTIF(Session-ID)
- CHAT(Session-ID, message)
- HISTORY_REQ(Client-ID)
- HISTORY_RESP(Client-ID, message)