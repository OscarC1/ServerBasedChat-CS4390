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





