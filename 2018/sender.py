# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator
import utils
import random


class Sender(object):
    TEST_DATA = bytearray([68, 65, 84, 65])  # some bytes representing ASCII characters: 'D', 'A', 'T', 'A'
    SEG = 4
    MSS = len(TEST_DATA)/SEG
    InitialSeqNumber = random.getrandbits(32)

    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=10, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))      

        while True:
            for seg in segmentor(TEST_DATA)
                try:
                    Segment.CreateSeg(seg, NextSeqNum)
                    self.simulator.put_to_socket(data)  # send data

    def checkSum(self,data):        #this function converts data into a bytearray, and does a XOR sum on each elements of the byte-array. Return the invert of the XOR sum
        byteData=bytearray(data)
        xorSum=bytes(0)
        for i in xrange(len(byteData)):
            xorSum^=byteData[i]
        return ~xorSum

    def checkCheckSum(self,data,ReceivedCS):        #this function calulates the checkSum of the RECEIVED data  
        byteData=bytearray(data)
        xorSum=bytes(ReceivedCS)        #ReceivedCS should be an "one byte" object, the same type as xorSum in checkSum function     
        for i in xrange(len(byteData)):
            xorSum^=byteData[i]
        if xorSum==225:         #if xorSum is 11111111, the data is not corrupted
            return True
        else:
            return False

    def segmentor(data, MSS)
        j = 0
        k = MSS
        yield data[j:k]
        i = i+MSS
        k = k+MSS
        

class Segment():
    def __init__(self)

    def CreateSeg(seg, seqnum)
        
        #checksum = 

        #seqnum = 

        #ack = 

        #data = 


        #raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoSender(Sender):
    TEST_DATA = bytearray([68, 65, 84, 65])  # some bytes representing ASCII characters: 'D', 'A', 'T', 'A'

    def __init__(self):
        super(BogoSender, self).__init__()

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        while True:
            try:
                self.simulator.put_to_socket(data)  # send data
                ack = self.simulator.get_from_socket()  # receive ACK
                self.logger.info("Got ACK from socket: {}".format(
                    ack.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                break
            except socket.timeout:
                pass


if __name__ == "__main__":
    # test out BogoSender
    sndr = BogoSender()
    sndr.send(BogoSender.TEST_DATA)
