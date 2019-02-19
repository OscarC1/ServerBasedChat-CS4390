# Action Plan

2019-02-26: Action plan due

2019-03-12: Status report due

2019-04-23: Status report due

2019-04-29: Final submission due

### Components

- Action plan
- UDP transport and UDP protocol codes
- CK-A Encryption (and challenge/response)
- TCP tunneling
- Client prompt and messaging (interactivity)
- Server session handling (messaging, overhead, activity timer, etc)
- History storage and retrieval
- Clean up client UI



Worst case scenerio: 7d per component, minimal parallelism:

```mermaid
gantt
section General
Action Plan			:active,	actplan,	2019-02-19,	6d
section Networking
CK-A Encryption		:	cka, 2019-02-26, 7d
UDP transport		:	udp, after cka, 7d
TCP Tunnel			:	tcp, after udp, 7d
section Client
Client prompt		:   prompt, after tcp, 7d
UI					:	ui, after prompt, 7d
section Server
Session handling	:	session, after prompt, 7d
History				:	history, after session,	7d
```

Final product ready 2019-04-14



Optimized/Real scenerio:

```mermaid
gantt
section General
Action Plan			:active,	actplan,	2019-02-19,	6d
section Networking
CK-A Encryption		:	cka, 2019-02-26, 7d
UDP transport		:	udp, after cka, 5d
TCP Tunnel			:	tcp, after cka, 7d
section Client
Client prompt		:   prompt, 2019-02-26, 5d
UI polish			:	ui, after prompt, 4d
section Server
Session handling	:	session, after tcp, 10d
History				:	history, after session,	5d
```

Final product ready 2019-04-14