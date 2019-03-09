# Communication initializer class

import socket 		# To manage sockets
import netifaces 	# To check the validaty of the TCP_IP address entered
import secrets		#  for generating cryptographically strong random numbers


class Com_Init:

	can_play = False;
	node_nbr = 0;
	node_ip = "";
	node_port = 0;


	def __init__(self, node_nbr, text):
		self.text = text
		self.node_nbr = node_nbr

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

		

	def get_text(self):
		return self.text

	def get_node_nbr(self):
		return self.node_nbr

	def get_node_ip(self):
		return self.node_ip

	def get_node_port(self):
		return self.node_port