import socket
from random import randint

host = raw_input("enter IP address: ")
port = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
server = (host, 5000)

def Main():
	sock.sendto('Hello, ',server)
	quitting = False
	while not quitting:
		data, addr = sock.recvfrom(512)
		if data == 'q':
			quitting = True
			continue
		print data
		randpacket = randint(0, 9)
		print randpacket
		if randpacket == 4:
			print "Packet Dropped"
			continue
		else:
			print "acknowlegment Sent"
			sock.sendto('acknowledged',server)

	sock.close()

Main()