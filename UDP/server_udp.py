import socket
import time
import os
import sys
#checks the length of the command line input
if len(sys.argv) != 3:
    print("Wrong Number of Args for client UDP")
    #should be length 3, ie the file name, control port number, data port
    sys.exit()
else:
    try:
        #set port num to input
        controlport = int(sys.argv[1])
        dataport = int(sys.argv[2])
        host = 'localhost'
        #create UDP Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #bind socket to server address
        s.bind((host, controlport))
        fs.bind((host, dataport))
        while True:
            #recieve command from client
            command, client_addr = s.recvfrom(2048)
            cmd_to_split = command.decode()
            #split the decoded command so it can be read
            cmd = cmd_to_split.split()

            #cd command handler
            if cmd[0] == 'cd':
                #set directory of command input to direc
                direc = cmd[1]
                cd_ACK = 'cd ACK'
                #send the cd ACK to the client
                s.sendto(cd_ACK.encode(), client_addr)
                print("CD ACK sent to Client")
                try:
                    #os change directory command
                    os.chdir(direc)
                    cd_ACK2 = 'cd Worked!'
                    #send the confirmation to client
                    s.sendto(cd_ACK2.encode(), client_addr )
                    print('cd Success')
                except (NotADirectoryError, FileNotFoundError):
                    print("This directory doesnt exist or could not be found")
                    msg = 'cd error'
                    #send error message to client
                    s.sendto(msg.encode(), client_addr)

            #ls command handler 
            if cmd[0] == 'ls':
                #set the directory you are listing to direc
                direc = cmd[1]
                ls_ACK = 'ls ACK'
                #send ACK to client
                s.sendto(ls_ACK.encode(), client_addr)
                print('ls ACK sent to client: ', client_addr)
                #if valid directory
                try:
                    #os command to list directory
                    F = os.listdir(direc)
                    #create a list to convert to string
                    direc_list = []
                    #read F and put into list
                    for file in F:
                        direc_list.append(file)
                    #convert list to string so it can be sent to client
                    direc_str = str(direc_list)
                    #sent ls result
                    s.sendto(direc_str.encode(), client_addr)
                    print('ls result sent to Client')
                except (NotADirectoryError, FileNotFoundError):
                    msg = 'The Directory you entered does not exist, or could not be found'
                    s.sendto(msg.encode(), client_addr)
                    print("The requested directory could not be found")
                    
            #GET AND PUT SOURCED FROM
            #https://github.com/pratiklotia/Client-Server-Fast-File-Transfer-using-UDP-on-Python/blob/master/server/server.py
            #Created on Sep 17, 2016#
            #@author: prati

            #get command handler        
            if cmd[0] == 'get':
                #set the file name
                file_name = cmd[1]
                print("Sending Acknowledgment of command.")
                #get ACK to start
                msg = "Valid Get command. Let's go ahead "
                s.sendto(msg.encode(), client_addr)
                print("Message Sent to Client.")
                if os.path.isfile(file_name):
                    #file ACK
                    msg = "File exists. Let's go ahead "
                    #sends the ack about file
                    s.sendto(msg.encode(), client_addr)
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
                    s.sendto(tillSS.encode(), client_addr)
                    #stop and wait
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
                        s.sendto(RunS, client_addr)
                        #stop and wait
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
                    s.sendto(msg.encode(), client_addr)
                    print("Message Sent.")

               
                            
                    

                    
            if cmd[0] == 'put':
                print("Sending Acknowledgment of command.")
                #PUT_ACK
                msg = "Valid Put command. Let's go ahead "
                s.sendto(msg.encode(), client_addr)
                print("Message Sent to Client.")
                print("In Server, Put function")
                #duplicate handler, checks to see if file already exists in server
                if os.path.isfile('Received_'+cmd[1]):
                    BigSAgain = open('New_'+cmd[1], "wb")   
                #open the file
                else:
                    BigSAgain = open('Received_'+cmd[1], "wb")
                #packet counter
                d = 0
                print("Receiving packets will start now if file exists.")
                #print("Timeout is 15 seconds so please wait for timeout at the end.")
                #receive number of packets
                Count, countaddress = s.recvfrom(4096)
                #convert to int
                tillI = int(Count.decode())
                #while there are packets being read
                while tillI != 0:
                    #recieve file data
                    ServerData, serverAddr = s.recvfrom(4096)
                    #stop and wait
                    s.settimeout(2)
                    time.sleep(1)
                    #write to new file in server
                    dataS = BigSAgain.write(ServerData)
                    d += 1
                    tillI = tillI - 1
                    #Print out packets received
                    print("Received packet number:" + str(d))
                #close the file
                BigSAgain.close()
                print("New file closed. Check contents in your directory.")
    except ConnectionResetError:
        print('Port Numbers Do Not Match')
               
