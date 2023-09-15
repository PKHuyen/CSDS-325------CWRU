import socket
import random
import time

#UnreliableSocket, containing implemented bind(), recvfrom(), sendto(), close() from socket library
class UnreliableSocket:
    #Initiate a new socket that will send the message through unreliable network (UDP)
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Bind the address and port number to a specific socket (typically receiver/server) so that all sender/client can send to.
    #socketIP is the address of this socket
    #socketPort is the port number of this socket
    def bind(self, host, port):
        self.socketIP = host
        self.socketPort = port
        self.socket.bind((self.socketIP, self.socketPort))

    #Receive the data from unreliable network, can be invoked by both sender and receiver (If have to communicate)
    #Data is receive from the socket
    #address is the sender's address 
    def recvfrom(self, bufferSize, flags=0):
        self.data, self.address = self.socket.recvfrom(bufferSize, flags)

        #Stimulate packet loss
        if random.random() < 0.1:
            self.data = None
            self.address = None

        #Stimulate delay
        elif random.random() < 0.1:
            time.sleep(0.6)

        #Stimulate corruption of data, flip bits
        elif random.random() < 0.1:
            for i in range(len(self.data)):
                self.data[i] ^= 0xff

        return self.data, self.address

    #Send the packet and return the bytes have been sent
    def sendto(self, data, address):
        return self.socket.sendto(data, address)

    #Disconnect
    def close(self):
            self.socket.close()

#PacketHeader is to create the header in each message that send through Unreliable Socket. This prevent the data corruption
class PacketHeader:
    #Initiate a new PacketHeader, containing type of packet, sequence number of packet, length of payload, checksum of payload
    def __init__(self, pType, seq_num, length, checksum):
        self.pType = pType
        self.seq_num = seq_num
        self.length = length
        self.checksum = checksum

    #Helper method to convert PacketHeader to bytes
    def to_bytes(self):
        return self.pType.to_bytes(4, byteorder='big') + self.seq_num.to_bytes(4, byteorder='big') + self.length.to_bytes(4, byteorder='big') + self.checksum.to_bytes(4, byteorder='big')

#Calculate the checksum of the whole packet (include data and packet header). Return 4 byte checksum
def compute_checksum(packet):
    crc32 = 0xffffffff
    for i in range(len(packet)):
        #print(crc32, packet[i])
        crc32 ^= int.from_bytes(bytes(str(packet[i]), "UTF-8"), byteorder='big')
        for j in range(8):
            crc32 = (crc32 >> 1) ^ (0xedb88320)
    return crc32

#Check the integrity of packet.
def verify_packet(ipv4checksum, packet):
    return compute_checksum(packet) == ipv4checksum
