# Communication TCP listener class
import socket 		# To manage sockets

class Tcp_Initiator:

	tcp_ip = 0
	tcp_port = 0
	participants = {}		# Dictionary: {'participant_id': [listening_at, publishing_at]} udp ports
	BUFFER_SIZE = 1024
	sock = '' # Socket
	node_id = 0

	def __init__(self, tcp_ip, tcp_port, node_id):
		self.tcp_ip = tcp_ip
		self.tcp_port = tcp_port
		self.node_id = node_id
		self.BUFFER_SIZE = 1024
		self.participants = dict()


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
		if not self.participants:  # No participants yet !
			udp_port = self.tcp_port + 1
		else: 				 # There are other participants
			# The list bellow takes the last participant's udp port nbr and adds 1 to it to initialize udp_port
			udp_port = self.participants[ list( self.participants.keys())[-1] ][-1] + 1
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			self.sock.bind((self.tcp_ip, self.tcp_port))

			self.sock.listen(1)

			conn, addr = self.sock.accept()
			while 1:
				tmp = conn.recv(self.BUFFER_SIZE)
				if not tmp: break
				data = str(tmp.decode('ascii')) # data is the neighbor node ID
				
				# Generate 2 free udp port nbr
				self.participants[data] = []
				for i in range(2):
					while(not self.checkPort(udp_port)):
						udp_port+=1
					self.participants[data].append(udp_port)
					udp_port+=1

				to_send = self.tcp_echo_msg(data) # to send should contain [<node_id>, <udp_listening_port>, <udp_publiishing_port> ]

				conn.send(to_send.encode('utf-8'))  # echo
		finally:
			self.sock.close()


	'''
	Function used to check port availability
	Input:
		port: integer => port number to check
	Return:
		result: boolean => True if port is not in use; false otherwise
	'''
	def checkPort(self, port):
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    result = False
	    try:
	        sock.bind(("0.0.0.0", port))
	        result = True
	    except:
	        result = False
	    sock.close()
	    return result

	'''
	Function to generate TCP/IP communication playback message
	returns a string
	'''
	def tcp_echo_msg(self, neighbor_id):
		msg_struct = [str(self.node_id), str(self.participants[neighbor_id][0]), str(self.participants[neighbor_id][1])]

		return '.'.join(msg_struct)

	'''
	Used when user needs to join a game !
	'''
	def tcp_joiner(self, neighbor_node_nbr, node_subnet):
		neighbor_ip = node_subnet + '.' + str(neighbor_node_nbr)

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		self.sock.connect((neighbor_ip, self.tcp_port))

		try:
			self.sock.sendall(str(self.node_id).encode('utf-8'))

			while True:
				data = self.sock.recv(self.BUFFER_SIZE) # node_id.udp_l_port.udp_p_port
				if data: break

			self.participants = self.extract_master_msg(data)


		finally:
			self.sock.close()


	'''
	extract_master_msg encapsulate the message received from the 
	'''
	def extract_master_msg(self, data):
		data = data.decode('ascii')

		participant = data.split('.')
		
		participant = { str(participant[0]) : list(map(int, participant[1:])) }
		
		return participant

	'''
	Needed to close connection socket if something unexpeceted happened
	'''
	def close_tcp_listener(self):
		try:
			self.sock.close()
		except:
			pass
		return

	def get_participants(self):
		return self.participants