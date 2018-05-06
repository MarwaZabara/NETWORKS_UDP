import socket
from random import randint

host = raw_input("enter IP address: ")
port = 5001
dict={}
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creating the socket
sock.bind((host, port))
server = (host, 5000) #server's host and port number
def SW(f,data,index,totalRecv):
	dict[index]=data						#stores the packet of the given ID
	print "acknowlegment Sent"
	print "dict keys are:"+ str(dict.keys())
	#data, addr = sock.recvfrom(512)
	print totalRecv
	f.write(data)
	sock.sendto('acknowledged',server)

def GBN(f,data,index,totalRecv):
	dict[index]=data						#stores the packet of the given ID
	print "acknowlegment Sent"
	print "dict keys are:"+ str(dict.keys())
	#data, addr = sock.recvfrom(512)
	print totalRecv
	f.write(data)
	sock.sendto('acknowledged',server)


def SR(f,data,index,totalRecv):
	dict[index]=data						#stores the packet of the given ID
	print "acknowlegment Sent"
	print "dict keys are:"+ str(dict.keys())
	#data, addr = sock.recvfrom(512)
	print totalRecv
	if index ==0:
		f.write(dict[index])
		index=1
	while index in dict.keys():
		f.write(dict[index])
		index=+1
	sock.sendto('acknowledged',server)


def Main():
	sock.sendto('Hello, ',server) 								#just to make sure the client is connecting to the server
	# quitting = False
	# while not quitting:
	method = raw_input("Enter SR or SW or GBN to choose the method? -> ")
	sock.sendto(method, server)
	filename = raw_input("Filename? -> ")
	if filename != 'q': 									#if not quit 
		sock.sendto(filename, server)
		data, addr = sock.recvfrom(512) 					#receives wether the file does exist or not
		if data[:6] == 'EXISTS':
			filesize = long(data[6:])
			message = raw_input("file exists"+ str(filesize) + " Bytes, wanna download it? (Y/N): ")
			if(message == 'Y'):
				sock.sendto('OK', server)
				f = open('new_'+ method +"_" + filename, 'wb')
					#dictionary to store all received packets and giving each an ID
				# index,addr=sock.recvfrom(8) 				
				# data, addr = sock.recvfrom(512) 			
				# dict[index]=data 							
				# print "first index"+str(index)
				totalRecv = 0
				while totalRecv < filesize:
					#if flag == 0:
					index,addr=sock.recvfrom(8)				#receives the ID of each packet
					data, addr = sock.recvfrom(512)			#receives the packet itself
					totalRecv += len(data)
					randpacket = randint(0, 9)
					print "random bit="+str(randpacket)
					if randpacket == 4: 						#lost acknowledgment 
						print "Packet Dropped: " + str(index)
						print "dict keys are:"+ str(dict.keys())
						totalRecv -= len(data)
						continue
					else :
						if method == "SW":
							SW(f,data,index,totalRecv)
							
						#flag = 0
						elif method == "SR":
							SR(f,data,index,totalRecv)
						elif method == "GBN":
							GBN(f,data,index,totalRecv)
						else:
							print "UNKNOWN METHOD ENTERED"
							
					print "{0:.1f}".format((totalRecv/float(filesize))*100) + "% Done"
				print "Download Complete!"
				exit()
	else :
		quitting=True
		print "Quitting"

		# else:
		# 	print "File doesn't exist!"

	sock.close()

Main()