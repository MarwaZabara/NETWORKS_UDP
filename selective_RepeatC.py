import socket
from random import randint

host = raw_input("enter IP address: ")
port = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creating the socket
sock.bind((host, port))
server = (host, 5000) #server's host and port number

def Main():
	sock.sendto('Hello, ',server) 								#just to make sure the client is connecting to the server
	quitting = False
	while not quitting:
		filename = raw_input("Filename? -> ")
		if filename != 'q': 									#if not quit 
			sock.sendto(filename, server)
			data, addr = sock.recvfrom(512) 					#receives wether the file does exist or not
			if data[:6] == 'EXISTS':
				filesize = long(data[6:])
				message = raw_input("file exists"+ str(filesize) + " Bytes, wanna download it? (Y/N): ")
				if(message == 'Y'):
					sock.sendto('OK', server)
					f = open('new_' + filename, 'wb')
					dict={} 						#dictionary to store all received packets and giving each an ID
					# index,addr=sock.recvfrom(8) 				
					# data, addr = sock.recvfrom(512) 			
					# dict[index]=data 							
					# print "first index"+str(index)
					totalRecv = 0
					# flag = 1

					while totalRecv < filesize:
						#if flag == 0:
							index,addr=sock.recvfrom(8)				#receives the ID of each packet
							data, addr = sock.recvfrom(512)			#receives the packet itself
							totalRecv += len(data)
							randpacket = randint(0, 9)
						# if index == 0:
						# 	print "index zero"
						# else:
						# 	dict[index]=data
							print "random bit="+str(randpacket)
							# print "dict keys are:"+ str(dict.keys())
							if randpacket == 4: 						#lost acknowledgment 
								print "Packet Dropped" + str(index)
								print "dict keys are:"+ str(dict.keys())
								totalRecv -= len(data)
								continue
							else:
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
							#flag = 0
							print "{0:.1f}".format((totalRecv/float(filesize))*100) + "% Done"
					print "Download Complete!"

		# 	if data == 'q':
		# 		quitting = True
		# 		continue
		# 	print data
		# 	randpacket = randint(0, 9)
		# 	print randpacket
		# 	if randpacket == 4:
		# 		print "Packet Dropped"
		# 		continue
		# 	else:
		# 		print "acknowlegment Sent"
		# 		sock.sendto('acknowledged',server)

		else:
			print "File doesn't exist!"

	sock.close()

Main()