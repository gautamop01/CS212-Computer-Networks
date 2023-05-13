# CS212-Computer-Networks
# Computer Networks Course
## Lab 1 - Basic Networking Tools and Wireshark
## Lab 2 - Sockets + Make A Chat Room (Logic Based On Other chatting platform)
### In Lab 2 lab :
#### The codes in the description are instructions for designing and implementing a series of programs to demonstrate the use of UDP and TCP sockets in Python.
#### Part 1 involves creating a UDP Client-Server system that sends requests for either the current date or time, and receives responses from the server with the requested information.
#### Part 2 involves creating a TCP Client-Server system where the client sends an arithmetic expression to the server, and the server calculates the result and sends it back to the client. The client can continue to send arithmetic expressions until it decides to quit.
#### Part 3 is a bonus question that involves designing a multi-client TCP server, which acts as a chat room manager. The server allows clients to log in to the chat room and keeps track of all logged-in clients. The server sends messages to all logged-in clients when interesting events occur, such as a new user joining or leaving the chat. The clients act as chat windows, sending messages to the server and displaying messages received from the server.

## Lab 3 - Principles of Reliable Data Transfer
### In this lab i completed these codes: 
#### Testbench.py: This file is used to run the simulations and test the reliability of the different protocols. It contains the main function that initiates the simulation and sets the parameters such as the number of messages to send, the probability of packet corruption (Pc), and the probability of packet loss (Pl).
#### Channel.py: This file implements a model for an unreliable channel over which packets can be corrupted or lost. It takes in the parameters Pc, Pl, and Delay, and simulates the behavior of the channel.
#### Protocol_rdt1.py: This file implements the trivial protocol rdt1.0, which works only if the channel is assumed to be ideal. It is used to test the behavior of the channel when Pc = 0.

#### Protocol_rdt2.py: This file implements the simple ACK/NAK based protocol rdt2.0 that can work when data packets can get corrupted. It is used to test the behavior of the channel when Pc > 0.

#### Protocol_rdt22.py: This file implements the alternating-bit protocol rdt2.2, which can work even when both the data and ack packets can get corrupted. It is used to test the behavior of the channel when both Pc and Pl are greater than 0.

#### Protocol_rdt3.py: This file implements the alternating-bit protocol with timeouts (rdt3.0), which can work when data or ack packets can be corrupted or lost. It is used to test the behavior of the channel when both Pc and Pl are greater than 0.

## Lab 4 - Sliding Window Protocols
#### This lab assignment involves implementing the Go-back-N and Selective Repeat protocols for reliable data transfer by translating their FSM descriptions into Python code. The aim is to perform simulations to validate the implementation and gain insights on how the performance of these protocols varies with various parameters.
#### The submission for this team assignment should include a typeset report in pdf format, a Python file containing the implementation of the Selective Repeat protocol, and no other files. The Go-Back-N protocol is provided as a template.

#### The assignment has four tasks:
#### Verify the Go-Back-N protocol's Python implementation matches the FSM description given in the textbook and simulate the system with non-zero probability of packet corruption and loss for both the DATA and ACK channels.
#### Set parameter values for the DATA and ACK channels and modify the Testbench.py file for a single simulation run until the receiving application receives the first 1000 messages. Report the time at which the receiving application receives the first 1000 messages, the channel utilization on the sender side (for the DATA channel), and the fraction of packets sent by the rdt_Sender that are simply retransmissions of previously sent packets.
#### Draw plots to show how the simulation time at which the receiving application receives the first 1000 messages, the percentage of packets sent that are retransmissions of previously sent packets, and the channel utilization on the sender-side vary with the probability of packet loss (Pl ranges from 0.1 to 0.9) while keeping the other parameters constant.
#### Implement the Selective Repeat protocol and modify the Testbench.py file for a single simulation run until the receiving application receives the first 1000 messages. Report the time at which the receiving application receives the first 1000 messages, the channel utilization on the sender-side (for the DATA channel), and the fraction of packets sent by the rdt_Sender that are simply retransmissions of previously sent packets. Compare the results with those from the Go-Back-N protocol.
## Lab 5 - The Web, HTTP and DNS 
### This repository contains the code and files for Lab 5 on The Web, HTTP and DNS in a computer networking course. The lab includes creating web pages using HTML and JavaScript, creating a web server using Python, observing HTTP traffic using browser and Wireshark, and exploring DNS using the dig command and Wireshark. The code includes HTML, JavaScript, and Python scripts for the web server. The repository also includes screenshots and a brief report documenting the solutions for each question in the lab.

