#! /usr/bin/env python

import socket,select

UDP_IP = '0.0.0.0'
UDP_PORT = 10053

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
sock2.bind((UDP_IP, UDP_PORT))

while True:
    r, w, x = select.select([sock, sock2], [], [])
    for i in r:
        print i, i.recvfrom(131072)
