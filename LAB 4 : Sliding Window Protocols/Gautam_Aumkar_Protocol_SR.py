# Gautam Kumar Mahar (2103114)
# Aumkar Lorekar (2003108)
#---------------------------------------------------------------------------------

# SimPy models for rdt_Sender and rdt_Receiver
# implementing the Go-Back-N Protocol

# Author: Dr. Neha Karanjkar, IIT Goa
import simpy
import random
import sys
import math
from Packet import Packet

class rdt_Sender(object):
    
    def __init__(self, env):
        # Initialize variables and parameters
        self.env = env
        self.channel = None
        # some default parameter values
        self.data_packet_length = 10  # bits
        self.timer_timeout_value = 1  # default timeout value for the sender
        # packets will have their own time after which they will be resend
        self.timeout_value = 5
        self.N = 5  # Sender's Window size
        self.K = 16  # Packet Sequence numbers can range from 0 to K-1

        # some state variables and parameters for the Go-Back-N Protocol
        self.base = 1  # base of the current window
        self.nextseqnum = 1  # next sequence number
        # a buffer for storing the packets to be sent (implemented as a Python dictionary)
        self.pkt_sent = {}
        # some other variables to maintain sender-side statistics
        self.total_packets_sent = 0
        self.num_retransmissions = 0
        # timer-related variables
        self.timer_is_running = False
        self.timer = None

    def rdt_send(self, msg):
        check = self.nextseqnum in [(self.base+i) % self.K for i in range(0, self.N)]
        if (check):
            print("TIME:", self.env.now, "RDT_SENDER: rdt_send() called for nextseqnum=",
                  self.nextseqnum, " within current window. Sending new packet.")
            # Make a new Packet
            new_pkt = Packet(seq_num=self.nextseqnum, payload=msg,packet_length=self.data_packet_length)
            # Now set some data for this packet in the pkt_sent dictionary
            self.pkt_sent[self.nextseqnum] = {
                0: self.env.now + int(self.timeout_value), 1: False, 2: new_pkt 
                } #Here 0 denotes the timeout value of the packet, current time + timeout value , ACK Status, next packet se no.
            # send the packet
            self.channel.udt_send(new_pkt)
            self.total_packets_sent += 1

            # start the timer if required
            check1 = self.base == self.nextseqnum
            if (check1):
                self.start_timer()
            # update the nextseqnum
            self.nextseqnum = (self.nextseqnum+1) % self.K
            return True
        else:
            print("TIME:", self.env.now, "RDT_SENDER: rdt_send() called for nextseqnum=",
                  self.nextseqnum, " outside the current window. Refusing data.")
            return False

    def rdt_rcv(self, packt):
        # This function is called by the lower-layer
        # when an ACK packet arrives

        if (packt.corrupted == False):
            if (packt.seq_num in self.pkt_sent.keys()):
                if (not self.pkt_sent[packt.seq_num][1]):
                    self.pkt_sent[packt.seq_num][1] = True 
                    print("TIME:", self.env.now, "RDT_SENDER: got an ACK", packt.seq_num, ". updated window:", [
                        (self.base+i) % self.K for i in range(0, self.N)], "base =", self.base, "nextseqnum =", self.nextseqnum)

                    while (self.base in self.pkt_sent.keys() and self.pkt_sent[self.base][1] == True):
                        del self.pkt_sent[self.base]
                        self.base = (self.base + 1) % self.K

                    if (self.base == self.nextseqnum):
                        self.stop_timer()
                    else:
                        self.restart_timer()
                else:
                    print("TIME:", self.env.now, "RDT_SENDER: got an ACK", packt.seq_num, "packet is alredy acked Updated window:", [
                        (self.base+i) % self.K for i in range(0, self.N)], "base =", self.base, "nextseqnum =", self.nextseqnum)
        else:
            # corrupt packet is ignored
            print("TIME:", self.env.now, "RDT_SENDER: packet was corrupted")

    # Finally, these functions are used for modeling a Timer's behavior.
    def timer_behavior(self):
        try:
            # Wait for timeout
            self.timer_is_running = True
            yield self.env.timeout(self.timer_timeout_value)
            self.timer_is_running = False
            # take some actions
            self.timeout_action()
        except simpy.Interrupt:
            # stop the timer
            self.timer_is_running = False

    # This function can be called to start the timer
    def start_timer(self):
        assert (self.timer_is_running == False)
        self.timer = self.env.process(self.timer_behavior())
        print("TIME:", self.env.now, "TIMER STARTED for a timeout of ",
              self.timer_timeout_value)

    # This function can be called to stop the timer
    def stop_timer(self):
        assert (self.timer_is_running == True)
        self.timer.interrupt()
        print("TIME:", self.env.now, "TIMER STOPPED.")

    def restart_timer(self):
        # stop and start the timer
        assert (self.timer_is_running == True)
        self.timer.interrupt()
        # assert(self.timer_is_running==False)
        self.timer = self.env.process(self.timer_behavior())
        print("TIME:", self.env.now, "TIMER RESTARTED for a timeout of ",
              self.timer_timeout_value)

    # Actions to be performed upon timeout

    def timeout_action(self):

        # re-send all the packets for which an ACK has been pending and time has crossed time_out
        pkts = list(self.pkt_sent.keys())
        to_resend = []

        for seq_num in pkts:
            if self.pkt_sent[seq_num][1] == False and self.pkt_sent[seq_num][0] < self.env.now:
                to_resend.append(seq_num)
                self.pkt_sent[seq_num][0] = int(
                    self.env.now) + self.timeout_value
        print("TIME:", self.env.now,
              "RDT_SENDER: got a timeout, now resending the packet", to_resend, " from", list(self.pkt_sent.keys()))

        for seq_num in to_resend:
            self.channel.udt_send(self.pkt_sent[seq_num][2])
            self.num_retransmissions += 1
            self.total_packets_sent += 1
        self.start_timer()

    # A function to print the current window position for the sender.
    def print_status(self):
        print("TIME:", self.env.now, "Current window:", [
              (self.base+i) % self.K for i in range(0, self.N)], "base is ", self.base, "next_seqnum is ", self.nextseqnum)
        print("TIME:", self.env.now, "buffer contents:", [str(
            i) + "-" + ("has been acknowledged" if self.pkt_sent[i][1] else "is not acknowledged") for i in list(self.pkt_sent.keys())], )
        print("---------------------")


