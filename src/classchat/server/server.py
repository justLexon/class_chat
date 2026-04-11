import socket

# Personal machine for hosting
HOST = "127.0.0.1"
# Port that the server listens on
PORT = 5000
# Amount of bytes that can be read at once
BUFFER_SIZE = 1024

def start_server():
    # Make TCP Socket, where AF_INET means IPv4 and SOCK_STREAM means TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow quick restart without waiting for the port to free up
    # setsockopt avoids "address already in use" issue when restarting the server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind socket to IP address and port
    server_socket.bind((HOST, PORT))

    # listen(int) tells OS that the socket is waiting for connections
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    # Server accepts client
    client_socket, client_address = server_socket.accept()
    print(f"Connected by {client_address}")

    # Send acknowledge message to client saying "connected"
    # sendall(...): sends the parameter to the client
    # encode(): turns string in bytes
    ack_message = "Connected to ClassChat server"
    client_socket.sendall(ack_message.encode())

    # Receive any messages from the client
    # recv(...): receives the bytes from client and decodes message into string
    data = client_socket.recv(BUFFER_SIZE)
    message = data.decode()
    print(f"Received from client: {message}")

    # Send a message to confirm message was received
    response = f"Server received: {message}"
    client_socket.sendall(response.encode())

    # Close/End connection
    client_socket.close()
    server_socket.close()
    print("Server shutdown")


if __name__ == "__main__":
    start_server()
