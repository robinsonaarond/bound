#! /usr/bin/env python

import socket,select
import binascii

UDP_IP = '0.0.0.0'
UDP_PORT = 10053

def parse_query(message):
	domain = ""
	# First 4 ID, e.g., =E9=94
	# Next 4 Flags e.g., =01=00
	# Next 4 QDCOUNT e.g., =00=01
	# Next 4 ANCOUNT e.g., =00=00
	# Next 4 NSCOUNT e.g., =00=00
	# Next 4 ARCOUNT e.g., =00=00
	# Next ? Data e.g., =03www=06google=03com
	# Next 2 End of Domain e.g., =00
	# Next 4 Data Query type e.g., =00=01
	# Last 4 Data Class type e.g., =00=01
	#domain = "%s.%s.%s" % (p[13],p[14],p[15])
	return domain

# 127.0.0.1 57188 =E9=94=01=00=00=01=00=00=00=00=00=00=03www=06google=03com=00=00=01=00=01
#('\x9ae\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01', ('127.0.0.1', 32944))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
sock2.bind((UDP_IP, UDP_PORT))

while True:
    r, w, x = select.select([sock, sock2], [], [])
    for i in r:
		#message = parse_message(i.recvfrom(1024)[0])
		#ip = packet[1][0]
		#port = packet[1][1]

		#message, hostdata = (binascii.b2a_qp(i.recv(1024)), i.recvfrom(1024)[1])

		message = binascii.b2a_qp(i.recv(1024))
		hostdata = i.recvfrom(1024)[1] # Having the second recv causes weird hangups
	
		ip = hostdata[0]
		port = hostdata[1]

		domain = parse_query(message)

		#message, hostdata = i.recvfrom(1024)
		#ip = hostdata[0]
		#port = hostdata[1]
		if port is not 0: # All those broadcast messages from Bonjour! ;)
			print ip, port, domain
		#else:
			#print "Found other..."
		




