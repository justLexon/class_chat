import json
import socket
import threading

# Personal machine for hosting
HOST = "127.0.0.1"
# Port that the server listens on
PORT = 5000
# Amount of bytes that can be read at once
BUFFER_SIZE = 1024
# Store all connected clients by username
connected_clients = {}
# Lock to protect connected clients when multiple threads update it
clients_lock = threading.Lock()

def send_json(client_socket, payload):
    try:
        client_socket.sendall(json.dumps(payload).encode())
        return True
    except OSError:
        return False

def receive_json(client_socket):
    try:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            return None

        return json.loads(data.decode())
    except (OSError, json.JSONDecodeError):
        return None

def handle_client(client_socket, client_address):
    print(f"Connected by {client_address}")
    username = None

    # Send acknowledge message to client saying "connected"
    send_json(
        client_socket,
        {
            "type": "ack",
            "text": "Connected to ClassChat server",
        },
    )

    try:
        # First message from the client should be their username
        register_message = receive_json(client_socket)
        if register_message is None:
            return

        if register_message.get("type") != "register":
            send_json(
                client_socket,
                {
                    "type": "error",
                    "text": "First message must be a register message.",
                },
            )
            return

        username = register_message.get("sender", "").strip()

        if username == "":
            send_json(
                client_socket,
                {
                    "type": "error",
                    "text": "Username cannot be empty.",
                },
            )
            return

        with clients_lock:
            if username in connected_clients:
                send_json(
                    client_socket,
                    {
                        "type": "error",
                        "text": "Username already in use.",
                    },
                )
                return

            connected_clients[username] = client_socket

        send_json(
            client_socket,
            {
                "type": "ack",
                "text": f"Username set to {username}",
            },
        )
        print(f"{username} registered from {client_address}")

        # Loop for persistent listening
        while True:
            # Receive any messages from the client
            message = receive_json(client_socket)
            if message is None:
                print(f"Client disconnected: {username}")
                break

            message_type = message.get("type")

            if message_type == "disconnect":
                send_json(
                    client_socket,
                    {
                        "type": "disconnect",
                        "text": "Closing connection.",
                    },
                )
                print(f"Client requested disconnect: {username}")
                break

            if message_type == "list":
                with clients_lock:
                    users = list(connected_clients.keys())
                send_json(
                    client_socket,
                    {
                        "type": "list",
                        "users": users,
                        "text": f"Connected users: {', '.join(users)}",
                    },
                )
                continue

            if message_type == "chat":
                receiver = message.get("receiver", "").strip()
                text = message.get("text", "").strip()

                if receiver == "" or text == "":
                    send_json(
                        client_socket,
                        {
                            "type": "error",
                            "text": "Chat messages need a receiver and text.",
                        },
                    )
                    continue

                with clients_lock:
                    receiver_socket = connected_clients.get(receiver)

                if receiver_socket is None:
                    send_json(
                        client_socket,
                        {
                            "type": "error",
                            "text": f"User {receiver} is not connected.",
                        },
                    )
                    continue

                message_sent = send_json(
                    receiver_socket,
                    {
                        "type": "chat",
                        "sender": username,
                        "receiver": receiver,
                        "text": text,
                    },
                )

                if not message_sent:
                    with clients_lock:
                        if receiver in connected_clients:
                            del connected_clients[receiver]

                    send_json(
                        client_socket,
                        {
                            "type": "error",
                            "text": f"User {receiver} disconnected before the message could be delivered.",
                        },
                    )
                    continue

                print(f"{username} -> {receiver}: {text}")
                continue

            send_json(
                client_socket,
                {
                    "type": "error",
                    "text": "Unknown message type.",
                },
            )
    except json.JSONDecodeError:
        send_json(
            client_socket,
            {
                "type": "error",
                "text": "Invalid JSON message format.",
            },
        )
    finally:
        if username is not None:
            with clients_lock:
                if username in connected_clients:
                    del connected_clients[username]
        client_socket.close()

def start_server():
    # Make TCP Socket, where AF_INET means IPv4 and SOCK_STREAM means TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow quick restart without waiting for the port to free up
    # setsockopt avoids "address already in use" issue when restarting the server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind socket to IP address and port
    server_socket.bind((HOST, PORT))

    # listen(int) tells OS that the socket is waiting for connections
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        # Server accepts clients continuously
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(
            target = handle_client,
            args = (client_socket, client_address),
            daemon = True,
        )
        client_thread.start()

if __name__ == "__main__":
    start_server()
