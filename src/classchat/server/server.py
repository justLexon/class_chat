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

def handle_client(client_socket, client_address):
    print(f"Connected by {client_address}")
    username = None

    # Send acknowledge message to client saying "connected"
    # sendall(...): sends the parameter to the client
    # encode(): turns string in bytes
    ack_message = "Connected to ClassChat server"
    client_socket.sendall(ack_message.encode())

    try:
        # First message from the client should be their username
        username_data = client_socket.recv(BUFFER_SIZE)
        if not username_data:
            return

        username_message = username_data.decode().strip()
        username_parts = username_message.split(maxsplit = 1)

        if len(username_parts) != 2 or username_parts[0] != "/username":
            client_socket.sendall("Invalid username format. Use /username your_name".encode())
            return

        username = username_parts[1]

        with clients_lock:
            if username in connected_clients:
                client_socket.sendall("Username already in use.".encode())
                return

            connected_clients[username] = client_socket

        client_socket.sendall(f"Username set to {username}".encode())
        print(f"{username} registered from {client_address}")

        # Loop for persistent listening
        while True:
            # Receive any messages from the client
            # recv(...): receives the bytes from client and decodes message into string
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print(f"Client disconnected: {username}")
                break

            message = data.decode().strip()

            if message == "/quit":
                client_socket.sendall("Closing connection.".encode())
                print(f"Client requested disconnect: {username}")
                break

            if message == "/list":
                with clients_lock:
                    users = ", ".join(connected_clients.keys())
                client_socket.sendall(f"Connected users: {users}".encode())
                continue

            if message.startswith("/msg "):
                message_parts = message.split(maxsplit = 2)

                if len(message_parts) < 3:
                    client_socket.sendall("Use /msg username your_message".encode())
                    continue

                receiver = message_parts[1]
                text = message_parts[2]

                with clients_lock:
                    receiver_socket = connected_clients.get(receiver)

                if receiver_socket is None:
                    client_socket.sendall(f"User {receiver} is not connected.".encode())
                    continue

                receiver_socket.sendall(f"\nFrom {username}: {text}".encode())
                # client_socket.sendall(f"Message sent to {receiver}".encode())
                print(f"{username} -> {receiver}: {text}")
                continue

            client_socket.sendall("Unknown command. Use /msg, /list, or /quit".encode())
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
