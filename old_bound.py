#! /usr/bin/env python
# Goal: Create DNS server from scratch
import socket

# DNS Entries
server_list = {
	'www.testing.com':		'192.168.16.251',
	'www.besting.com':		'192.168.16.251',
	'www.resting.com':		'192.168.16.251',
	'www.guessing.com':		'192.168.16.251',
	'www.blessing.com':		'192.168.16.251',
	};

# TCP Connection
#serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# UDP Connection
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serversocket.bind((socket.gethostname(), 5053))

# Also for TCP connections
#serversocket.listen(5)

while 1:
	# TCP
	#(clientsocket, address) = serversocket.accept()
	#ct = client_thread(clientsocket)
	#ct.run()
	data, addr = serversocket.recvfrom(1024)
	print "Received message:", data

print "Server exited."
