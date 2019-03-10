# Communication publisher class
import socket

class udp_pubsub:

	udp_subnet          = ""
	participants		= {}
	udp_ips 	        = []
	other_nodes_msgs    = {}
	sock                = ''


	'''
	Constructor
	Takes a string that contains master node subnet network
	and dictionary of participants (created at tcp_listener class) 
	Dictionary: {'participant_id': [listening_at, publishing_at]} udp ports
	It generates neighboting nodes ips too
	'''

	def __init__(self, udp_subnet, participants):
		self.udp_subnet          = udp_subnet
		self.participants		 = participants
		self.neighboring_nodes_ips(udp_subnet, participants)
		self.other_nodes_msgs    = {}
		# It should start udp_subscriber thread and udp_publisher thread


	'''
	neighboring nodes ips function uses provided subnet to formulate
	IP addresses of other discovered nodes.
	The results are stores in the global variable udp_ips
	'''
	def neighboring_nodes_ips(self, udp_subnet, participants):
		for node_id, udp_ports in participants.items():
			udp_ports.append( udp_subnet + '.' +  node_id )


	'''
	Publishes current node information and states to other neighboring nodes ! 
	centers_score is a list of integers of the form [<center_x>, <center_y>, <score>]
	The message will be published to all neighboring nodes at their listening ports
	the published message form is described in message_formulation function 

	'''
	def udp_publisher(self, centers_score):
		MESSAGE = self.message_formulation(centers_score) # Formulating the write msg to send

		MESSAGE = MESSAGE.encode('utf-8') # encoding the message before sending it

		self.sock = socket.socket(socket.AF_INET, # Internet
		                     socket.SOCK_DGRAM) # UDP

		for node_id in self.participants:
			IP   = self.participants[node_id][2]
			PORT = self.participants[node_id][0]
			self.sock.sendto(MESSAGE, (IP, PORT))

		self.sock.close()


	'''
	message_formulation function takes a list of ints of the form [<center_x>, <center_y>, <score>]
	and transform it to a string ready to be sent !
	The string has the form:
	"node_id.center_x.center_y.score"
	'''

	def message_formulation(self, centers_score):
		return '.'.join(list(map(str, centers_score)))


	'''
	UDP subscriber

	Result of its operation is stored in the dictionary other_nodes_msgs
	other_nodes_msgs has the following structure
	other_nodes_msgs = {<node_id>: [<center_y_coor>, <center_y_coor>, <score>]}

	'''

	def udp_subscriber(self):
		self.other_nodes_msgs = {}	# Initializing other_nodes msgs to none

		self.sock = socket.socket(socket.AF_INET, # Internet
		                     socket.SOCK_DGRAM) # UDP

		for node_id in self.participants:
			IP   = self.participants[node_id][2] # IP of neighbor
			PORT = self.participants[node_id][1] # Neighbor's publishing port (we listener to the publishing port of the neighbor)
			
			self.sock.bind((IP, PORT))

			data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
			
			print("received message:", data.decode('ascii'))
			# Update the other_nodes_msgs
			msg = self.message_reformulation(data.decode('ascii'))
			
			if int(msg[0]) == int(node_id):
				self.other_nodes_msgs[node_id] = msg[1:]

		self.sock.close()


	'''
	Function message_reformulation used to convert the received udp packet from string
	to a list of meaningful elements
	the structure of the result is
	[<center_x_coor>, <center_y_coor>, <node score>]
	all elements are integers ! 
	'''
	def message_reformulation(self, message):
		result = []
		# splitting the message on '.'
		result = message.split('.')
		# Casting the message elements from strings to integers
		result = list(map(int, result))

		return result




	'''
	Getters
	'''

	def get_other_nodes_msgs(self):
		return self.other_nodes_msgs

	def get_participants_ips(self):
		return self.participants

