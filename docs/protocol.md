# Protocol

## Transport Layer

`ClassChat` uses `TCP/IP` socket communication over IPv4.

- The server listens on a configured IP address and port.
- Each client creates a TCP socket and connects to the server.
- All communication between clients passes through the server.
- TCP is used because it provides reliable, ordered delivery.

## Communication Model

`ClassChat` uses a central server model.

- Clients do not communicate directly with each other.
- Each client sends JSON messages to the server.
- The server validates the message and either responds to the sender or forwards the message to another client.
- The server keeps a dictionary of connected usernames and their sockets.

## Message Format

Application messages are encoded as `JSON`.

Current implementation sends one JSON object per socket send call. Each message includes a `type` field and may also include `sender`, `receiver`, `text`, or `users` depending on the message.

Example chat message:

```json
{
  "type": "chat",
  "sender": "Alice",
  "receiver": "Bob",
  "text": "Hi, do you know how TCP works?"
}
```

## Message Types

### Client To Server

- `register`: register a username after connecting
- `chat`: send a direct message to another user
- `list`: request the list of connected users
- `disconnect`: close the client connection

### Server To Client

- `ack`: confirms a successful action
- `chat`: forwarded direct message from another user
- `list`: returns the currently connected users
- `error`: indicates invalid input or a routing failure
- `disconnect`: confirms the server is closing the connection

## Message Fields

- `type`: identifies the kind of message
- `sender`: username of the sending client
- `receiver`: username of the intended recipient
- `text`: message content or status text
- `users`: list of connected usernames returned by the server

## Workflow

1. A client connects to the server.
2. The server responds with an `ack` message.
3. The client sends a `register` message with its username.
4. The server validates the username and stores the client socket.
5. The client can then send `chat`, `list`, or `disconnect` messages.
6. For a `chat` message, the server looks up the receiver and forwards the message.
7. If the receiver does not exist or has disconnected, the server sends an `error` message back to the sender.

## Error Handling

The current implementation handles these cases:

- blank username
- duplicate username
- missing receiver or message text
- unknown message type
- recipient not connected
- recipient disconnected before delivery
- malformed or unreadable JSON
- abrupt socket disconnects

## Notes

- The terminal UI still uses slash commands such as `/msg`, `/list`, and `/quit`, but the client translates those commands into JSON before sending them.
- The server is implemented using `threading`, which satisfies the multi-thread server requirement in the project instructions.
