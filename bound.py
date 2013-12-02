#! /usr/bin/env python

import socket,select
import binascii
import re

UDP_IP = '0.0.0.0'
UDP_PORT = 10053

# message should be hex encoded
def parse_query(message):
	m = {}
	# Example hex values for www.google.edu nslookup
	# ab5a010000010000000000000377777706676f6f676c65036564750000010001
	# ID [ab5a], Flags [0100], QDCOUNT [0001], ANCOUNT [0000], NSCOUNT [0000], ARCOUNT [0000]
	m['id'], m['flags'], m['qdcount'], m['ancount'], m['nscount'], m['arcount'] = re.findall('....', message[0:24])
	domains = []
	msg_contents = message[24:]
	i = 0
	while i < len(msg_contents):
		byte_width = 2
		# Denotes how long the domain string length will be, in hex. 
		# Convert to int, multiply by byte char width (usually 2)
		domain_length = int(msg_contents[i:i+byte_width], 16) * byte_width
		if domain_length != 0:
			d = msg_contents[i+byte_width:i+domain_length+byte_width]
			dstring = binascii.unhexlify(d)
			domains.append(dstring)
			i += domain_length + byte_width
		else:
			#print "Message Domain:", '.'.join(domains)
			m['domains'] = domains
			# Done going through domains segments, now get final bits
			# QueryType [0001], DataClass [0001]
			m['querytype'], m['dataclass'] = re.findall('....', msg_contents[i+2:])
			break
	return m

# Returns binary response
def gen_response(request):
	response=''
	response += request['id']
	response_flags = '8180'
	response += response_flags
	response += request['qdcount']
	response_ancount = '0001'
	response += response_ancount
	response += request['nscount']
	response += request['arcount']

	# Re-encode domains and add to response
	domains = request['domains']
	for domain in domains:
		dlen = str(hex(len(domain))[2:]).zfill(2)
		response += dlen
		d = binascii.hexlify(domain)
		#print "Domain:", d
		response += d

	response_ispointer = 'c'
	response += response_ispointer
	response_nameoffset = '00c'
	response += response_nameoffset
	response_type = '0001' # 0001 = Type A query (Host address)
	response += response_type
	response_class = '0001' # 0001 = Class IN (Internet address)
	response += response_class
	response_ttl = '00000020' # 20 = 32 decimal seconds.
	response += response_ttl
	address_length = '0004'
	response += address_length
	ip = "1.2.3.4"
	response += binascii.b2a_hex(str.join('',map(lambda x: chr(int(x)), ip.split('.'))))
	return response

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
			msg = parse_query(message)
			print "Message from:", ip, port
			print "Domains:", ".".join(msg['domains'])
			print "ID:", msg['id']

			response = gen_response(msg)
			print response, type(response), len(response)
			print binascii.a2b_hex(response)
			i.sendto(gen_response(msg), (ip, port))

