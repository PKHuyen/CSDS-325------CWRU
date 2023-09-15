import socket
import sys
from RDTSocket import RDTSocket
class Sender:
    #Initiate new sender with receiver's address and port number. Sender have a maximum windowSize packets can be sent at the same time
    def __init__(self, host, port, windowSize):
        self.host = host
        self.port = port
        self.windowSize = windowSize
        self.socket = RDTSocket(self.windowSize)
        
    #Reading the alice.txt file
    def readFile(self):
        f = open("alice.txt", "r")
        self.data = f.read()
        self.socket.connect((socket.gethostbyname(socket.gethostname()), self.port))
        self.socket.send(self.data)
        f.close()

#Run sender.py
if __name__ == '__main__':
    newSender = Sender(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    newSender.readFile()

