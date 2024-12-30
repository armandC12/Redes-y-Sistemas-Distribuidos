# Server Application

This repository contains the implementation of a server application as part of the Networks and Distributed Systems course. The server application is designed to handle client connections and perform various tasks based on the client's requests.

## Contributors

- Fernando Alvarado (fernando.alvarado@mi.unc.edu.ar)
- Ivan Ponzio (ivan.ponzio@mi.unc.edu.ar)
- Armando Carral (armando.carral@mi.unc.edu.ar)

## Table of Contents

- Code Structure
- Design
- Challenges
- Questions

## Code Structure

### server.py

The `server.py` file contains the main implementation of the server application. It provides functionality for initializing the server, accepting client connections, and processing client requests. The server utilizes socket programming to establish network connections and communicate with clients.

### connection.py

The `connection.py` module is responsible for handling individual client connections. It defines the logic for receiving client requests, processing them, and sending back the appropriate responses.

## Design

The server application is designed to follow a client-server architecture. It uses the socket library in Python to create a socket and listen for incoming client connections. Once a client connection is established, a new thread is spawned to handle the client's requests concurrently. This allows the server to handle multiple clients simultaneously without blocking other connections.

## Challenges

During the development process, we encountered several challenges. One of the difficulties was implementing error handling using try-except statements, as we were not familiar with this approach initially. Additionally, encoding and sending messages correctly posed some challenges, which required us to refine our implementation and ensure proper communication between the server and clients.

## Questions

1. What strategies exist to implement a server capable of handling multiple clients simultaneously? Briefly research and explain what changes would be necessary in the code design.

To implement a server that can handle multiple clients simultaneously, one common approach is to use multithreading. This involves creating a new thread for each incoming client connection and delegating the communication tasks to these threads. By doing so, each thread can handle a specific client connection independently, allowing the server to serve multiple clients concurrently. In terms of code design, modifications would be required to properly manage and synchronize access to shared resources among the different threads.

2. When running the server on a machine, what is the difference between using the IP address "localhost", "127.0.0.1", or "0.0.0.0"?

- "localhost" is a hostname that refers to the current machine where the server is running. When using "localhost", the server only listens for connections from the local machine itself.
- "127.0.0.1" is the loopback IP address of IPv4, which is commonly used to refer to the local machine. Like "localhost", it restricts connections to the local machine only.
- "0.0.0.0" is a special IP address that represents all available network interfaces on the machine. When the server is configured to listen on "0.0.0.0", it can accept connections from any network interface, including physical and virtual interfaces.

It is important to note that the choice of IP address affects the accessibility of the server and the range of clients that can connect to it.