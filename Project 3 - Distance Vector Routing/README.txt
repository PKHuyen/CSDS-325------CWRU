Project 3 - Distance Vector Routing Algorithm
Author: Harley Phung 
CSDS 325 - Computer Networks
Professor: An Wang and Vipin Chaudhary
Case Western Reserve University 

1. Overview:
- This program is written in Java, and make use of HashMap while implementing distance vector routing algorithm (Bellman-Ford)
- For further information about coding, comments give out more information about my intention in the code

2. Main class: 
    a. Server.java: To create a new Server. 
    - accept(): To accept the JOIN request from all routers available. Only when all routers have joined, the program can be continued.
    - update(): To deal with update request from routers after they have finished filling their table
    - terminate(): To disconnect Server with all routers. Triggered by timeout 2000 miliseconds (2 seconds)
    - main(): Run the program

    b. Router.java: This class defined action for each specific router can do. Similar to abstract class
    - connect(): To send JOIN message to the server and receive RESPONSE from server to update that router's table
    - update(): To send out UPDATE message to the server and wait for other's routers update request (forwarded by server)
    - printTable(): To print out table that have format <destination router, cost>
    - drive(): Since Router is an abstract class, this acts similarly to main(). Run the program

    Router.java contains RouterU, RouterV, RouterW, RouterX, RouterY, RouterZ

3. Helper class:
    a. Message.java: This class identifies the message information, have ability to send, receive between sockets
    b. Type.java: Enum, contain JOIN, RESPONSE, UPDATE, TERMINATE
    c. Run.java: Help compile Router without going into network package
    
4. HOW TO RUN THE PROGRAM:
- This program is written and run on Linux machine, please use compatiable operating system to run this program.
You can use either localhost (if your operating system is Linux based, preferably Ubuntu) or use virtual machine 
(eecslab-1.case.edu if you are a student from Case Western Reserve University).
- If your code did not compile at first, please wait for 5 minutes for the project to run properly.
To compile: Use     javac *.java
NOTE: Check folder message and network to see if there's .class extension. If yes, you are ready to run the program.
If not, please use the same code    javac *.java    to compile these script.
- To run the program, please follow these step. There are 2 methods you can do this:
    + Method 1: Using terminal, open 7 terminals (if there are 6 routers in the configuration). Make sure you in correct directory
        Step 1: java Server
        For each router in terminal from 2 to 7:
            Step 2: cd network
            Step 3: java RouterU //Change RouterU to RouterV, RouterW, etc in other terminals.
    + Method 2: Using terminal, open 7 terminals (if there are 6 routers in the configuration). Make sure you in correct directory
        Step 1: java Server
        For each router in terminal from 2 to 7:
            Step 2: java network/RouterU ////Change RouterU to RouterV, RouterW, etc in other terminals.

5. If there's another use cases to test:
- Change configurationPath.txt to your use case but make sure to format it similar to original table
- Change RouterU, RouterV, RouterW, RouterX, RouterY, RouterZ to corresponding name of new configuration, but make sure to format it similar to 
origianl Router.