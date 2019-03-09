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
		- get_can_play : If true => all set, node can play; If false: node can't play the game
'''
class Com_Init:

	can_play = False;
	node_nbr = 0;
	node_ip = "";
	node_tcp_port = 0;


	def __init__(self):
		'''
		In the following section we will get the IP address of the wireless device of the node
		'''
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

		if self.can_play:
			self.node_nbr = self.geenrate_node_nbr(self.node_ip)

			# Checking the availability of the port
			node_tcp_port = 5000
			while(not self.checkPort(node_tcp_port)):
				node_tcp_port+=1

			self.node_tcp_port = node_tcp_port
		
		#else => couldn't get node IP address => This node can't play the game !




	'''
	Function used to generate node number
	Input:
		node_ip: node IP address => string
	Return:
		node_nbr : integer => node number
	'''
	def geenrate_node_nbr(self, node_ip):
		
		node_nbr = node_ip.split('.')[-1]

		return node_nbr

		
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
	Getters section
	'''
	def get_node_nbr(self):
		return self.node_nbr

	def get_node_ip(self):
		return self.node_ip

	def get_node_tcp_port(self):
		return self.node_tcp_port

	def get_can_play(self):
		return self.can_play