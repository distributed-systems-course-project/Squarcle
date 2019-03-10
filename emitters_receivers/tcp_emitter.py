#!/usr/bin/env python
import socket


TCP_IP = '100.72.32.32'		# Put here Pi's IP address
TCP_PORT = 25000					# Put here Master-to-Slave
BUFFER_SIZE = 1024
#MESSAGE = "image"				# Choose one of these messages
#MESSAGE = "board"				# The information will be echoed to your computer
#MESSAGE = "pieces"
#MESSAGE = "piece"
#MESSAGE = "arm"
MESSAGE = '32'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode('utf-8'))
data = s.recv(BUFFER_SIZE)
s.close()

print("received data:", data.decode('ascii'))
