Author: Harley Phung
Professor: An Wang and Vipin Chaudhary
Course: CSDS 325 - Computer Networks, Case Western Reserve University

1. util.py
- This file contains 2 classes and 2 methods.
a. UnreliableSocket is the class that initiate the socket that links to the Unreliable Network between a server and a clients. Including the implementation of: 
- bind(): To assign an address and port number to the receiver (server) socket
- recvfrom(): To receive the packets from unreliable network. Simluate the 10% packet loss, the 10% packet delay, and the 10% data corruption
- sendto(): To send packets to unreliable network, the return value is number of bytes data has been sent
- close(): To disconnect the socket.

b. PacketHeader is the class that create a new header, containing data that UDP protocol required to make the receiver understands it's information. These information includes: type, sequence number, length of data, and checksum. A PacketHeader must have these 4 information. 

c. compute_checksum() is the method of util.py to calculate crc32 checksum of data.

d. verify_packet() is the method of util.py to compute between received checksum and payload checksum

2. RDTSocket.py
RDTSocket is the reliable socket that is required to receive data from Application layer and send to the unreliable network.
- accept(): Is the method invoked only by the receiver. If the receiver are waiting for a new connection, whenever the first sender request to connect, it accept,send a header with similar sequence number and ignore others' connection. 
- connect(): Is the method invoked only by the sender. To establish connection, sender must send START message, and wait for that START_ACK. If timeout, the sender did not receive ACK, it must be ACK message has been lost or START hasn't make it to the receiver, send again.
- send(): Is the method invoked only by the sender. To continuously sending data to receiver, then wait for each of the packet's ACK. Have appropriate behavior when there's packet loss, or timeout.
- recv(): Is the method invoked only by the receiver. To wait for data, and send back ACK to sender.
- close(): Is the method invoked only by the sender. To send END message, and wait for the END_ACK. If received END_ACK, receiver removes sender as a client, and listens to next request.

3. sender.py
To initiate the sender that have input host address, port number, sender window size. 
To call functions in RDTSocket.
The sender automatically disconnect from receiver after the content of file has been sent.

4. receiver.py
To initiate the receiver that have input port number, receiver windowsize. Call functions in RDTSocket.
The receiver cannot disconnect itself after receive a packet from sender. Have to wait for next sender to send their package.
To disconnect receiver, use Ctrl + C to cause KeyboardInterrupt.

5. HOW TO RUN THE PROGRAM
This program only takes file named "alice.txt" to works for the sender. If want to send another file, go to sender.py, line 14, change to    f = open("<file name>", "r"). Similarly, this program only output the "download.txt" file. If want to change file name, go to receiver.py, line 16, change to   fileName = open("<file name>", "w")

- To run this program, the machine must be Linux (Ubuntu is suggested) and python version must be at least 3.0. To check the version of your current python: 
    python --version 
    or 
    python3 --version.
If the output is not 3.*, please update version of python using the following URL: https://www.python.org/downloads/ 

If the output is 3.*, run this program as following (Please follow the syntax strictly):
- First: Check the local host name, and use the output for third step:
    hostname
- Second, initiate the receiver: 
    python3 receiver.py <port number> <windowSize>
- Third, initiate the sender:
    python3 sender.py <hostname> <port number> <windowSize>

After the sender disconnect, check your files name with the download.txt (a file records received data from sender):
    diff download.txt <your_file_name>
