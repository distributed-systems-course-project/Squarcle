#!/usr/bin/env python
import socket
import sys

TCP_IP = '192.168.1.108'		# Put here Pi's IP address
TCP_PORT = 25000					# Put here Master-to-Slave
BUFFER_SIZE = 1024
first_msg = int(sys.argv[1])
if first_msg == 1:
	MESSAGE = '108.mokhtar'
else:	
	MESSAGE = 'True.mokhtar.108'#.Juhha.125.Puhutko.201' # start the game message

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.connect((TCP_IP, TCP_PORT))
	s.send(MESSAGE.encode('utf-8'))
	data = s.recv(BUFFER_SIZE)
finally:
	s.close()

print("received data:", data.decode('ascii'))
