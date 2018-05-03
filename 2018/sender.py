# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator
import utils
import random
import binascii
import math


class Sender(object):

    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=10, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


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

class MySender(BogoSender):
    #TEST_DATA = "HELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAHHELLO YINGZHI I AM ABDULLAH END"
    file_open=open("./Test_Input.txt",'rb')
    TEST_DATA=file_open.read()
    BUFF = 256 
    MSS = 250
    SEG = int(math.ceil(len(TEST_DATA)/float(MSS)))
    PCKG = 0
    seqnum = random.randint(0, 255)
    while seqnum == (BUFF-MSS):
        seqnum = random.randint(0,255)
    j = 0
    k = MSS
    dupCount = 0
    packageSent = False
    resend=False

    buffer = bytearray(BUFF) # circular array - max size 256
    buffer_start = seqnum # start index of buffer
    buffer_end = seqnum # end index of buffer

    def __init__(self, timeout=0.1):
        super(MySender, self).__init__()
        self.timeout = timeout
        self.simulator.sndr_socket.settimeout(self.timeout)

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))      

        for seg in self.splitter(self.TEST_DATA,self.MSS,self.PCKG):
            try:
                if not self.resend:
                    segment = Segment(checksum=0,seqnum=0,acknum=0,data=seg)
                    segment.seqnum = Segment.seqnum(self,self.seqnum,seg,self.MSS)
                    self.seqnum=segment.seqnum
                    segment.acknum = Segment.acknum(self,1)
                    byteArray = bytearray([segment.checksum, segment.acknum, segment.seqnum])
                    byteArray += seg
                    segment.checksum = Segment.checkSum(self,byteArray)
                    byteArray[0]=segment.checksum       #update checksum to new calculated value
                    self.simulator.u_send(byteArray)       #send data

                # Handle acks
                while True:
                    # we receive: ([ackPackage.checksum,ackPackage.acknum])
                    receivedByteArray = self.simulator.u_receive()

                    if self.checkCheckSum(receivedByteArray): # ack not corrupted
                        if len(receivedByteArray) == 3 or receivedByteArray[1] == self.seqnum:
                            self.packageSent = True
                            self.simulator.u_send(byteArray)                            
                        elif receivedByteArray[1] == (self.seqnum + len(seg))%256: # no error
                            self.dupCount = 0
                            if self.timeout > 0.1:
                                self.timeout -= 0.1
                            self.simulator.sndr_socket.settimeout(self.timeout)
                            self.resend=False
                            break
                        else: # error
                            self.simulator.u_send(byteArray) # resend data 
                    else:
                        self.simulator.u_send(byteArray) # resend data 
                        self.dupCount+=1
                        if self.dupCount == 3 and self.packageSent:
                            self.timeout*=2
                            self.simulator.sndr_socket.settimeout(self.timeout) 
                            self.dupCount = 0
                            if self.timeout>10:
                                print("Timeout has occurred!")
                                exit()                                                            
            except socket.timeout:
                self.resend = True
                self.simulator.u_send(byteArray)
                self.dupCount += 1
                if self.dupCount >= 3:
                    self.dupCount = 0
                    self.timeout *= 2
                    self.simulator.sndr_socket.settimeout(self.timeout)
                    if self.timeout > 10:
                        print("Timeout has occurred!")
                        exit()

            

    #@staticmethod
    def checkCheckSum(self,data):        #this function calulates the checkSum of the RECEIVED data  
        xorSum=~data[0]         #checkSum is at data[0]
        for i in xrange(1,len(data)):
            xorSum^=data[i]
        if xorSum==-1:         #if xorSum is 11111111, the data is not corrupted
            return True
        else:
            return False

    def splitter(self, data, MSS, PCKG):

        for i in range(self.SEG):
            PCKG = PCKG + 1
            yield data[self.j:self.k]
            self.j = self.j+MSS
            self.k = self.k+MSS  

    def _fillBuffer(self,data):
        for byte in data:
            self.buffer[self.buffer_start] = byte
            self.buffer_end += 1
            self.buffer_end %= 256

    # returns empty spots in buffer
    def _bufferNumOpenSpots(self):
        return (buffer_end - buffer_start)%BUFF

class Segment(object):
    def __init__(self,checksum=0,seqnum=0,acknum=0,data=[]):
        self.checksum = checksum
        self.seqnum = seqnum
        self.acknum = acknum
        self.data = data

    @staticmethod
    def seqnum(self,lastseqnum,data,MSS):
        return (lastseqnum + MSS)%256
    
    @staticmethod
    def acknum(self,isSender):
        if isSender:
            return 0
        else:
            return self.seqnum + MSS    
    @staticmethod
    def checkSum(self,data):        #this function converts data into a bytearray, and does a XOR sum on each elements of the byte-array. Return the invert of the XOR sum
        byteData=bytearray(data)
        xorSum=0
        for i in xrange(len(byteData)):
            xorSum=byteData[i]^xorSum
        return xorSum
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


if __name__ == "__main__":
    sndr = MySender()
    sndr.send(MySender.TEST_DATA)
