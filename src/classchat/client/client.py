import socket
import threading

# Personal machine for hosting
HOST = "127.0.0.1"
# Port that the server listens on
PORT = 5000
# Amount of bytes that can be read at once
BUFFER_SIZE = 1024
PROMPT = "Enter a message for the server: "
waiting_for_input = threading.Event()

def receive_messages(client_socket):
    while True:
        try:
            response_data = client_socket.recv(BUFFER_SIZE)
            if not response_data:
                print("Server disconnected.")
                break

            response_message = response_data.decode()
            print(f"{response_message}")
            
            if response_message == "Closing connection.":
                break
        except OSError:
            break

def start_client():
    # Make TCP Socket, where AF_INET means IPv4 and SOCK_STREAM means TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect socket to IP address and port
    client_socket.connect((HOST, PORT))
    print(f"Connect to server at {HOST}:{PORT}")

    # Wait for server to send ack message
    ack_data = client_socket.recv(BUFFER_SIZE)
    ack_message = ack_data.decode()
    print(f"Server says: {ack_message}")

    # Register username with the server before starting chat
    username = input("Enter your username: ").strip()
    client_socket.sendall(f"/username {username}".encode())

    username_response_data = client_socket.recv(BUFFER_SIZE)
    username_response_message = username_response_data.decode()
    print(f"Server says: {username_response_message}")

    if username_response_message == "Username already in use.":
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
        client_socket.sendall(message.encode())

        if message == "/quit":
            print("Client closed")
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
