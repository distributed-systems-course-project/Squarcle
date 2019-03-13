#!/usr/bin/env python
import socket


TCP_IP = '192.168.1.104'		# Put here your computer's IP
TCP_PORT = 25000					# Put here the Slave-to-Master Port
BUFFER_SIZE = 1024 # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	print('Connection address:', addr)
	while 1:
	    data = conn.recv(BUFFER_SIZE)
	    if not data: break
	    data = data.decode('ascii')
	    print("Master receive from slave: ", data)
	    msg = data + ".25001.25002"
	    conn.send(msg.encode('utf-8'))  # echo
finally:
	conn.close()
