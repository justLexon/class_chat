# Architecture

## Project Structure

```text
classChat/
|-- docs/
|-- src/
|   `-- classchat/
|       |-- client/
|       |-- gui/
|       `-- server/
|-- technical_report_and_screenshots/
|   |-- section_1/
|   |-- section_2/
|   |-- section_3/
|   |-- section_4/
|   |-- section_5/
|   `-- technical_report.md
|-- .gitignore
`-- README.md
```

## Folder Responsibilities

- `docs/`: architecture notes, protocol documentation, and the project instructions PDF.
- `src/`: main application source code.
- `src/classchat/client/`: client networking, user input, and incoming message display.
- `src/classchat/gui/`: Tkinter GUI client and launcher GUI.
- `src/classchat/server/`: server networking, client registration, and message forwarding.
- `technical_report_and_screenshots/`: screenshots for project sections and the technical report.

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
- The project now includes both a GUI client and a launcher GUI in addition to the console client.
