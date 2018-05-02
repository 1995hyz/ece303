# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator
import utils
import random
import binascii
import math


class Sender(object):
    TEST_DATA = bytearray([68, 65, 84, 65, 80, 79, 79, 80, 81, 82])  # some bytes representing ASCII characters: 'D', 'A', 'T', 'A'
    BUFF = 256 
    MSS = 4
    SEG = int(math.ceil(len(TEST_DATA)/float(MSS)))
    PCKG = 0
    seqnum = random.randint(0, 255)
    j = 0
    k = MSS

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

        for seg in self.splitter(self.TEST_DATA,self.MSS,self.PCKG):
            try:
                segment = Segment(checksum=0,seqnum=0,acknum=0,data=seg)
                segment.seqnum = Segment.seqnum(self,self.seqnum,seg)
                self.seqnum=segment.seqnum
                segment.acknum = Segment.acknum(self,1)
                byteArray = bytearray([segment.checksum, segment.acknum, segment.seqnum])
                byteArray += seg
                segment.checksum = Segment.checkSum(self,byteArray)
                byteArray[0]=segment.checksum       #update checksum to new calculated value
                print (segment)
                self.simulator.put_to_socket(byteArray)       #send data
            except socket.timeout:
                pass

#       def checkCheckSum(self,data,ReceivedCS):        #this function calulates the checkSum of the RECEIVED data  
 #       byteData=bytearray(data)
  #      xorSum=bytes(ReceivedCS)        #ReceivedCS should be an "one byte" object, the same type as xorSum in checkSum function     
   #     for i in xrange(len(byteData)):
    #        xorSum^=byteData[i]
     #   if xorSum==225:         #if xorSum is 11111111, the data is not corrupted
      #      return True
       # else:
        #    return False

    def splitter(self, data, MSS, PCKG):

        for i in range(self.SEG):
            PCKG = PCKG + 1
            yield data[self.j:self.k]
            self.j = self.j+MSS
            self.k = self.k+MSS        
    
class Segment(object):
    def __init__(self,checksum=0,seqnum=0,acknum=0,data=[]):
        self.checksum = checksum
        self.seqnum = seqnum
        self.acknum = acknum
        self.data = data

    def toArray(self):
        print bytearray(self.seqnum) #bytearray(self.acknum) + bytearray(self.acknum) + bytearray(self.checksum) 

    @staticmethod
    def seqnum(self,lastseqnum,data):
        return (lastseqnum + len(data))%255
    
    @staticmethod
    def acknum(self,isSender):
        if isSender:
            return 0
        else:
            return self.seqnum + MSS    
    @staticmethod
    def checkSum(self,data):        #this function converts data into a bytearray, and does a XOR sum on each elements of the byte-array. Return the invert of the XOR sum
        byteData=bytearray(data)
        print "Lenth of data is "
        print len(byteData)
        xorSum=0
        for i in xrange(len(byteData)):
            print "byte value: "
            print bin(byteData[i])
            xorSum=byteData[i]^xorSum
            print bin(xorSum)
        return xorSum
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

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
    sndr = Sender()
    sndr.send(Sender.TEST_DATA)
