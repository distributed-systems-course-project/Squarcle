#!/usr/bin/env python
import socket


TCP_IP = '100.72.32.32'		# Put here your computer's IP
TCP_PORT = 25000					# Put here the Slave-to-Master Port
BUFFER_SIZE = 1024 # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)

while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    data = data.decode('ascii')
    print("Master receive from slave: ", data)
    data = data.split('.')
    msg = '108' + '.' + 'Master_name' + ".25001.25002"
    conn.send(msg.encode('utf-8'))  # echo
	
conn.close()
