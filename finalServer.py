import socket
import time
import sys
import os
import threading

#def RetrFile(name, sock):
	#print "holla retreive file"
	#filename, addr = sock.recvfrom(512)
	#print filename +" "+ str(addr)
	#if(os.path.isfile(filename)):
		#print "Exists "
		#sock.sendto(("EXISTS " + str(os.path.getsize(filename))), addr)
		#userResponse, addr = sock.recvfrom(512)
		#print (userResponse + "received")



def SW():
	host = raw_input("enter IP: ")
	port = 5000

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host, port))

	quitting = False
	print "Server Started"

	while not quitting:
		data, addr = sock.recvfrom(512)
		print "Client connected <" + str(addr) + ">"
		if str(data) == "quit":
			quitting = True
			continue
		filename, addr = sock.recvfrom(512)
		print filename +" "+ str(addr)
		if(os.path.isfile(filename)):
			print "Exists "
			sock.sendto(("EXISTS " + str(os.path.getsize(filename))), addr)
			userResponse, addr = sock.recvfrom(512)
			if(userResponse == 'OK'):
				print (userResponse + " received")
				with open(filename, 'rb') as f:
					bytesToSend = f.read(512)
					#fl = open('server_' +filename, 'wb')
					#fl.write(bytesToSend)
					sock.sendto(bytesToSend, addr)
					while bytesToSend != "":
						bytesToSend = f.read(512)
						fl.write(bytesToSend)
						sock.sendto(bytesToSend, addr)
		else:
			sock.sendto("ERR", addr)
		#t = threading.Thread(target = RetrFile, args =("retrthread", sock))
		#t.start()
	sock.close()

SW()
