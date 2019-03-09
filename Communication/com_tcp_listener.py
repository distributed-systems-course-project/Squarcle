# Communication TCP listener class
import socket 		# To manage sockets


tcp_ip = 0
tcp_port = 0
BUFFER_SIZE = 1024
sock = '' # Socket
node_id = 0

class Tcp_Listener:

	def __init__(self, tcp_ip, tcp_port, node_id):
		self.tcp_ip = tcp_ip
		self.tcp_port = tcp_port
		self.node_id = node_id


	'''
	tcp_connect function
	Arguments:
		TCP_IP: (string) server's tcp_ip address to be used
		TCP_PORT: (integer) server's tcp open port
		MESSAGE: (string) Message to send to the server
	return
		data: (binary stirng) server reply message to our sent message
	Note that tcp_connection initializes the tcp_ip connection of  the client to the server
	the message in encoded into binary string so that it can be sent
	'''
	def tcp_listen(self):
		data = ""
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.sock.bind((self.tcp_ip, self.tcp_port))

		self.sock.listen(1)

		conn, addr = self.sock.accept()
		while 1:
			tmp = conn.recv(BUFFER_SIZE)
			if not tmp: break
			data = tmp
			to_send = str(self.node_id) # add UDP ports too !
			conn.send(to_send.encode('utf-8'))  # echo
		self.sock.close()
		return str(data.decode('ascii'))

	def close_tcp_listener(self):
		try:
			self.sock.close()
		except:
			pass
		return
