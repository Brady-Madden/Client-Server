import socket
import os
import subprocess
import sys
import time
#client_tcp.py server_ip controlport dataport
if len(sys.argv) != 4:
    print("Wrong Number of Args for client TCP")
    sys.exit()
else:
    #as per specifications of the assignment
    server_ip = str(sys.argv[1])
    controlport = int(sys.argv[2])
    dataport = int(sys.argv[3])
    #Create client side TCP sockets
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect to the server, should be listening on these ports
    c.connect((server_ip, controlport))
    fc.connect((server_ip, dataport))
    #while connected
    while True:
        #input command prompt
        cmd = input('Enter a Command: ')
        #send cmd to server
        c.send(bytes(cmd.encode()))
        #split so it can be manipulated
        command = cmd.split()
        #FTP COMMANDS
        
        if command[0] == 'cd':
            print('Waiting for ACK')
            #receive cd ACK
            server_resp = c.recv(1024)
            if server_resp.decode() == 'cd ACK':
                #if received cd works
                print('Current Directory is: ' , command[1])
            if server_resp.decode() == 'cd Error':
                #if receieved cd has failed
                print('Directory Not Found')

        if command[0] == 'ls':
            print('Checking for ACK')
            #get ls ACK
            ls_ack = c.recv(1024)
            print(ls_ack)
            if ls_ack.decode() == 'ls ACK':
                print('Getting data from server...')
                #get the ls result form server
                lsresult = c.recvfrom(4096)
                #print result
                print(lsresult)
            if ls_ack.decode() == 'ls Error':
                #if error message was received
                print('The directory you entered could not be found')

            #GET AND PUT SOURCED FROM
            #https://github.com/pratiklotia/Client-Server-Fast-File-Transfer-using-UDP-on-Python/blob/master/server/server.py
            #Created on Sep 17, 2016#
            #@author: prati

        if command[0] == 'get':
            print("Checking for acknowledgement")
            #recieve get ACK
            get_ack = c.recv(51200)
            print(get_ack.decode())
            #get is now ready
            print("Inside Client Get")
            #recieve file size ACK
            ClientData = c.recv(51200)
            print(ClientData.decode())
            if len(ClientData.decode()) < 30:
                if command[0] == "get":
                    #create a new file names Received_file_name
                    BigC = open('Received_'+command[1], "wb")
                    #count number of packets
                    d = 0
                    #get number of packets
                    CountC = c.recv(4096)
                    #convert to int
                    tillCC = int(CountC.decode())
                    print("Receiving packets will start now if file exists.")
                    while tillCC != 0:
                    #recieve data chunks
                        ClientBData = c.recv(51200)
                        #write into new file
                        dataS = BigC.write(ClientBData)
                        d += 1
                        print("Received packet number:" + str(d))
                        tillCC = tillCC - 1
                    #close file
                    BigC.close()
                    print("New Received File, Check contents of Directory")  
            
                
        if command[0] == 'put':
         #set the file name
            file_name = command[1]
            print("Sending Acknowledgment of command.")
            #get ACK to start
            msg = "Valid Put command. Let's go ahead "
            c.send(bytes(msg.encode()))
            print("Message Sent to Client.")
            if os.path.isfile(file_name):
                #file ACK
                msg2 = "File exists. Let's go ahead "
                #sends the ack about file
                c.send(bytes(msg2.encode()))
                print("Message about file existence sent.")
                #packet counter
                d = 0
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
                c.sendall(bytes(tillSS.encode()))
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
                    c.sendall(RunS)
                    time.sleep(1)
                    d += 1
                    check -= 1
                    #print out number of packets
                    print("Packet number:" + str(d))
                    print("Data sending in process:")
                #close file
                GetRunS.close()
                print("Sent from Server - Get function")
            else:
                msg = "Error: File does not exist in Server directory."
                #sends error message
                c.sendall(bytes(msg.encode()))
                print("Message Sent.")
        
