# Protocol

## Transport Layer

The `ClassChat` system uses `TCP/IP` socket communication.

- The server listens on a configured IP address and port.
- Each client creates a TCP socket and connects to the server.
- All communication between clients passes through the server.
- TCP is used because it provides reliable, ordered delivery of data.

## Communication Model

`ClassChat` uses a central server model.

- Clients do not communicate directly with each other.
- A client sends messages to the server.
- The server validates the message and forwards it to the intended receiver.
- The server is responsible for tracking connected users.

## Message Format

Application messages are encoded as `JSON`.

Each message should contain the information needed for the server to understand the request and route it correctly. Since TCP is a byte-stream protocol, messages should be clearly delimited during implementation. A simple approach is to send one JSON message per line.

Example:

```json
{
  "type": "chat",
  "sender": "Alice",
  "receiver": "Bob",
  "text": "Hi, do you know how TCP works?",
  "timestamp": "2026-04-09T14:00:00Z"
}
```

## Message Fields

- `type`: identifies what kind of message is being sent.
- `sender`: the username of the client sending the message.
- `receiver`: the username of the intended recipient.
- `text`: the message body.
- `status`: used by the server in responses such as success or error.
- `timestamp`: the time the message was created or sent.

## Message Types

The core message types for the project are:

- `register`: sent by a client when joining the system.
- `ack`: sent by the server to confirm a connection or successful action.
- `chat`: a direct message from one client to another.
- `error`: sent by the server when a request cannot be completed.
- `disconnect`: sent when a client leaves the system.

Optional message types for advanced or bonus features:

- `user_list`: returns a list of connected users.
- `group_chat`: sends a message to a group.
- `file_transfer`: supports file sending between clients.
- `offline_message`: stores and delivers messages for offline users.
- `secure_key_exchange`: used for encryption or session-key setup.

## Connection Workflow

The expected communication flow is:

1. A client creates a TCP socket and connects to the server.
2. The server accepts the connection and sends an acknowledgment.
3. The client sends a `register` message containing its username.
4. The server stores the client connection in its active client list.
5. The client sends `chat` messages addressed to another user.
6. The server checks whether the receiver exists.
7. If the receiver exists, the server forwards the message.
8. If the receiver does not exist, the server returns an `error` message.

## Error Handling

The server should handle invalid or unexpected situations safely.

Examples include:

- the username is already in use
- the receiver is not connected
- the JSON message is malformed
- required message fields are missing
- the client disconnects unexpectedly
- an empty message is received

## Design Notes

- TCP/IP satisfies the project requirement for socket-based client-server communication.
- JSON keeps the protocol simple, readable, and easy to debug.
- A shared message format should be used by both the client and server so routing logic stays consistent.
- The protocol should be implemented in a way that makes it easy to extend later for bonus features such as group chat, offline messaging, file transfer, and encryption.
