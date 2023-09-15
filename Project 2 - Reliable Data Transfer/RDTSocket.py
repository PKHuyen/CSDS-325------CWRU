import random
import time
from util import UnreliableSocket
from util import PacketHeader
from util import compute_checksum
from util import verify_packet

#RDTSocket inherit UnreliableSocket functions. 
class RDTSocket(UnreliableSocket):
    #Initiate a new RDTSocket, call socket by super() from UnreliableSocket.
    #windowSize is the maximum packets can be sent/received at the same time, initiate in Terminal
    #receiverAddress is the permanent address of receiver (including IP, and port number). Cannot change during connection
    #senderAddress is the address of receiver (including IP, and port number). Cannot change during connection, after disconnect can be changed
    #expectedToReceive is the variables to keep checking the packet's sequence number sent by sender (used by receiver)
    #expectedACK is the variable to keep checking the header's sequence number sent by receiver (used by sender)
    def __init__(self, windowSize):
        super().__init__()
        self.windowSize = windowSize
        self.senderAddress = None
        self.receiverAddress = None
        self.expectedToReceive = 0
        self.expectedACK = 0
        if self.windowSize <= 0:
            print("No window initiated, disconnect")
            self.close()

    #Helper method to check the senderAddress.
    def check_sender(self, sender_address):
        #Currently no sender, add any first come sender.
        if self.senderAddress == None:
            self.senderAddress = sender_address
            return True
        #Currently have a sender, and match with address retrieved by recvfrom()
        elif self.senderAddress == sender_address:
            return True
        #Currently have a sender, but not match with address retrieved by recvfrom()
        else:
            return False

    #accept(), called by receiver, to send START_ACK back to sender and establish the connection
    def accept(self):
        try:
            #Listening to the request
            while True:
                #Only receive the packet header from sender
                header = b''
                while len(header) < 16:
                    message, sender_address = self.socket.recvfrom(16 - len(header))
                    header += message
                #Only continue if the sender_address match
                if self.check_sender(sender_address) == True:
                    self.senderAddress = sender_address
                    pType = int.from_bytes(header[:4], 'big')
                    pSeqNum = int.from_bytes(header[4:8], 'big')
                    
                    #Only continue if the received header is a START type.Create a ACK header with same sequence number and send
                    if pType == 0:
                        ackHeader = PacketHeader(3, pSeqNum, 0, 0)
                        ackHeader = ackHeader.to_bytes()
                        sent = 0
                        self.expectedToReceive = pSeqNum + 1
                        while sent < 16:
                            sent += self.socket.sendto(ackHeader[sent:], sender_address)
                        return sender_address
        except Exception as e:
            raise e

    #connect(), called by sender to send START message and wait for ACK from receiver. If there's a timeout (START message got lost
    # or ACK message got lost), resent START message to same receiver.
    def connect(self, address):
        #Create a header with random number
        pSeqNum = int(random.random() * 10000)
        header = PacketHeader(0, pSeqNum, 0, 0)
        header = header.to_bytes()
        startTime = 0
        try:
            while True:
                #If not send yet or timeout, resend START
                if startTime == 0 or time.time_ns() - startTime > 500*1e6:
                    sent = 0
                    while sent < 16:
                        sent += self.socket.sendto(header[sent:], address)
                    startTime = time.time_ns()

                #Wait for ACK
                ackHeader = b''
                while len(ackHeader) < 16:
                    message, receiver_address = self.socket.recvfrom(16 - len(ackHeader))
                    ackHeader += message
                #If the receive message is from expected receiver and the type is correct (ACK), continue
                if address == receiver_address:
                    ackType = int.from_bytes(ackHeader[:4], 'big')
                    ackNum = int.from_bytes(ackHeader[4:8], 'big')
                    if ackType == 3 and ackNum == pSeqNum:
                        self.receiverAddress = receiver_address
                        self.expectedACK = pSeqNum + 1
                        break
        except Exception as e:
            raise e

    #Helper method to split data sender wants to send. With each of the splitted packet, add corresponding type, 
    # sequence number, length of payload, checksum of payload.
    # Since Ethernet support at most 1500 bytes, IP protocol uses 20 bytes, UDP header uses 8 bytes, the whole packets uses 1472 bytes.
    # Header uses 16 bytes with 4 bytes each segment, therefore, payload is 1456 bytes maximum.
    def splitData(self, typeSend, seqNum, data):
        data = data.encode()
        chunks = [data[i : i + 1456] for i in range (0, len(data), 1456)]
        allPacket = []

        for datachunk in chunks:
            preChecksum = compute_checksum(datachunk)
            header = PacketHeader(typeSend, seqNum, len(datachunk), preChecksum)
            header = header.to_bytes()
            packet = header + datachunk
            allPacket.append(packet)
            seqNum += 1
        
        return allPacket

    #send(), implementign sendto() from UnreliableSocket
    #wRange is the range that a packet can be accepted at a time, if it's out of range, ignore that packet.
    #wIndex is the index in window
    #window is the sender window, containing packets that are sending 
    #wACK is the confirmation window, to let the sender knows that packets it's sending has been received by the receiver
    def send(self, data):
        allPacket = self.splitData(2, self.expectedACK, data)
        self.expectedACK += 1
        wRange = range(self.expectedACK, self.expectedACK + self.windowSize)
        wIndex = range(0, self.windowSize)
        window = [None] * self.windowSize
        wACK = [None] * self.windowSize
        
        #Send all packet in window
        for i in wIndex:
            if len(allPacket) != 0:
                window[i] = allPacket[0]
                self.socket.sendto(window[i], self.receiverAddress)
                allPacket.pop(0)

        #Wait for ACK
        try:
            while True:
                ackHeader = b''
                message, receiver_address = self.socket.recvfrom(16)
                ackHeader += message
                #Only proceed if receive message from correct receiver
                if self.receiverAddress == receiver_address:
                    pType = int.from_bytes(ackHeader[:4], 'big')
                    pSeqNum = int.from_bytes(ackHeader[4:8], 'big')
                    startTime = time.time_ns()
                    #Make sure the received type is an ACK, if else ignore the header
                    if pType == 3 and time.time_ns() - startTime <= 500*1e6:
                        #If sequence number is not expected, buffer to wACK window at correct position then reset timer
                        if pSeqNum != self.expectedACK:
                            if pSeqNum in wRange:
                                wACK[pSeqNum - self.expectedACK] = window[pSeqNum - self.expectedACK]
                                startTime = time.time_ns()

                        #If sequence number if expected, add to wACK window, and iterate expectedACK until wACK out of range
                        #or None. At the same time, add remaining packets to window and send
                        else:
                            for i in range(0, len(wACK)):
                                #Continue to update expectedACK
                                if wACK[i] != None:
                                    self.expectedACK += 1
                                    window.pop(0)
                                    wACK[i] = None
                                    #Make sure there's still packet to send. If out of packet, reset window, ready to close
                                    if len(allPacket) != 0:
                                        window.append(allPacket[0])
                                        self.socket.sendto(allPacket[0], self.receiverAddress)
                                        allPacket.pop(0)
                                        startTime = time.time_ns()
                                    else:
                                        if window == [None] *self.windowSize:
                                            break
                                #Add to wACK, send next packet. If out of packet, close()
                                else: 
                                    wACK[pSeqNum - self.expectedACK] = window[pSeqNum - self.expectedACK]
                                    if len(wACK) <= 1:
                                        wACK[pSeqNum - self.expectedACK] = None
                                        self.expectedACK += 1
                                        if len(allPacket) != 0: 
                                            window.append(allPacket[0])
                                            self.socket.sendto(allPacket[0], self.receiverAddress)
                                            allPacket.pop(0)
                                            startTime = time.time_ns()
                                        else:
                                            self.close()
                                            return
                                    else: 
                                        wACK[pSeqNum - self.expectedACK - 1] = None
                                        self.expectedACK += 1
                                        if len(allPacket) != 0:
                                            window.append(allPacket[0])
                                            self.socket.sendto(allPacket[0], self.receiverAddress)
                                            allPacket.pop(0)
                                        else: 
                                            self.close()
                                            return
                                    startTime = time.time_ns()
                            wRange = range(self.expectedACK, self.expectedACK + self.windowSize)

                    #If there's timeout, resend all packets in the window
                    elif time.time_ns() - startTime > 500*1e6:
                        for i in wIndex:
                            self.socket.sendto(window[i], self.receiverAddress)
                            startTime = time.time_ns()
        except Exception as e:
            raise e

    #recv(), called by receiver, wait for sender's packets and send ACK for next packet
    #window is the received window by receiver
    #wIndex is the index of window
    #wRange is the acceptable range of data that receiver can received at the same time
    #fileName is the array of payload, later used.
    def recv(self):
        window = [None] * self.windowSize
        wIndex = range(0, self.windowSize)
        wRange = range(self.expectedToReceive, self.expectedToReceive + self.windowSize)
        fileName = []
        #Wait for packet
        try:
            while True:
                packet,sender_address = self.socket.recvfrom(1472)
                if self.senderAddress == sender_address:
                    pType = int.from_bytes(packet[:4], 'big')
                    pNum = int.from_bytes(packet[4:8], 'big')
                    pLength = int.from_bytes(packet[8:12], 'big')
                    pChecksum = int.from_bytes(packet[12:16], 'big')
                    payload = packet[16:16+pLength]

                    #Only proceed if the packet is DATA type and checksum is correct
                    if pType == 2:
                        if verify_packet(pChecksum, payload) == True:
                            #If the received sequence number is not expected, in range, and not received before, continue. If not in range ignore.
                            if pNum != self.expectedToReceive:
                                if pNum in wRange:
                                    #Add the payload to correct window index, send the header of expected sequence number.
                                    if window[pNum - self.expectedToReceive] == None:
                                        window[pNum - self.expectedToReceive] = payload
                                        header = PacketHeader(3, self.expectedToReceive, 0, 0)
                                        header = header.to_bytes()
                                        sent = 0
                                        while (sent < 16):
                                            sent += self.socket.sendto(header[sent:], self.senderAddress)
                                    #Pass
                                #Pass
                            #If expected then only goes to window[0] because pNum = self.expectedToReceive
                            else: 
                                if window[0] == None: 
                                    #Add payload to first index of window, iterate until window[i] = None, at the same time add payload to fileName to store data
                                    window[0] = payload
                                    for i in wIndex:
                                        if window[i] != None:
                                            self.expectedToReceive += 1
                                            fileName.append(window[i])
                                            window[i] = None
                                        else:
                                            wRange = range(self.expectedToReceive, self.expectedToReceive + self.windowSize)
                                    header = PacketHeader(3, self.expectedToReceive, 0, 0)
                                    header = header.to_bytes()
                                    sent = 0
                                    while sent < 16:
                                        sent += self.socket.sendto(header[sent:], self.senderAddress)
                    #If receive the END message, send back ACK for that END message.
                    elif pType == 1:
                        while True:
                            header = PacketHeader(3, pNum, 0, 0)
                            header = header.to_bytes()
                            sent = 0
                            while sent < 16:
                                sent += self.socket.sendto(header[sent:], self.senderAddress)
                            self.senderAddress = None
                            self.expectedToReceive = 0
                            self.expectedACK = 0
                            return fileName, -1
                            
        except Exception as e:
            raise e

    #close(), called by sender, to disconnect from receiver. If timeout but not receive correct ACK, resend the message.
    def close(self):
        pSeqNum = self.expectedACK
        header = PacketHeader(1, pSeqNum, 0, 0)
        header = header.to_bytes()
        sent = 0
        while sent < 16:
            sent += self.socket.sendto(header[sent:], self.receiverAddress)
        startTime = time.time_ns()

        while True:
            if time.time_ns() - startTime > 500*1e6:
                sent = 0
                while sent < 16:
                    sent += self.socket.sendto(header[sent:], self.receiverAddress)
                    startTime = time.time_ns()

            ackHeader = b''
            message, receiver_address = self.socket.recvfrom(16)
            ackHeader += message
            if self.receiverAddress == receiver_address:
                ackType = int.from_bytes(ackHeader[:4], 'big')
                ackNum = int.from_bytes(ackHeader[4:8], 'big')
                if ackType == 3 and ackNum == pSeqNum:
                    self.receiverAddress = receiver_address
                    self.expectedACK = pSeqNum + 1
                    break
