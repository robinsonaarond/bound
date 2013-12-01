#! /usr/bin/env python

import socket,select
import binascii
import re

UDP_IP = '0.0.0.0'
UDP_PORT = 10053

# message should be base64 encoded
def parse_query(message):

	# hex values for www.google.edu nslookup
	# ab5a010000010000000000000377777706676f6f676c65036564750000010001
	# ID [ab5a], Flags [0100], QDCOUNT [0001], ANCOUNT [0000], NSCOUNT [0000], ARCOUNT [0000]
	msg_id, msg_flags, msg_qdcount, msg_ancount, msg_nscount, msg_arcount = re.findall('....', message[0:24])
	domains = []
	msg_data = message[24:]
	i = 0
	while i < len(msg_data):
		byte_width = 2
		# Denotes how long the domain string length will be, in hex. 
		# Convert to int, multiply by byte char width (usually 2)
		domain_length = int(msg_data[i:i+byte_width], 16) * byte_width
		if domain_length != 0:
			d = msg_data[i+byte_width:i+domain_length+byte_width]
			dstring = binascii.unhexlify(d)
			domains.append(dstring)
			i += domain_length + byte_width
		else:
			print "Message Domain:", '.'.join(domains)
			# Done going through domains segments, now get final bits
			msg_querytype, msg_dataclass = re.findall('....', msg_data[i+2:])
			print "Query Type:", msg_querytype
			print "Data Class:", msg_dataclass
			#i += 2
			## Next 4 Data Query type e.g., 0001
			#message_querytype = msg_data[i:i+4]
			#i += 4
			## Last 4 Data Class type e.g., 0001
			#msg_dataclass = msg_data[i:i+4]
			## Now clear out, we're done parsing
			break
	return True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
sock2.bind((UDP_IP, UDP_PORT))

print "Listening on port %s..." % UDP_PORT

while True:
    r, w, x = select.select([sock, sock2], [], [])
    for i in r:
		packet = i.recvfrom(1024)
		message = binascii.b2a_hex(packet[0])
		ip = packet[1][0]
		port = packet[1][1]

		if port is not 0: # All those broadcast messages from Bonjour! ;)
			domain = parse_query(message)
			print "Message from:", ip, port

