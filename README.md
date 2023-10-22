# Data-Streaming Service

## Project Overview

In this endeavor, we have implemented a robust streaming server demonstrating the ubiquitous application of streaming services in contemporary digital ecosystems such as Netflix, stock exchange platforms, and meteorological forecast streaming.
Project Implementation

   - **Stream Nature**: Our team elected to focus on a multimedia stream, encapsulating a sequence of messages, each bearing a distinct type and at least two specific fields. A crucial field is the packet order in the stream, initiating from 1.

   - **Command Line Configuration**: A feature enabling the configuration of the time interval for message transmission in the stream via command line has been successfully integrated.

   - **Client-Server Interaction**: Multiple clients can register with the server to receive the stream, facilitated through UDP/IP. Upon termination, each client generates statistics on UDP usage, including packet loss and out-of-order packet arrival.

   - **Data Operation**: Each client implements an operation on the received data. In our scenario, the operation identifies and returns the most popular data within the stream.

   - **Execution Logs**: Logs for multiple executions have been documented, with one mandatory execution involving three clients receiving the stream.

## Code Structure

   - **server.py**: This file encapsulates the core functionality of the streaming server, handling client registrations, message streaming, and ensuring the seamless transmission of packets to registered clients.

   - **client.py**: This script represents the client-side logic, handling server communication, data reception, operation implementation on the received data, and generating UDP usage statistics upon client termination.

