# Architecture

## Project Structure

```text
classChat/
|-- docs/
|-- project_instructions/
|-- scripts/
|-- src/
|   `-- classchat/
|       |-- client/
|       |-- libs/
|       |-- security/
|       `-- server/
|-- technical_report_and_screenshots/
|   |-- section_one/
|   `-- section_two/
|-- tests/
|-- .gitignore
`-- README.md
```

## Folder Responsibilities

- `docs/`: architecture notes, protocol documentation, and planning/progress notes.
- `project_instructions/`: original project instructions in PDF and Markdown form.
- `scripts/`: helper scripts for running demos or future automation.
- `src/`: main application source code.
- `src/classchat/client/`: client networking, user input, and incoming message display.
- `src/classchat/server/`: server networking, client registration, and message forwarding.
- `src/classchat/libs/`: shared helpers if common logic is factored out later.
- `src/classchat/security/`: reserved for optional encryption or security features.
- `technical_report_and_screenshots/`: screenshots and report artifacts organized by section.
- `tests/`: future test cases for client, server, and protocol behavior.

## High-Level Design

- Clients connect to a central TCP server.
- After connecting, each client registers a username.
- The server stores connected usernames in a shared dictionary protected by a lock.
- Each client connection is handled in its own thread.
- Clients send JSON messages to the server.
- The server validates and forwards direct messages to the intended recipient.

## Current Implementation Notes

- The client terminal still uses slash commands for ease of use.
- The client translates those commands into JSON before sending them.
- The server currently supports direct messaging and connected-user listing.
- GUI work has not been started because the console implementation is being completed first.
