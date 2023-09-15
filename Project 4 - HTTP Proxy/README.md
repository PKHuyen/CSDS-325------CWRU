CSDS 325 - Project 4 (Optional) - HTTP Proxy
Author: Harley Phung
Professors: An Wang and Vipin Chaudhary
Case Western Reserve University

This project is written in Java with the help from https://www.ece.ucdavis.edu/~chuah/classes/eec173a/code.html.
This project is written on Ubuntu 22.04 and tested on Ubuntu 22.04 and MacOS. Therefore, please use this operating system or MacOS to run the program to make sure it run correctly.

1. Proxy.java
- This is the proxy server that support a subset of the HTTP standard. It forwards HTTP Get requests and support basic portions of standard, 
- Do not need to suppor persistent connections (request pipelining, or other, advanced portions of the standard)
- Handle HTTP requests where a single request/response pair is sent over a single TCP connections. 
- Methods:
    + Proxy(): Constructor, create a socket and remembered in the class
    + init() : Initiate a new TCP connection, then receive request from the client (terminal), and forward that request to the server (based on http that client gives). Receive response from the server and forward that response to client. Finally close connections, waiting for next request
    + main(): Run the proxy server.

2. To run the program, please make sure that your computer has downloaded wget. 
    + To check if wget has been downloaded: go to terminal, enter command "wget".
    + If shown "wget: missing URL", it means your operating system has wget. Else, update, then download wget by "sudo apt-get wget".

- After finished downloading wget, open 2 terminals. One of them is used to run the proxy server. 
    + Step 1: Compile "javac Proxy.java"
    + Step 2: Run "java Proxy"
    + If you saw Listening on port 9099, server is running, you are ready to test Proxy
The second Terminal is used to test proxy. In this example, I will use this HTTP URL to test: http://engineering.case.edu/eecs. This means we want to get access to http://engineering.case.edu, and all information that server sent back is stored in a file named eecs.
    + Step 1: Type "bash"
    + Step 2: Type "export http_proxy=http://127.0.0.1:9099 && wget http://engineering.case.edu/eecs. 
    Take a look at the result after output has been printed. If you see "eecs ===== 100%, it means all of your response has been recorded to eecs.
    + Step 3: Type "export http_proxy="" && wget http://engineering.case.edu/eecs"
    Take a look at the result after output has been printed. If you see "eecs.1 ==== 100%, it means all of your response has been recoreded to eecs.1 file. It has eecs.1 because this file did not override eecs file. Therefore, it had to add postfix to differentiate the 2 files.
    + Step 4: Compare the 2 files: "diff eecs eecs.1". If there's no output in the terminal, the program works correctly.

3. NOTE: 
If there's any step did not works on your machine, please reach out to me via Gmail: hkp15@case.edu.