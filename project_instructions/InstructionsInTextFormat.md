# Project Title: A ClassChat System

The objective of this project is to design and develop an online chat system, named `ClassChat`, to be used for communications and discussions among students in a class. The `ClassChat` system should provide a software platform that enables students to chat with the instructor and other students for necessary discussions such as homework problems.

## Requirements

The total points for this project are `100 + 40 bonus`.

- Add a `README` file explaining how to run your code.
- Add a screenshot for your demo for each section.
- Add a technical report explaining your implementation.
- If you use AI/ChatGPT for your project, include why and where you used it and what you learned during the process.

If the `README` or technical report, including screenshots, is missing, the project will not be graded.

## 1. Client-Server Communication Using TCP/IP

The first step is to build a server and a client that can communicate with each other.

### 1.1 Server

A server should be developed as a central controlling point that can offer resources and services per client request. Here, the server should have a core function of interconnecting the communication of two clients. That is, if client `A` wishes to initiate a chat with client `B`, both `A` and `B` should connect to the server, and the server can help forward messages or requests between `A` and `B`.

To implement a server, the following steps have to be implemented:

- Create a socket for communication
- Bind the local port and connection address
- Configure TCP protocol with a port number
- Listen for client connection
- Accept connection from client
- Send acknowledgment
- Receive message from client
- Send message to client

### 1.2 Client

To implement a client, the following steps have to be implemented:

- Create a socket for communication
- Configure TCP protocol with the server IP address and port number
- Connect with the server through the socket
- Wait for acknowledgment from the server
- Send message to the server
- Receive message from the server

The sketch of client-server communication through socket programming using TCP/IP is shown in Figure 1.

`Server <-> Client`

Figure 1: Client-server communication using TCP/IP

### 1.3 Requirement

Now, you can implement the communications of a client and a server. In the implementation, GUI is not required but is highly encouraged. It is fine if you just use the command line to let the client and server communicate with each other, but UI would be appreciated.

Python is strongly recommended to implement the system since it offers convenient tools for socket programming.

This task takes `30 points`.

## 2. Advanced Client

After you have implemented the simple client-server communication system, you can add more function so that a client can both send and receive messages at the same time with less CPU workload.

I/O multiplexing can be used in this task. You can use a system callback function to activate a client application. That is, a client will be activated if the socket receives data from the server or keyboard input from the user.

Hint: try to use `select()`, `poll()`, and `epoll()` in your client.

This part takes `20 points`.

## 3. Multi-Thread Communication Server

Now the client-server communication system should be improved by developing a network server that can handle multiple concurrent users. The goal of this task is to allow multiple students to discuss class topics or homework problems at the same time.

There are three common ways to implement such a function in a server:

- Use the `socketserver` model
- Use `thread + socket`
- Use I/O multiplexing

You can select any one method to implement your server.

In the first method, Python provides the `socketserver` package to simplify the process of building a network server.

By this point, your server should be able to support connections with multiple clients at the same time.

This part takes `20 points`.

## 4. Client-Client Communication

Now, you are ready to implement client-to-client communication in `ClassChat`.

Your `ClassChat` should have three core functions:

- Client management
- Receive messages from a sending client
- Forward messages to a receiving client

Client management is very important on the server. The server should be able to capture the exception where a receiver is not in the system. For example, `A` wishes to chat with `B`, but `B` is not in the system. Practical cases like this should be considered to make the system more robust.

Figure 2 illustrates the main function of the `ClassChat` server. Clients can communicate with each other by passing messages through the `ClassChat` server. Figure 3 shows a demo of `ClassChat`. In that figure, Alice and Bob first create connections with the server. Then Alice sends a message to Bob, the server receives the message and forwards it to Bob.

Figure 2: A flowchart of `ClassChat`

Figure 3: `ClassChat` demo

- Client window for Alice
- Client window for Bob
- Server window

In your client, you should be able to capture sender information, receiver information, and text messages. `JSON` is a standard format that can be used in network transmission.

In this project, a simple example is:

```json
{
  "status": "1",
  "sender": "Alice",
  "receiver": "Bob",
  "text": "Hi, do you know how TCP works?"
}
```

This task takes `30 points`.

Figure 4: An example of group chatting

## 5. Bonus Section

The following tasks aim to enhance `ClassChat`'s functionality. You can get `10 bonus points` for each one.

### 5.1 Group Chatting

Group chatting is important for group discussion or information announcement.

The core function here is that each group member can send and receive messages in the group chat window, while those messages are visible to all group members.

For example, an instructor may create a group including all students so important information can be broadcast to the group and received by all students. Also, if any student has a question, they can raise it in the group. The instructor and all students can see the question and give replies.

An example is shown in Figure 4.

### 5.2 File Transfer

You can improve `ClassChat` by supporting file transfer between clients. That is, one client can transfer a file to another client by using `ClassChat`.

### 5.3 Offline Message

Now, enable `ClassChat` to receive offline messages.

For example, the instructor assigns a project to the class through `ClassChat`, but some students may not be online and may not be connected to the server. To recover this offline message, the server should save the message for offline clients. Once these clients connect to the server, the stored message can be forwarded to them.

### 5.4 Encryption/Decryption Between Client and Server

The `ClassChat` server IP address and port are exposed on the network. Transmitted messages have the potential risk of being captured by Wireshark. To improve security, add encryption and decryption to transmitted messages.

Please come up with a security model for `ClassChat`.

Hint: use public and private keys to generate and transmit a session key.
