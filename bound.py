#! /usr/bin/env python

import socket,select
import binascii

UDP_IP = '0.0.0.0'
UDP_PORT = 10053

# message should be base64 encoded
def parse_query(message):

	# Mostly...
	# =E9=94=01=00=00=01=00=00=00=00=00=00=03www=06google=03com=00=00=01=00=01
	# Every once in a while...
	# =A1X=01=00=00=01=00=00=00=00=00=00=03www=06google=03com=00=00=01=00=01
	# Or...
	# =CFU=01=00=00=01=00=00=00=00=00=00=03www=06google=03com=00=00=01=00=01
	# Or...
	# M=A0=01=00=00=01=00=00=00=00=00=00=03www=06google=03com=00=00=01=00=01
	# Or...
	# :=18=01=00=00=01=00=00=00=00=00=00=03www=06google=03com=00=00=01=00=01
	# Or...
	# <?=01=00=00=01=00=00=00=00=00=00=03www=06google=03com=00=00=01=00=01

	wlength = 6
	nchar = 0
	# First 4 ID, e.g., =E9=94 or =A1X or :=18
	# Basically, I'm punting and will use the message_id, which is always the
	# same, to find the id.
	message_id = message[nchar:message.find("=01=00")]
	#message_id = message[nchar:nchar+wlength].replace("=", "")
	print "Message ID:", message_id
	nchar += len(message_id)
	# Next 4 Flags e.g., =01=00
	message_flags = message[nchar:nchar+wlength].replace("=", "")
	print "Message Flags:", message_flags
	nchar += wlength
	# Next 4 QDCOUNT e.g., =00=01
	message_qdcount = message[nchar:nchar+wlength].replace("=", "")
	print "Message QDCOUNT:", message_qdcount
	nchar += wlength
	# Next 4 ANCOUNT e.g., =00=00
	message_ancount = message[nchar:nchar+wlength].replace("=", "")
	print "Message ANCOUNT:", message_ancount
	nchar += wlength
	# Next 4 NSCOUNT e.g., =00=00
	message_nscount = message[nchar:nchar+wlength].replace("=", "")
	print "Message NSCOUNT:", message_nscount
	nchar += wlength
	# Next 4 ARCOUNT e.g., =00=00
	message_arcount = message[nchar:nchar+wlength].replace("=", "")
	print "Message ARCOUNT:", message_arcount
	domains = []
	message_data = message[nchar+wlength:]
	print "Message Data:", message_data
	for i in range(0,len(message_data)):
		if message_data[i] == "=":
			dlength = int(message_data[i+2:i+3])
			print "Message Dlength:", dlength
			if dlength != 0:
				domains.append(message_data[i+3:i+dlength+3])
				i += dlength
			else:
				print "Message Domain:", '.'.join(domains)
				# Done going through domains segments, now get final bits
				i += 3
				# Next 4 Data Query type e.g., =00=01
				message_querytype = message_data[i:i+6].replace("=", "")
				print "Message QType:", message_querytype
				i += 6
				# Last 4 Data Class type e.g., =00=01
				message_dataclass = message_data[i:i+6].replace("=", "")
				print "Message DCType:", message_dataclass
				# Now clear out, we're done parsing
				break
	print "Message Full:", message
	return True



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
		#('\x9ae\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01', ('127.0.0.1', 32944))

		message = binascii.b2a_qp(i.recv(1024))
		hostdata = i.recvfrom(1024)[1] # Having the second recv causes weird hangups
		print message, hostdata
	
		ip = hostdata[0]
		port = hostdata[1]
		domain = parse_query(message)

		if port is not 0: # All those broadcast messages from Bonjour! ;)
			print ip, port

