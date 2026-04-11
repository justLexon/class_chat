import socket

# Personal machine for hosting
HOST = "127.0.0.1"
# Port that the server listens on
PORT = 5000
# Amount of bytes that can be read at once
BUFFER_SIZE = 1024

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

    # Send message to server
    message = input("Enter a message for the server: ")
    client_socket.sendall(message.encode())

    # Receive response from server
    response_data = client_socket.recv(BUFFER_SIZE)
    response_message = response_data.decode()
    print(f"Server response: {response_message}")

    # Close connection
    client_socket.close()
    print("Client closed")

if __name__ == "__main__":
    start_client()