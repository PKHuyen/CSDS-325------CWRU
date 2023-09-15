import sys
import socket

class ChatServer:
        # Initiate the ChatServer. 
        def __init__(self, serverPort):
                self.serverPort = serverPort
                self.serverSocket = None
                
        # Create new socket and bind that socket to the server
        def createServer(self):
                self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.serverSocket.bind((socket.gethostbyname(socket.gethostname()), self.serverPort))
                self.clientList = []

        # To receive the message from client, process the message, then call sendMessageToClient
        def receiveMessageFromClient(self, message, clientAddress):
                message = message[:-1]
                clientIP, clientPort = clientAddress
                self.addOnMessage = "<From " + str(clientIP) + ":" + str(clientPort) + ">: "
                self.modifiedMessage = self.addOnMessage + str(message)
                self.sendMessageToClient(self.modifiedMessage)

        # To send message to all clients that are on client list, including the one who sent the message.
        def sendMessageToClient(self, message):
                try:
                    for c in self.clientList:
                        sent = 0
                        encodedMessage = message.encode()
                        while sent < len(encodedMessage):
                            sent += self.serverSocket.sendto(encodedMessage, c)
                except Exception as e:
                    pass

        # Wait client, if there's new connection, then add to the clientList. The client list can later be used to send message back to all clients in the list. Call receive message
        def waitClient(self):
                while True:
                        message, clientAddress = self.serverSocket.recvfrom(2048)
                        if clientAddress not in self.clientList:
                                self.clientList.append(clientAddress)
                        if message.decode() != "greeting":
                                self.receiveMessageFromClient(message.decode(),(clientAddress))

        # Initiate the Server
if __name__ == '__main__':
                server = ChatServer(int(sys.argv[1]))
                server.createServer()
                print("Server Initilized...")
                server.waitClient()

