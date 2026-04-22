# Plan

## Finish Section 1 cleanly
- make the current server and client persistent
- keep the connection open until the user exits with /quit
- Stabilize the single-client version
- confirm repeated send/receive works
- handle clean disconnects
- avoid crashing on empty input or closed sockets

## Move into Section 2
- let the client send and receive without the whole program feeling single-step
- likely use threading for input and receiving, or select if you want to stay closer to the instruction hint
## Move into Section 3
- make the server handle multiple clients at the same time
- usually this means a loop around accept() plus one thread per client
## Move into Section 4
- add usernames
- track connected clients
- forward messages from one client to another
- handle “recipient not found” cleanly
- Leave GUI until after console networking works
- GUI is optional early