import socket

def SW():
	host = raw_input("enter IP: ")
	port = 5001

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host, port))
	server = (host, 5000)

	test = raw_input("connect or quit: ")
	sock.sendto(test, server)

	filename = raw_input("Filename? -> ")
	if(filename != "q"):
		sock.sendto(filename, server)
		data, addr = sock.recvfrom(512)
		if data[:6] == 'EXISTS':
			filesize = long(data[6:])
			message = raw_input("file exists"+ str(filesize) + " Bytes, wanna download it? (Y/N): ")
			if(message == 'Y'):
				sock.sendto('OK', server)
				f = open('new_' + filename, 'wb')
				data, addr = sock.recvfrom(512)
				totalRecv = len(data)
				print totalRecv
				f.write(data)
				while totalRecv < filesize:
					data, addr = sock.recvfrom(512)
					totalRecv += len(data)
					f.write(data)
					print "{0:.1f}".format((totalRecv/float(filesize))*100) + "% Done"
				print "Download Complete"
				sock.sendto('quit', server)
		else:
			print "File doesn't exist!"
		sock.close()
SW()
