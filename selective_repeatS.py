import socket 
import time
import threading 
import os
import sys
from random import randint

host = raw_input("enter IP address: ")
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

# def lost_resend():
#     while lost:
#         print "timeout, resend packet..."
#         sock.sendto(str(i), addr)
#         sock.sendto(bytesToSend, addr)


def Selective(file_name,addr):
    indexi = 0
    flag = 0
    dict={}
    lost=9999
    bytesToSend=[]
    bytesToSend.append(None)
    received = []
    endi = 0
    with open(file_name, 'rb') as f:
        while bytesToSend[indexi]!= "":
            endi = indexi + 4
            for counter in range (indexi,endi):
                # if bytesToSend[indexi] == "":
                #     break
                bytesToSend[indexi]=f.read(512)
                if indexi in received:
                    continue
                randpacket = randint(0,9)
                ack = False
                sock.settimeout(10)
                if randpacket == 4:
                    print "dropped!"
                    while not socket.timeout:
                        continue
                else:
                    received.append(indexi)
                    sock.sendto(str(indexi), addr)
                    sock.sendto(bytesToSend[counter], addr)
                while not ack:
                    try:
                        print "TRY"
                        data, addr = sock.recvfrom(512)
                        ack = True
                    except socket.timeout :
                        print "timeout, added to loss list.."
                        if flag == 0:
                            lost = counter
                            flag =1
                print data
            flag=0
            indexi = lost







# def Selective(file_name, addr):
#     index=0
#     dict={}
#     lost={}
#     with open(file_name, 'rb') as f:
#         bytesToSend= None
        # while bytesToSend != "":
        #     counter=0
        #     while counter < 4:
        #         bytesToSend = f.read(512)
        #         randpacket = randint(0,9)
        #         sock.settimeout(10)
        #         ack = False
        #         if randpacket == 4:
        #             print "dropped!"
        #             while not socket.timeout:
        #                 continue
        #         else:
        #             sock.sendto(str(index), addr)
        #             sock.sendto(bytesToSend, addr)
        # while bytesToSend != "":
        #     for counter in range[index:index+4]:
        #         lost={}
        #         bytesToSend = f.read(512)
        #         randpacket = randint(0, 9)
        #         sock.settimeout(10)
        #         ack = False
        #         if randpacket == 4:
        #             print "dropped!"
        #             while not socket.timeout:
        #                 continue
        #         else:
        #             sock.sendto(str(index), addr)
        #             sock.sendto(bytesToSend, addr)
        #         while not ack:
        #             try:
        #                 print "TRY"
        #                 data, addr = sock.recvfrom(512)
        #                 del dict[index]
        #                 ack = True 
        #             except socket.timeout :
        #                 lost[index]=data
        #                 print "time out"
        #         counter+=1
        #         index+=1
        #     for i in lost.keys():
        #         sock.sendto(str(i), addr)
        #         sock.sendto(bytesToSend, addr)
        #     index+=1
        #     print data
            


                        


                        

                # else:
                #     sock.sendto(str(index), addr)
                #     sock.sendto(bytesToSend, addr)
                # while not ack:
                #     try:
                #         print "TRY"
                #         data, addr = sock.recvfrom(512)
                #         del dict[index]

                #         ack = True 
                #     except socket.timeout :
                #         print "timeout, resend packet..."
                #         sock.sendto(str(index), addr)
                #         sock.sendto(bytesToSend, addr)
                # index+=1
                # print data



def Main():
    data, addr = sock.recvfrom(512)
    print data + "Server Started.\n Client connected <" + str(addr) + ">"
    quitting = False
    while not quitting:
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
                Selective(filename,addr)


               



    sock.close()

Main()