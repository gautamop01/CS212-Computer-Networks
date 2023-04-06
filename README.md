# CS212-Computer-Networks
# Computer Networks Course
## Lab 1 - Basic Networking Tools and Wireshark
## Lab 2 - Sockets + Make A Chat Room (Logic Based On Other chatting platform)
## Lab 3 - Principles of Reliable Data Transfer
## Lab 4 - Sliding Window Protocols
### This lab assignment involves implementing the Go-back-N and Selective Repeat protocols for reliable data transfer by translating their FSM descriptions into Python code. The aim is to perform simulations to validate the implementation and gain insights on how the performance of these protocols varies with various parameters.

The submission for this team assignment should include a typeset report in pdf format, a Python file containing the implementation of the Selective Repeat protocol, and no other files. The Go-Back-N protocol is provided as a template.

The assignment has four tasks:

Verify the Go-Back-N protocol's Python implementation matches the FSM description given in the textbook and simulate the system with non-zero probability of packet corruption and loss for both the DATA and ACK channels.
Set parameter values for the DATA and ACK channels and modify the Testbench.py file for a single simulation run until the receiving application receives the first 1000 messages. Report the time at which the receiving application receives the first 1000 messages, the channel utilization on the sender side (for the DATA channel), and the fraction of packets sent by the rdt_Sender that are simply retransmissions of previously sent packets.
Draw plots to show how the simulation time at which the receiving application receives the first 1000 messages, the percentage of packets sent that are retransmissions of previously sent packets, and the channel utilization on the sender-side vary with the probability of packet loss (Pl ranges from 0.1 to 0.9) while keeping the other parameters constant.
Implement the Selective Repeat protocol and modify the Testbench.py file for a single simulation run until the receiving application receives the first 1000 messages. Report the time at which the receiving application receives the first 1000 messages, the channel utilization on the sender-side (for the DATA channel), and the fraction of packets sent by the rdt_Sender that are simply retransmissions of previously sent packets. Compare the results with those from the Go-Back-N protocol.
## Lab 5 - The Web, HTTP and DNS 
### This repository contains the code and files for Lab 5 on The Web, HTTP and DNS in a computer networking course. The lab includes creating web pages using HTML and JavaScript, creating a web server using Python, observing HTTP traffic using browser and Wireshark, and exploring DNS using the dig command and Wireshark. The code includes HTML, JavaScript, and Python scripts for the web server. The repository also includes screenshots and a brief report documenting the solutions for each question in the lab.

