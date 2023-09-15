import sys
import socket
import select

class ChatClient:
    #Initiate a new client that send data to host and port number 
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clientSocket = None

    #Create a new socket and send a GREETING message. This message is to register client into server.
    def createClient(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.sendto("greeting".encode(), (self.host, self.port))

    #Send message to host and port obtained previously
    def sendMessage(self, message):
        try:
            sent = 0
            messageEncoded = message.encode()
            while sent < len(messageEncoded):
                sent += self.clientSocket.sendto(messageEncoded[sent:], (self.host, self.port))
        except Exception as e:
            pass

    #Receive message from server and print out (Other clients message)
    def receiveMessage(self):
        try:
            receivedMessage, address = self.clientSocket.recvfrom(4096)
            print(receivedMessage.decode())
        except Exception as e:
            pass

    #Interact between client and server. Use select() to always read socket
    def interact(self):
        while True:
            print(">")
            readables, writeables, errors = select.select([sys.stdin, self.clientSocket], [], [])
            # Check if readables existed. len(readables) = 0 means not existed.
            if len(readables) == 0:
                continue
            else:
                #Check if readable is client's input or server's message. If readable is a socket, then it is message from server
                # Else, it is message to send to the server
                readable = readables[0]
                if isinstance(readable, socket.socket):
                    self.receiveMessage()
                else:
                    self.sendMessage(readable.readline())

#Run the program
if __name__ == '__main__':
        client = ChatClient(sys.argv[1], int(sys.argv[2]))
        client.createClient()
        client.interact()
