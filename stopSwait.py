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

def Main():
	data, addr = sock.recvfrom(512)
	print data + "Server Started"
	quitting = False
	while not quitting:
		input = raw_input("data you'd like to send?: ")
		if input == 'q':
			sock.sendto(input, addr)
			quitting = True
			continue
		randpacket = randint(0, 9)
		sock.settimeout(10)
		ack = False
		if randpacket == 4:
			print "dropped!"
			while not socket.timeout:
				continue
		else:
			sock.sendto(input, addr)
		while not ack:
			try:
				print "TRY"
				data, addr = sock.recvfrom(512)
				ack = True
			except socket.timeout :
				print "timeout, resend packet..."
				sock.sendto(input, addr)
		print data

	sock.close()

Main()