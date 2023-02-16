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
ACK_0 = 1
call1fromabove = 2
ACK_1 = 3
call0frombelow = 4
call1frombelow = 5

packetCount = 0
Overall_Time = 0


class rdt_Sender(object):

    def __init__(self, env):
        # Here is Initialize variables 
        self.env = env
        self.channel = None
        self.timeout_value = 3*2
        self.timer_is_running = False
        self.timer = None
        # Here is some state variables
        self.state = call0fromabove
        self.seq_num = 0
        self.packet_to_be_sent = None
        self.avg_time = 0

    def timer_behavior(self):
        try:
            # Here is Start
            self.timer_is_running = True
            yield self.env.timeout(self.timeout_value)
            # now , Stop
            self.timer_is_running = False
            # Here is take some actions
            self.timeout_action()
        except simpy.Interrupt:
            # Here is upon interrupt, stop the timer
            self.timer_is_running = False

    # This function can be called to start the timer
    def start_timer(self):
        assert (self.timer_is_running == False)
        self.timer = self.env.process(self.timer_behavior())
        # This function can be called to stop the timer

    def stop_timer(self):
        assert (self.timer_is_running == True)
        self.timer.interrupt()

    def timeout_action(self):
        # Now, add here the actions to be performed upon a timeout
        self.channel.udt_send(self.packet_to_be_sent)
        self.start_timer()

    def rdt_send(self, msg):
        global starttime
        if self.state == call0fromabove:
            # Now, This function is called by the ending application.

            # create a packet, and save a copy of this packet for retransmission, if needed
            self.packet_to_be_sent = Packet(seq_num=0, payload=msg)
            self.seq_num = 0
            self.start_timer()
            starttime = self.env.now
            # send it over the channel
            self.channel.udt_send(self.packet_to_be_sent)
            # wait for an ACK or NAK
            self.state = ACK_0
            return True
        elif self.state == call1fromabove:
            # Here is This function is called by the sending application.

            # Now, create a packet, and save a copy of this packet for retransmission, if needed
            self.packet_to_be_sent = Packet(seq_num=1, payload=msg)
            self.seq_num = 1
            self.start_timer()
            starttime = self.env.now
            # Now, send it over the channel
            self.channel.udt_send(self.packet_to_be_sent)
            # Now, wait for an ACK or NAK
            self.state = ACK_1
            return True

    def rdt_rcv(self, packt):
        global packetCount
        global timetaken
        global Overall_Time
        if (packt.corrupted or self.seq_num != packt.seq_num):
            # Here is Corrupted Packet is being received
            if (self.state == ACK_0):
               assert (self.state == ACK_0)
            else:
                assert (self.state == ACK_1)
            self.channel.udt_send(self.packet_to_be_sent)
            pass
        else:
            # Here is Packet isn't corrupted
            if (self.state == ACK_0):
                assert (self.state == ACK_0)
                
                endtime = self.env.now
                packetCount = packetCount+1
                timetaken = endtime - starttime
                Overall_Time = Overall_Time + timetaken
                if (packetCount == 1000):
                    self.avg_time = Overall_Time/1000
                    print("Average Time = ", self.avg_time)
                self.stop_timer()
                self.state = call1fromabove

            else:
                endtime = self.env.now
                packetCount = packetCount+1
                timetaken = endtime - starttime
                Overall_Time = Overall_Time + timetaken
                if (packetCount == 1000):
                    self.avg_time = Overall_Time/1000
                    print("Average Time = ", self.avg_time)
                self.stop_timer()
                self.state = call0fromabove


class rdt_Receiver(object):
    def __init__(self, env):
        # Here is Initialize variables
        self.env = env
        self.receiving_app = None
        self.channel = None
        self.state = call0frombelow
        self.seq_num = 0

    def rdt_rcv(self, packt):
        # Now, This function is called by the lower-layer when a packet arrives
        # at the receiver

        if (self.state == call0frombelow):
            # check whether the packet is corrupted
            if (packt.corrupted or self.seq_num != packt.seq_num):
                # send a NAK and discard this packet. and seq_num for the response can be arbitrary. It is ignored.
                response = Packet(seq_num=1, payload="ACK1")
                self.channel.udt_send(response)
            else:
                # The packet is not corrupted end an ACK and deliver the data.
                self.state = call1frombelow
                response = Packet(seq_num=0, payload="ACK0")
                # send it over the channel
                self.channel.udt_send(response)
                self.receiving_app.deliver_data(packt.payload)
                self.seq_num = 1
        else:
            # Here is check whether the packet is corrupted
            if (packt.corrupted or self.seq_num != packt.seq_num):
                # Now, send a NAK and discard this packet and seq_num for the response can be arbitrary. It is ignored.
                response = Packet(seq_num=0, payload="ACK0")
                # send it over the channel
                self.channel.udt_send(response)
            else:
                # Here is The packet is not corrupted.
                # Now, Send an ACK and deliver the data.
                self.state = call0frombelow
                response = Packet(seq_num=1, payload="ACK1")
                # Here , send it over the channel
                self.channel.udt_send(response)
                self.receiving_app.deliver_data(packt.payload)
                self.seq_num = 0