# ==========================================================================================

class rdt_Receiver(object):

    def __init__(self, env):

        # Initialize variables
        self.env = env
        self.receiving_app = None
        self.channel = None

        # some default parameter values
        self.ack_packet_length = 10  # bits
        self.K = 16  # range of sequence numbers expected
        self.N = 5   # Receiver's window size
        # initialize state variables
        self.base = 1
        self.pkt_sent = Packet(seq_num=0, payload="ACK",
                             packet_length=self.ack_packet_length)
        self.total_packets_sent = 0
        self.num_retransmissions = 0
        self.rcvpkt = {}

    def rdt_rcv(self, packt):
        check = packt.seq_num in [(self.base+i) % self.K for i in range(0, self.N)]
        if (not packt.corrupted and check):
            self.rcvpkt[packt.seq_num] = packt
            self.pkt_sent = Packet(seq_num=packt.seq_num,payload="ACK", packet_length=self.ack_packet_length)
            self.channel.udt_send(self.pkt_sent)
            self.total_packets_sent += 1

        elif (not packt.corrupted):
            print("TIME:", self.env.now, "RDT_RECEIVER: this is a packet that has been received from an old window",". Sent ACK", packt.seq_num)
            self.pkt_sent = Packet(seq_num=packt.seq_num, payload="ACK", packet_length=self.ack_packet_length)
            self.channel.udt_send(self.pkt_sent)
            self.total_packets_sent += 1
            self.num_retransmissions += 1
        else:
            print("TIME:", self.env.now, "RDT_RECEIVER: got corrupted packet",
                    ". Sent ACK", self.pkt_sent.seq_num)

        self.final_deliver()

    def final_deliver(self):
        while self.base in self.rcvpkt.keys():
            self.receiving_app.deliver_data(self.rcvpkt[self.base].payload)
            del self.rcvpkt[self.base]
            self.base = (self.base+1) % self.K
