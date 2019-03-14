# Communication initializer class

import socket 		# To manage sockets
import netifaces 	# To check the validaty of the TCP_IP address entered
import secrets		#  for generating cryptographically strong random numbers

'''
	This class is used to set the initial parameter of the communication between the nodes
	It implements an empty constructor

	It implements 4 getters:
		- get_node_nbr: returns node generated number to be used as an identifier !
		- get_node_ip: node IP address
		- get_node_tcp_port: TCP/IP port number
		- get_node_subnet_ip: return node subnet it (192.168.1) 
		- get_can_play : If true => all set, node can play; If false: node can't play the game
'''
class Com_Init:

	# This port nbr was chosen from https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers#Table_legend
	INITIAL_TCP_PORT = 25000 # Assuming port 25,000 is not used by any other process

	can_play = False;
	node_nbr = 0;
	node_ip = "";
	node_tcp_port = 0;
	node_subnet_ip = 0;
	playability = False # playability 
	data = '' # Squarcle object

	# Constructor
	def __init__(self, data):
		'''
		In the following section we will get the IP address of the wireless device of the node
		'''
		self.data = data

		device = ""
		devices = netifaces.interfaces()
		for x in devices:
			for char in x:
				if char == 'w': # Assuming wireless interface has a 'w' character in its name
					device = x
					break

		if device: # a wireless device with 'w' letter in its name was found !
			self.node_ip  = netifaces.ifaddresses(netifaces.interfaces()[devices.index(device)])[netifaces.AF_INET][0]['addr']
			self.can_play = True

		else: # No wireless device with 'w' in its name
			self.can_play = False
		
		data.acquire()
		data.set_playability(self.can_play)
		data.release()
			

		if self.can_play:
			self.node_nbr = self.genrate_node_nbr(self.node_ip)
			self.node_subnet_ip = self.generate_node_subnet_ip(self.node_ip)

			# Checking the availability of the port
			
			self.node_tcp_port = self.INITIAL_TCP_PORT

		#else => couldn't get node IP address => This node can't play the game !
		data.acquire()
		data.set_node_ID(int(self.node_nbr))
		data.release()

	'''
	Function used to generate node number
	Input:
		node_ip: node IP address => string
	Return:
		node_nbr : integer => node number
	'''
	def genrate_node_nbr(self, node_ip):
		
		node_nbr = node_ip.split('.')[-1]

		return node_nbr

	'''
	Function to extract node subnet ip address to be used later
	Input:
		node_ip: string => node ip address
	Return:
		node_subnet_ip : string => node subnet ip address
	
	'''
	def generate_node_subnet_ip(self, node_ip):
		
		node_subnet_ip = "."
		
		separated = node_ip.split('.')
		
		del separated[-1] 

		node_subnet_ip = node_subnet_ip.join(separated)
	
		return node_subnet_ip
		

	'''
	Getters section
	'''
	def get_node_nbr(self):
		return self.node_nbr

	def get_node_ip(self):
		return self.node_ip

	def get_node_tcp_port(self):
		return self.node_tcp_port

	def get_node_subnet_ip(self):
		return self.node_subnet_ip

	def get_can_play(self):
		return self.can_play