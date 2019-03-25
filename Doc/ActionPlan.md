# Action Plan

Goal: Server-based chat program

Start Date: 2019-02-01

Team Members:

| Name            | NetID     | Initials |
| --------------- | --------- | -------- |
| Seth Giovanetti | stg160130 | SG       |
| Oscar Contreras | oxc160030 | OC       |
| Brennan Stuewe  | brs140230 | BS       |

## Table

(Derived from gantt charts, see below)

| No   | Action                             | Responsible            | Deadline   | Resources Needed | Dependencies | Result                                                  | Completed | Issues                                                       |
| ---- | ---------------------------------- | ---------------------- | ---------- | ---------------- | ------------ | ------------------------------------------------------- | --------- | ------------------------------------------------------------ |
| 1    | Action Plan                        | SG, OC                 | 2019-02-26 | GitHub           | None         | Get idea of how tasks will be divided                   | :ballot_box_with_check: | Most of team is less experienced in Python - members will need to use resources to become familiar. |
| 2    | UDP Transport and Protocol         | SG             |            | IDE              | None         | Messages for login / initiation of connections done     | :ballot_box_with_check: |                                                              |
| 3    | Authentication and CK-A Encryption | SG             |            | IDE              | 2            | Clients can be authenticated; messages can be encrypted | :ballot_box_with_check: |                                                              |
| 4    | TCP Tunneling                      | SG, OC |            | IDE              | 2,3          | Ready to implement client-client messaging              | :ballot_box_with_check: |                                                              |
| 5    | Chat sessions                      | SG                     |            |                  |              |                                                         | :ballot_box_with_check: |                                                              |
| 6    | Client Prompt and Messaging        | SG                     |            | IDE              | 2,3,4        | Chat between clients can be performed                   | :ballot_box_with_check: |                                                              |
| 7    | Server Session Handling            | SG                     |            | IDE              | 2,3,4,5      | Functional chat in place                                | :ballot_box_with_check: |                                                              |
| 8    | History Storage and Retrieval      | OC, BS                 |            | IDE              | 2,3,4,5,6    | Chat history retrievable by clients                     |           |                                                              |
| 9    | Polished Client UI                 | SG                     |            | IDE              | 2,3,4,5,6,7  | Implementation of chat program done                     |           |                                                              |
## Notes

Tam Nguyen has opted not to contribute to the group project and build a standalone network program for his own education.

## Deadlines

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


Optimized/Real scenerio:

```mermaid
gantt
section General
Action Plan			:done,	actplan,	2019-02-19,	6d
section Networking
CK-A Encryption		:done,	cka, 2019-02-26, 7d
UDP transport		:done,	udp, after cka, 5d
TCP Tunnel			:done,	tcp, after cka, 7d
Chat sessions		:done	chat, after tcp, 7d
section Client
Client prompt		:done,   prompt, 2019-02-26, 5d
UI polish			:active	ui, after prompt, 4d
section Server
Session handling	:done	session, after tcp, 10d
History				:active	history, after session,	5d
```

(Last updated: 2019-03-13)

Final product ready 2019-04-14



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

