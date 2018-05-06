import socket 
import os
import sys
from random import randint

host = raw_input("enter IP address: ")
port = 5000
dict={}
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

def StopAndWait(file_name, addr):
    with open(file_name, 'rb') as f:
        # bytesToSend = f.read(512)
        i=0
        # flag = 1
        bytesToSend=None
        while bytesToSend != "":
            # if flag == 0:
            bytesToSend = f.read(512)
            print "bytesToSend: " + bytesToSend
            i+=1
            randpacket = randint(0, 9)
            sock.settimeout(10)
            ack = False
            if randpacket == 4:
                print "dropped!"
                while not socket.timeout:
                    continue
            else:
                sock.sendto(str(i), addr)
                sock.sendto(bytesToSend, addr)
            while not ack:
                try:
                    print "TRY"
                    data, addr = sock.recvfrom(512)
                    ack = True
                except socket.timeout :
                    print "timeout, resend packet..."
                    sock.sendto(str(i), addr)
                    sock.sendto(bytesToSend, addr)
            print data
        sock.close()
        exit()
            # flag = 0

def Selective(file_name,addr):
    with open(file_name, 'rb') as f:
        bytesToSend = None
        # indexi = 0
        flag = 0
        lost = []
        nextindex=0
        received = []
        while bytesToSend != "":
            # print"hello"
            # endi = indexi + 4
            endi=nextindex+4
            lost=[]
            # print endi
            for counter in range (nextindex,endi):
                # if bytesToSend[indexi] == "":
                #     break
                # if counter in lost:
                #     lost_resend(lost,dict)
                #     continue
                bytesToSend = f.read(512)
                print "bytesToSend: " + bytesToSend
                dict[counter]=bytesToSend
                if counter in received:
                    continue
                received.append(counter)
                print received
                del lost[:]
                randpacket = randint(0,9)
                ack = False
                sock.settimeout(10)
                if randpacket == 4:
                    print "dropped!"
                    while not socket.timeout:
                        continue
                else:
                    sock.sendto(str(counter), addr)
                    sock.sendto(bytesToSend, addr)
                check_recv(lost,counter,addr)
                # while not ack:
                #     try:
                #         print "TRY"
                #         data, addr = sock.recvfrom(512)
                #         ack = True
                #     except socket.timeout :
                #         received[counter] = 0
                #         print "timeout, added to loss list.."
                #         lost.append(counter)
                #         # if flag == 0:
                #         #     nextindex = counter
                #         #     flag =1
                # print data
            # flag=0
            nextindex=counter+1
            lost_resend(lost,addr)
        sock.close()
        exit()

def gobackn(file_name,addr):
    with open(file_name, 'rb') as f:
        bytesToSend = None
        # indexi = 0
        flag = 0
        lost = []
        nextindex=0
        received = []
        while bytesToSend != "":
            # print"hello"
            # endi = indexi + 4
            endi=nextindex+4
            lost=[]
            # print endi
            for counter in range (nextindex,endi):
                # if bytesToSend[indexi] == "":
                #     break
                # if counter in lost:
                #     lost_resend(lost,dict)
                #     continue
                bytesToSend = f.read(512)
                print "bytesToSend: " + bytesToSend
                dict[counter]=bytesToSend
                if counter in received:
                    continue
                received.append(counter)
                print received
                del lost[:]
                randpacket = randint(0,9)
                ack = False
                sock.settimeout(10)
                if randpacket == 4:
                    print "dropped!"
                    while not socket.timeout:
                        continue
                else:
                    sock.sendto(str(counter), addr)
                    sock.sendto(bytesToSend, addr)
                check_recv(lost,counter,addr)
                # while not ack:
                #     try:
                #         print "TRY"
                #         data, addr = sock.recvfrom(512)
                #         ack = True
                #     except socket.timeout :
                #         received[counter] = 0
                #         print "timeout, added to loss list.."
                #         lost.append(counter)
                #         # if flag == 0:
                #         #     nextindex = counter
                #         #     flag =1
                # print data
            # flag=0
            nextindex=counter+1
            #lost_resend(lost,addr)
        sock.close()
        exit()


def lost_resend(lost,addr):
    # with lost.pop(0) as x:
    while lost:
        x=lost.pop(0)
        y=dict[x]
        sock.sendto(str(x), addr)
        sock.sendto(y, addr)
        check_recv(lost,x,addr)


def check_recv(lost,index,addr):
    ack=False
    # while not ack:
    try:
        print "TRY"
        data, addr = sock.recvfrom(512)
        ack = True
        if index in lost:
            print index +"removed from lost"
            lost.remove(index)
    except socket.timeout :
        # received[counter] = 0
        print "timeout, added to loss list.."
        data="Lost data resent"
        lost.append(index)
        lost.sort()
        print "lost="+str(lost)
        lost_resend(lost,addr)
    print data
        # if flag == 0:
        #     nextindex = counter
        #     flag =1





def Main():
    data, addr = sock.recvfrom(512)
    print data + "Server Started.\n Client connected <" + str(addr) + ">"
    quitting = False
    while not quitting:
    	method,addr=sock.recvfrom(16)
    	print method
        filename, addr = sock.recvfrom(512)
        if str(filename) == "quit":
            quitting = True
            continue
        print filename +" "+ str(addr)
        if(os.path.isfile(filename)):
            print "Exists "
            sock.sendto(("EXISTS" + str(os.path.getsize(filename))), addr)
            userResponse, addr = sock.recvfrom(512)
            if(userResponse == 'OK'):
                print (userResponse + " received")
            if method=="SR":
                Selective(filename,addr)
            elif method == "SW":
            	StopAndWait(filename,addr)
            elif method == "GBN":
                gobackn(filename, addr)
            else:
            	print "UN KNOWN METHOD RECIEVED"



               

    sock.close()

Main()
