import socket
import sys
import os
from RDTSocket import RDTSocket
class Receiver:
    #Initiate a new Receiver with address and port number binded. Receiver have maximum windowSize received packets at the same time
    def __init__(self, receiverPort, windowSize):
        self.receiverHost = socket.gethostbyname(socket.gethostname())
        self.receiverPort = receiverPort
        self.windowSize = windowSize
        self.socket = RDTSocket(self.windowSize)
        self.socket.bind(self.receiverHost, self.receiverPort)

        #While in the connection, open download.txt file and ready to write received data.
        while self.socket.accept():
            fileName = open("download.txt", "w")
            while True:
                received = self.socket.recv()
                b = received[0]
                buffer = ""
                for i in b:
                    buffer += i.decode()
                fileName.write(buffer)
                if received[1] == -1:
                    break
            fileName.flush()
            os.sync()
            fileName.close()
#Run receiver.py
if __name__ == '__main__':
    newReceiver = Receiver(int(sys.argv[1]), int(sys.argv[2]))