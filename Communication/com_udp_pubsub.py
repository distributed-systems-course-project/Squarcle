# Communication publisher class
import socket

class udp_pubsub:
	udp_receiving_ports = [] # To listen to
	udp_sending_ports   = [] # To send to
	udp_ips 	        = []
	udp_node_nbrs       = []
	other_nodes_msgs    = []
	udp_subnet          = ""
	sock                = ''

	def __init__(self):
		pass

	def __init__(self, udp_subnet, udp_node_nbrs, udp_receiving_ports, udp_sending_ports):
		self.udp_subnet          = udp_subnet
		self.udp_node_nbrs       = udp_node_nbrs
		self.udp_receiving_ports = udp_receiving_ports
		self.udp_sending_ports   = udp_sending_ports

		self.neighboring_nodes_ips(udp_subnet, udp_node_nbrs)


	'''
	neighboring nodes ips function uses provided subnet to formulate
	IP addresses of other discovered nodes.
	The results are stores in the global variable udp_ips
	'''
	def neighboring_nodes_ips(self, udp_subnet, udp_node_nbrs):
		for node_nbr in udp_node_nbrs:
			udp_ips.append( udp_subnet.append( '.'+ str(node_nbr) ) )


	'''
	Publishes current node information and states to other neighboring nodes ! 
	Message should have the form [<node nbr>, <center_x_coor>, <center_y_coor>, <node score>]
	'''
	def udp_publisher(self, MESSAGE):
		MESSAGE = MESSAGE.encode('utf-8') # encoding the message before sending it

		sock = socket.socket(socket.AF_INET, # Internet
		                     socket.SOCK_DGRAM) # UDP

		for (IP, PORT) in zip (self.udp_ips, self.udp_sending_ports):
			sock.sendto(MESSAGE, (IP, PORT))


	def udp_subscriber(self):
		self.other_nodes_msgs = []	# Initializing other_nodes msgs to none

		self.sock = socket.socket(socket.AF_INET, # Internet
		                     socket.SOCK_DGRAM) # UDP

		for (IP, PORT) in zip (self.udp_ips, self.udp_receiving_ports):

			self.sock.bind((IP, PORT))

			i = 0
			for i in range(len(self.udp_ips)):
			    data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
			    print("received message:", data.decode('ascii'))
			    # Update the other_nodes_msgs
				self.other_nodes_msgs.append( self.message_reformulation(data.decode('ascii')) )

		sock.close()


	'''
	Function message_reformulation used to convert the received udp packet from string
	to a list of meaningful elements
	the structure of the result is
	[<node nbr>, <center_x_coor>, <center_y_coor>, <node score>]
	all elements are integers ! 
	'''
	def message_reformulation(self, message):
		result = []
		# splitting the message on '.'
		result = message.split('.')
		# Casting the message elements from strings to integers
		result = list(map(int, tmp))

		return result


	'''
	Getters
	'''

	def get_other_nodes_msgs(self):
		return self.other_nodes_msgs


