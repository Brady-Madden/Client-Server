import socket
import os
import subprocess
import sys
import time
#command line argument
#server_tcp.py controlport dataport
if len(sys.argv) != 3:
    print("Wrong Number of Args for server TCP")
    sys.exit()
else:
    #as per specifications of the assignment
    controlport = int(sys.argv[1])
    dataport = int(sys.argv[2])
    host = 'localhost'
    #create TCP sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    fs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #assign addr to respective port to bind to sockets
    server_addr = (host, controlport)
    file_addr = (host, dataport)
    #bind addr to the socket
    s.bind((server_addr))
    fs.bind((file_addr))
    #listens for a connection from client
    s.listen(5)
    fs.listen(5)
    #while listening
    while True:
        #accept connection on socket
        conn, client_addr = s.accept()
        conn2, addr = fs.accept()
        print('Connected by', client_addr)
        #while connected
        while True:
        #cmd receieved from client
            cmd = conn.recv(1024).decode()
            #split so it can be manipulated
            command = cmd.split()
            #FTP COMMANDS
            if command[0] == 'cd':
                #set directory name
                direc = command[1]
                try:
                    #os command for changing direc
                    os.chdir(direc)
                    msg = 'cd ACK'
                    #send cd ACK
                    conn.send(bytes(msg.encode()))
                    print('cd ACK sent to client')
                    #new directory
                    print('Directory has been changed to', direc)
                except (NotADirectoryError, FileNotFoundError):
                    print('Directory Not Found')
                    msg = 'cd Error'
                    #send cd error message
                    conn.send(bytes(msg.encode()))

            if command[0] == 'ls':
                #set direc to name of directory
                direc = command[1]
                ls_ACK = 'ls ACK'
                #send the ls ACK to client
                conn.sendall(bytes(ls_ACK.encode()))
                print('ls ACK sent to client')
                try:
                    #os command for list direc
                    F = os.listdir(direc)
                    #create a list to put the ls result into
                    direc_list = []
                    #read ls results
                    for file in F:
                        #put data into list
                        direc_list.append(file)
                    #convert list to string so it can be sent to client
                    direc_str = str(direc_list)
                    #send ls result to client
                    conn.sendall(bytes(direc_str.encode()))
                    print('ls result sent to client')
                except (NotADirectoryError, FileNotFoundError):
                    print('The requested directory could not be found')
                    msg = 'ls Error'
                    #send error message
                    conn.send(bytes(msg.encode()))

        #GET AND PUT SOURCED FROM
        #https://github.com/pratiklotia/Client-Server-Fast-File-Transfer-using-UDP-on-Python/blob/master/server/server.py
        #Created on Sep 17, 2016#
        #@author: prati
                                  
            if command[0] == 'get':
                #set the file name
                file_name = command[1]
                print("Sending Acknowledgment of command.")
                #get ACK to start
                msg = "Valid Get command. Let's go ahead "
                conn.send(bytes(msg.encode()))
                print("Message Sent to Client.")
                if os.path.isfile(file_name):
                    #file ACK
                    msg = "File exists. Let's go ahead "
                    #sends the ack about file
                    conn.send(bytes(msg.encode()))
                    print("Message about file existence sent.")
                    #packet counter
                    c = 0
                    #gets the size of a file
                    sizeS = os.stat(file_name)
                    #gets the number of packets in terms of bytes
                    sizeSS = sizeS.st_size  
                    print("File size in bytes:" + str(sizeSS))
                    #convert to int to send to client
                    NumS = int(sizeSS / 4096)
                    NumS = NumS + 1
                    tillSS = str(NumS)
                    #send packet num to client
                    conn.sendall(bytes(tillSS.encode()))
                    time.sleep(1)
                    #reads for if there are still packets
                    check = int(NumS)
                    #open the file
                    GetRunS = open(file_name, "rb")
                    #while theres still data to be read
                    while check != 0:
                        #read
                        RunS = GetRunS.read(4096)
                        #send file data to client
                        conn.sendall(RunS)
                        time.sleep(1)
                        c += 1
                        check -= 1
                        #print out number of packets
                        print("Packet number:" + str(c))
                        print("Data sending in process:")
                    #close file
                    GetRunS.close()
                    print("Sent from Server - Get function")
                else:
                    msg = "Error: File does not exist in Server directory."
                    #sends error message
                    conn.sendall(bytes(msg.encode()))
                    print("Message Sent.")   

            if command[0] == 'put':
                print("Checking for acknowledgement")
                #recieve get ACK
                get_ack = conn.recv(51200)
                print(get_ack.decode())
                #get is now ready
                print("Inside Client Put")
                #recieve file size ACK
                ClientData = conn.recv(51200)
                if len(ClientData.decode()) < 30:
                    if command[0] == "put":
                        #create a new file names Received_file_name
                        BigC = open('Received_'+command[1], "wb")
                        #count number of packets
                        d = 0
                        #get number of packets
                        CountC = conn.recv(4096)
                        #convert to int
                        print(CountC.decode())
                        tillCC = int(CountC)
                        print("Receiving packets will start now if file exists.")
                        while tillCC != 0:
                            #recieve data chunks
                            ClientBData = conn.recv(51200)
                            #write into new file
                            dataS = BigC.write(ClientBData)
                            d += 1
                            print("Received packet number:" + str(d))
                            tillCC = tillCC - 1
                        #close file
                        BigC.close()
                        print("New Received File, Check contents of Directory")  
    
