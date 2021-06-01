import socket
import time
import os
import sys
if len(sys.argv) != 4:
    print("Wrong Number of Args for client UDP")
    sys.exit()
else:
    try:
        #as per specifications of the project
        server_ip = str(sys.argv[1])
        controlport = int(sys.argv[2])
        dataport = int(sys.argv[3])
        #set server address
        server_addr = (server_ip, controlport)
        file_addr = (server_ip, dataport)
        #create UDP socket
        cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #give time for the server
        cs.settimeout(15)
        time.sleep(1)
        while True:
            #command prompt
            user_inp = input("Enter a Command: ")
            uie = user_inp.encode()
            #sends command to server
            cs.sendto(uie, server_addr)
            #split it into an array of strings
            command = user_inp.split()
            if len(command) != 2:
                print('Incorrect Number of Args')
            else:
                #cd commmand handler
                if command[0] == 'cd':
                    print('Checking for ACK')
                    #get cd ACK
                    data, addr = cs.recvfrom(2048)
                    if data.decode() == 'cd ACK':
                        print("CD Starting")
                        #recieve ack2 if cd is successful
                        ack2, addr = cs.recvfrom(2048)
                        if ack2.decode() == 'cd Worked!':
                            print('Current Directory: ', command[1])
                            #if ack2 was the error message
                        if ack2.decode() == 'cd error':
                            print('The Directory you entered could not be found')
                        

                    
                #ls commmand handler
                if command[0] == 'ls':
                    print('Checking for ACK')
                    #recieve ack
                    data, addr = cs.recvfrom(2048)
                    #if ack is recieved
                    if data.decode() == 'ls ACK':
                        #recieve ls result from server
                        print('LS Starting')
                        lsData, addr = cs.recvfrom(4096)
                        #print out the ls result
                        print(lsData.decode())
                        
            #GET AND PUT SOURCED FROM
            #https://github.com/pratiklotia/Client-Server-Fast-File-Transfer-using-UDP-on-Python/blob/master/server/server.py
            #Created on Sep 17, 2016
            #@author: prati

                        
                #get commmand handler       
                if command[0] == 'get':
                    print("Checking for acknowledgement")
                    #recieve get ACK
                    get_ack, clientAddr = cs.recvfrom(51200)
                    print(get_ack.decode())
                    #get is now ready
                    print("Inside Client Get")
                    #recieve file size ACK
                    ClientData, clientAddr2 = cs.recvfrom(51200)
                    print(ClientData.decode())

                    if len(ClientData.decode()) < 30:
                        if command[0] == "get":
                            #create a new file names Received_file_name
                            BigC = open('Received_'+command[1], "wb")
                            #count number of packets
                            d = 0
                            #get number of packets
                            CountC, countaddress = cs.recvfrom(4096)
                            #convert to int
                            tillCC = int(CountC.decode())
                            print("Receiving packets will start now if file exists.")
                            # print(
                            #   "Timeout is 15 seconds so please wait for timeout at the end.")
                            #while theres still data
                            while tillCC != 0:
                                #recieve data chunks
                                ClientBData, clientbAddr = cs.recvfrom(51200)
                                #write into new file
                                dataS = BigC.write(ClientBData)
                                d += 1
                                print("Received packet number:" + str(d))
                                tillCC = tillCC - 1
                            #close file
                            BigC.close()
                            print("New Received File, Check contents of Directory")
                        
                        
                    

                    
                #put commmand handler
                if command[0] == 'put':
                    #set file name
                    file_name = command[1]
                    print("Checking for acknowledgement")
                    #receive put ACK
                    ClientData, addr = cs.recvfrom(4096)
                    #print ACK
                    print(ClientData.decode())
                    print("Sending data.....")
                    #if ACK is received
                    if ClientData.decode == "Valid Put command. Let's go ahead ":
                        #check to see if file exists
                        if os.path.isfile(file_name):
                            #packet counter
                            c = 0
                            #get the size of the file
                            size = os.stat(file_name)
                            #get the number of packets in the file
                            sizeS = size.st_size
                            #print file size in bytes
                            print("File size in bytes: " + str(sizeS))
                            #convert to int
                            Num = int(sizeS / 4096)
                            Num = Num + 1
                            #print Num of Packets
                            print("Number of packets to be sent: " + str(Num))
                            #convert to string to send to server
                            till = str(Num)
                            #sent to server number of packets
                            cs.sendto(till.encode(), addr)
                            tillIC = int(Num)
                            #open the file
                            GetRun = open(file_name, "rb")
                            #while there is still data
                            while tillIC != 0:
                                #read the file
                                Run = GetRun.read(51200)
                                #send to server
                                cs.sendto(Run, addr)
                                c += 1
                                tillIC -= 1
                                print("Packet number:" + str(c))
                                print("Data sending in process:")
                            #close the file
                            GetRun.close()
                            #PUT success
                            print("Sent from Client - Put function")
                        else:
                            print("File does not exist.")
                    else:
                        print("Invalid.")


    except ConnectionResetError:
        print('Port Numbers Do Not Match')
    
