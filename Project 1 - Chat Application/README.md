#Project 1: Server - Clients UDP Chat Application

This project main objective is to create a chat application using UDP with server-client and peer-to-peer communication. 
NOTE: In order to compile, this program must be run on Ubuntu. If you do not have Ubuntu, try virtual machine

## ChatServer.py
- This python program is to create a new Chat Server and process the message received from the server and send back to all clients that connected to server.

- Import packages
    + sys: to read the command line
    + socket: to create socket and use socket's functions

- Functions include: 
    + __init__() : To initiate the ChatServer and remember instances.
    + createServer(): To create a new socket, bind the socket to one particular port number from Command Line, and   
                create a new client list that memorize all client's addresses that connected to the server
    + receiveMessageFromClient(): Receive the message from client, change the content of the message with client's IP 
                address and client's port number. Call sendMessageToClient()
    + sendMessageToClient(): Send the message to all clients in the client list (including one's that send the message)
    + waitClient(): Always listen to the socket, if there's new connection, retrieve the message and address to add to 
                client list. Call receiveMessageFromClient()
    + main: Run the program

## ChatClient.py
- This python program is to create a new client that will connect to ChatServer. The message must be input by user, then send to all other clients that also connected to the server.

- Import packages: 
    + sys: to read the command line
    + socket: to create socket and use socket's functions
    + select: To accept messages from both standard input and sockets.
- Functions include:
    + __init__: To initiate the ChatClient.py.
    + createClient(): To create new socket for client to connect to the server. 
    + sendMessage(): To send the message obtained from input to server (address from command line)
    + receiveMessage(): To receive the message that server send (with IP address and port number of sender).
    + interact(): Wait for client's input and server's message.
    + main: Run the program

## About
- My project is written in Python 2.7 using Case's Linux Virtual Machine (eecslab-1.case.edu)
- Libraries included in ChatServer.py are sys, socket. Libraries included in ChatClient.py are sys, socket, select.
- If there's exception in the system (ICMP errors), I choose to ignore them.
- To initiate the command line using Linux virtual machine (Ubuntu terminal) terminal: Make sure you're in correct directory.
    + For ChatServer.py:    
    python ChatServer.py 9099

        where 9099 is the port number that server listens to. If python version is 3.*, in command line, it should be:      
            python3 ChatServer.py 9099

    + For ChatClient.py:   
    python ChatClient.py <hostname> 9099

        where, before running this command, using command hostname to find server name, then run command with found host name. In my Linux virtual machine, it looks like       python ChatClient.py eecslab-1 9099
        If python version is 3.*, in command line, it should be
            python3 ChatClient.py eecslab-1 9099.         

        When you see ">" notation, it means you are ready to type message.

        To create multiple clients, you can open multiple terminal window.

    + If you are the only client connect to the server, you can still see your IP address and port number when the message return. If there are another clients, you can see their message if they send one. 

- To end the program, use "ctrl - C" combination.