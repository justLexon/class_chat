import json
import socket
import sys
import threading

# Personal machine for hosting
HOST = "127.0.0.1"
# Port that the server listens on
PORT = 5000
# Amount of bytes that can be read at once
BUFFER_SIZE = 1024
PROMPT = "Enter a message for the server: "
waiting_for_input = threading.Event()
console_lock = threading.Lock()

def send_json(client_socket, payload):
    try:
        client_socket.sendall(json.dumps(payload).encode())
        return True
    except OSError:
        return False

def receive_json(client_socket):
    try:
        response_data = client_socket.recv(BUFFER_SIZE)
        if not response_data:
            return None

        return json.loads(response_data.decode())
    except (OSError, json.JSONDecodeError):
        return None

def print_server_message(message_text):
    with console_lock:
        if waiting_for_input.is_set():
            sys.stdout.write("\r")
            sys.stdout.write(" " * (len(PROMPT) + 80))
            sys.stdout.write("\r")
            sys.stdout.flush()

        print(message_text)

        if waiting_for_input.is_set():
            sys.stdout.write(PROMPT)
            sys.stdout.flush()

def receive_messages(client_socket):
    while True:
        try:
            response_message = receive_json(client_socket)
            if response_message is None:
                print_server_message("Server disconnected.")
                break

            message_type = response_message.get("type")

            if message_type == "chat":
                print_server_message(f"From {response_message['sender']}: {response_message['text']}")
            else:
                print_server_message(f"{response_message['text']}")

            if message_type == "disconnect":
                break
        except (OSError, json.JSONDecodeError):
            break

def start_client():
    # Make TCP Socket, where AF_INET means IPv4 and SOCK_STREAM means TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect socket to IP address and port
    client_socket.connect((HOST, PORT))
    print(f"Connect to server at {HOST}:{PORT}")

    # Wait for server to send ack message
    ack_message = receive_json(client_socket)
    if ack_message is None:
        print("Could not connect to the server.")
        client_socket.close()
        return
    print(f"Server says: {ack_message['text']}")

    # Register username with the server before starting chat
    while True:
        username = input("Enter your username: ").strip()

        if username == "":
            print("Username cannot be blank. Please try again.")
            continue

        break

    username_sent = send_json(
        client_socket,
        {
            "type": "register",
            "sender": username,
        },
    )

    if not username_sent:
        print("Server disconnected before username registration.")
        client_socket.close()
        return

    username_response_message = receive_json(client_socket)
    if username_response_message is None:
        print("Server disconnected during username registration.")
        client_socket.close()
        return
    print(f"Server says: {username_response_message['text']}")

    if username_response_message["type"] == "error":
        client_socket.close()
        return

    receiver_thread = threading.Thread(
        target = receive_messages,
        args = (client_socket,),
        daemon = True,
    )
    receiver_thread.start()

    print("Use /msg username your_message to chat")
    print("Use /list to see connected users")
    print("Use /quit to disconnect\n")

    while True:
        # Send message to server
        waiting_for_input.set()
        message = input(PROMPT).strip()
        waiting_for_input.clear()

        if message == "/list":
            message_sent = send_json(
                client_socket,
                {
                    "type": "list",
                    "sender": username,
                },
            )
            if not message_sent:
                print("Server disconnected.")
                break
            continue

        if message.startswith("/msg "):
            message_parts = message.split(maxsplit = 2)

            if len(message_parts) < 3:
                print("Use /msg username your_message")
                continue

            message_sent = send_json(
                client_socket,
                {
                    "type": "chat",
                    "sender": username,
                    "receiver": message_parts[1],
                    "text": message_parts[2],
                },
            )
            if not message_sent:
                print("Server disconnected.")
                break
            continue

        if message == "/quit":
            message_sent = send_json(
                client_socket,
                {
                    "type": "disconnect",
                    "sender": username,
                },
            )
            if not message_sent:
                print("Server disconnected before /quit could be sent.")
            print("Client closed")
            break

        print("Unknown command. Use /msg, /list, or /quit")

    client_socket.close()

if __name__ == "__main__":
    start_client()
