# Architecture

## Project Structure

```text
classChat/
├─ docs/
├─ project_instructions/
├─ scripts/
├─ src/
│  └─ classchat/
│     ├─ client/
│     ├─ libs/
│     ├─ security/
│     └─ server/
├─ technical_report_and_screenshots/
│  ├─ section_one/
│  └─ section_two/
├─ tests/
├─ .gitignore
└─ README.md
```

## Folder Responsibilities

- `docs/`: project documentation such as architecture notes and the message protocol.
- `project_instructions/`: the original assignment PDF and its Markdown text version.
- `scripts/`: helper scripts for running demos or starting the client and server.
- `src/`: the main application source code.
- `src/classchat/client/`: client-side code for connecting to the server, sending messages, and receiving messages.
- `src/classchat/server/`: server-side code for accepting connections, managing clients, and forwarding messages.
- `src/classchat/libs/`: shared utilities, common models, constants, or protocol helpers used across the project.
- `src/classchat/security/`: optional security-related code such as encryption or key handling for bonus features.
- `technical_report_and_screenshots/`: report materials and screenshots organized by project section.
- `tests/`: test cases for protocol handling, networking behavior, and core logic.

## High-Level Design

- Clients connect to the server over TCP.
- Messages are exchanged using a shared JSON-based format.
- The server keeps track of connected clients and routes messages to the correct receiver.
- Shared logic should stay in `src/classchat/libs/` so both client and server use the same message structure and helper code.
