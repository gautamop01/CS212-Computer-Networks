# SimPy model for the Reliable Data Transport (rdt) Protocol 2.0 (Using ACK and NAK)

#
# Sender-side (rdt_Sender)
# - receives messages to be delivered from the upper layer
# (SendingApplication)
# - Implements the protocol for reliable transport
# using the udt_send() function provided by an unreliable channel.
#
# Receiver-side (rdt_Receiver)
# - receives packets from the unrealible channel via calls to its
# rdt_rcv() function.
# - implements the receiver-side protocol and delivers the collected
# data to the receiving application.

# Author: Neha Karanjkar


import simpy
import random
from Packet import Packet
import sys

# Here is the sender can be in one of these four states:
call0fromabove = 0
ack0 = 1
call1fromabove = 2
ack1 = 3
call0frombelow = 4
call1frombelow = 5


class rdt_Sender(object):

    def __init__(self, env):
        # Here is Initialize variables
        self.env = env
        self.channel = None

        # Here are some state variables
        self.state = call0fromabove
        self.seq_num = 0
        self.packet_to_be_sent = None

    def rdt_send(self, msg):

        if self.state == call0fromabove:
            # Here is This function is called by the
            # now, sending application.

            # Here is create a packet, and save a copy of this packet
            # now for retransmission, if needed
            self.packet_to_be_sent = Packet(seq_num=0, payload=msg)
            self.seq_num = 0
            # Here send it over the channel
            self.channel.udt_send(self.packet_to_be_sent)
            # Now, wait for an ACK or NAK 
            self.state = ack0
            return True
        elif self.state == call1fromabove:
            # Here This function is called by the ending application.

            # Now, create a packet, and save a copy of this packet or retransmission, if needed
            self.packet_to_be_sent = Packet(seq_num=1, payload=msg)
            self.seq_num = 1
            # Here us send it over the channel
            self.channel.udt_send(self.packet_to_be_sent)
            # Now wait for an ACK or NAK
            self.state = ack1
            return True

    def rdt_rcv(self, packt):
        if (packt.corrupted or self.seq_num != packt.seq_num):
            # Here are Corrupted Packet is being received
            # if (self.state == ack0):
            #     assert (self.state == ack0)
            # else:
            #     assert (self.state == ack1
            self.channel.udt_send(self.packet_to_be_sent)
        else:
            # Here is Packet isn't corrupted
            if (self.state == ack0):
                # assert (self.state == ack0)
                self.state = call1fromabove

            else:
                self.state = call0fromabove
    


class rdt_Receiver(object):
    def __init__(self, env):
        # Initialize variables
        self.env = env
        self.receiving_app = None
        self.channel = None
        self.state = call0frombelow
        self.seq_num = 0

    def rdt_rcv(self, packt):
        # Here This function is called by the lower-layer when a packet arrivesmat the receiver

        if (self.state == call0frombelow):
            # Now, check whether the packet is corrupted
            if (packt.corrupted or self.seq_num != packt.seq_num):
                # Now, send a NAK and discard this packet.
                # seq_num for the response can be arbitrary. It is ignored.
                response = Packet(seq_num=1, payload="ACK1")
                # send it over the channel
                self.channel.udt_send(response)
            else:
                # Here The packet is not corrupted and Send an ACK and deliver the data.
                self.state = call1frombelow
                response = Packet(seq_num=0, payload="ACK0")
                # Now, send it over the channel
                self.channel.udt_send(response)
                self.receiving_app.deliver_data(packt.payload)
                self.seq_num = 1
        else:
            # Here is check whether the packet is corrupted
            if (packt.corrupted or self.seq_num != packt.seq_num):
                # Now, send a NAK and discard this packet and seq_num for the response can be arbitrary. It is ignored.
                response = Packet(seq_num=0, payload="ACK0")
                # Now, send it over the channel
                self.channel.udt_send(response)
            else:
                # Here is The packet is not corrupted.
                # Now Send an ACK and deliver the data.
                self.state = call0frombelow
                response = Packet(seq_num=1, payload="ACK1")
                # send it over the channel
                self.channel.udt_send(response)
                self.receiving_app.deliver_data(packt.payload)
                self.seq_num = 0
