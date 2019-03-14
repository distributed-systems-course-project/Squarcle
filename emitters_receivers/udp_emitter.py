import socket
import sys

UDP_IP = "192.168.1.108"
UDP_PORT = int(sys.argv[1])
MESSAGE = '.'.join(['mokhtar' , '100', '200' , '1500'])

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM, # UDP
                     socket.IPPROTO_UDP) # Multicast
# Multicast line
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
while True:
	sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
