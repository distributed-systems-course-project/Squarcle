# Communication initializer class

import socket 		# To manage sockets
import netifaces 	# To check the validaty of the TCP_IP address entered
import secrets		#  for generating cryptographically strong random numbers
import platform

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
		user_os = platform.system()

		if user_os == 'Windows':
			devices = self.get_connection_name_from_guid(devices)
		
			for x in devices:
				if 'wi' in x.lower(): # Assuming wireless interface has a 'w' character in its name
					device = x
		else:
			for x in devices:
				for char in x:
					if char == 'w': # Assuming wireless interface has a 'w' character in its name
						device = x
		print(device)
		#jdevice = devices[-2]
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
	Translating Windows interfaces to meaningful names
	'''
	def get_connection_name_from_guid(self, iface_guids):
		import winreg as wr

		iface_names = ['(unknown)' for i in range(len(iface_guids))]
		reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
		reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
		for i in range(len(iface_guids)):
			try:
				reg_subkey = wr.OpenKey(reg_key, iface_guids[i] + r'\Connection')
				iface_names[i] = wr.QueryValueEx(reg_subkey, 'Name')[0]
			except FileNotFoundError:
				pass
		return iface_names


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