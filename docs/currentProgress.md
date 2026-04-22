# Current Progress of the Project

## 1.1 (Server) (COMPLETED)
- Create a socket for communication
- Bind the local port and connection address
- Configure TCP protocol with port number
- Listen for client connection
- Accept connection from client
- Send Acknowledgment
- Receive message from client
- Send message to client

# 1.2 (Client)
- Create a socket for communication
- Configure TCP protocol with IP address of server and port number
- Connect with server through socket
- Wait for acknowledgement from server
- Send message to the server
- Receive message from server

# 1.4 (Persistent Server and Client)
- update server.py
- after accept(), keep reading messages in a loop
- reply to each message
- break on /quit or disconnect
- update client.py
- after receiving the server acknowledgment, keep asking for input in a loop
- send each message
- print each response
- break on /quit
- test the flow
- start server
- start client
- send 3 to 4 messages
- quit cleanly