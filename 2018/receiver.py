# Written by S. Mevawala, modified by D. Gitzel

import logging

import channelsimulator
import utils


class Receiver(object):

    def __init__(self, inbound_port=50005, outbound_port=50006, timeout=10, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

    def receive(self):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoReceiver(Receiver):
    ACK_DATA = bytes(123)

    def __init__(self):
        super(BogoReceiver, self).__init__()

    def receive(self):
        self.logger.info("Receiving on port: {} and replying with ACK on port: {}".format(self.inbound_port, self.outbound_port))
        while True:
            data = self.simulator.get_from_socket()  # receive data
            self.logger.info("Got data from socket: {}".format(
                data.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
            self.simulator.put_to_socket(BogoReceiver.ACK_DATA)  # send ACK

class MyReceiver(BogoReceiver):
    RE_DATA=bytearray()
    lastacknum = -1 # initialized to -1 to signify first packet

    def __init__(self):
        super(MyReceiver, self).__init__()

    def receive(self):
        while True:
            # print("Before u_receive")
            self.RE_DATA=self.simulator.u_receive()
            # print("After u_receive")
            self.send();

    def send(self):
        ackPackage=Segment()
        ack_success = ackPackage.ack(self.RE_DATA,self.lastacknum)
        if ack_success:
            self.lastacknum = ackPackage.acknum
        if ackPackage.acknum < 0:
            ackPackage.acknum = 0 # we set it to 0 here, it may be set back to -1
        ackPackage.checksum = ackPackage.checkSum()
        print("acknum: {}".format(ackPackage.acknum))
        print("lastacknum: {}".format(self.lastacknum))
        byteArray=bytearray([ackPackage.checksum,ackPackage.acknum])
        self.simulator.u_send(byteArray)

class Segment(object):
    def __init__(self,checksum=0,seqnum=0,acknum=0,data=[]):
        self.checksum = checksum
        self.seqnum = seqnum
        self.acknum = acknum
        self.data = data
         
    def checkSum(self):        #Since the segament of receiver only has ACK number in it, the checkSum value will just be the ACK number
        return self.acknum
        
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    #@staticmethod
    def checkCheckSum(self,data):        #this function calulates the checkSum of the RECEIVED data  
        xorSum=~data[0]        #checkSum is at data[0]
        for i in xrange(1,len(data)):
            xorSum^=data[i]
        if xorSum==-1:         #if xorSum is 11111111, the data is not corrupted
            return True
        else:
            return False
    
    #@staticmethod
    def ack(self,data,lastacknum):
        isGood = self.checkCheckSum(data)
        if isGood:
            self.acknum=(data[2]+len(data[3:]))%256
            # if self.acknum > lastacknum or data[2]+len(data[3:]) >=256:
                # print("Payload: {}".format(data[3:]))
            print("Rec seqnum: {}".format(data[2]))
            if data[2] == lastacknum or lastacknum == -1:
                print("--------Payload: {}".format(data[3:]))
                return True

        else:
            print("corrupted")

        return False
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)



if __name__ == "__main__":
    rcvr = MyReceiver()
    rcvr.receive()
