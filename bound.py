#! /usr/bin/env python

import socket,select

UDP_IP = '0.0.0.0'
UDP_PORT = 10053

def parse_message(message):
	return message

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
sock2.bind((UDP_IP, UDP_PORT))

while True:
    r, w, x = select.select([sock, sock2], [], [])
    for i in r:
		message, hostdata = i.recvfrom(1024)
		#message = parse_message(i.recvfrom(1024)[0])
		ip = hostdata[0]
		port = hostdata[1]
		#ip = packet[1][0]
		#port = packet[1][1]
		if port is not 0: # All those broadcast messages from Bonjour! ;)
			print ip, port, message



#('\x9ae\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01', ('127.0.0.1', 32944))

