# ClassChat

`ClassChat` is a Python TCP/IP chat system built for the CMPS 413 semester project. It supports multiple clients, username registration, direct messaging through a central server, and both console and Tkinter GUI clients.

## Features

- TCP/IP client-server communication
- persistent client sessions
- multi-client server using `threading`
- username registration and connected-user tracking
- direct client-to-client messaging through the server
- connected user list
- JSON-based communication protocol
- console client
- Tkinter GUI client
- Tkinter launcher GUI for starting the server and opening client windows

## Requirements

- Python 3

No third-party packages are required for the current implementation.

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

## Run Options

You can run the project either with the console client or with the GUI.

### Option 1: GUI Launcher

Start the launcher:

```powershell
py src/classchat/gui/launcher_gui.py
```

From the launcher:

- click `Start Server` once
- click `Open Client` to open one or more GUI client windows

### Option 2: Manual Server + Console Client

Start the server:

```powershell
py src/classchat/server/server.py
```

Start a console client in another terminal:

```powershell
py src/classchat/client/client.py
```

Start additional clients in additional terminals the same way.

### Option 3: Manual Server + GUI Client

Start the server:

```powershell
py src/classchat/server/server.py
```

Start a GUI client:

```powershell
py src/classchat/gui/client_gui.py
```

Open additional GUI client windows the same way.

## Console Client Commands

- `/msg username your_message`: send a direct message to another connected user
- `/list`: show currently connected users
- `/quit`: disconnect from the server

## GUI Client Usage

1. Enter a username.
2. Click `Connect`.
3. Click `Refresh Users` to load connected usernames.
4. Select a username from the user list or type one in the recipient field.
5. Enter a message.
6. Click `Send Message`.
7. Click `Disconnect` when finished.

## Typical Demo Flow

1. Start the server or launcher.
2. Open two or more clients.
3. Register different usernames.
4. Confirm the connected user list appears correctly.
5. Send a message from one user to another.
6. Verify the receiving client displays the forwarded message.
7. Disconnect a client and verify the system handles it cleanly.

## Current Implementation Notes

- The server is the central routing point for all communication.
- Clients do not connect directly to each other.
- Console commands are translated into JSON messages before being sent.
- The GUI client uses the same server and protocol as the console client.

## Documentation

- Architecture: [docs/architecture.md](docs/architecture.md)
- Protocol: [docs/protocol.md](docs/protocol.md)
- Project instructions PDF: [docs/Networking Semester Project Instruction.pdf](docs/Networking%20Semester%20Project%20Instruction.pdf)
- Technical report: [technical_report_and_screenshots/technical_report.md](technical_report_and_screenshots/technical_report.md)
