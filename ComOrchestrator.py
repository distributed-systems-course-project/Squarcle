# Temporal main for communication !
from Communication import com_init 		   ## Initializer of communication parameters
from Communication import com_tcp_initiator ## Other node addition manager
from Communication import com_udp_pubsub	# UDP publish subscrib implementation 
from squarcle_data import squarcle_data
import threading


class ComOrchestrator:

	data 		 = ''	# Squarcle_data object !
	com_init_obj = ""   # Communication initializer
	tcp_obj 	 = ''	# TCP object
	playability  = False # Playability flag (check com_init for more details )
	'''
	ComOrchestrator class constructor takes a squarcle_data object
	This objects would be shared between all aspects of this program
	The access to this object is through a lock  => Entry data consistency
	'''
	def __init__(self, data):
		self.data = data 	# Initialization of squarcle data object
		
		# Communication initializer object
		# Initialization done whether player wants to start a new game or joining an existing game
		self.com_init_obj = com_init.Com_Init()

		# TCP listener object
		self.tcp_obj = com_tcp_initiator.Tcp_Initiator(self.com_init_obj.get_node_ip(), 
														self.com_init_obj.get_node_tcp_port(),
														self.com_init_obj.get_node_nbr())

		# Check if user has a wireless card connected !
		self.playability = self.com_init_obj.get_can_play()

	'''
	Starter function starts the communication thread and all what's needed !
	'''
	def master_starter(self):
		join_id = 0

		print("Your ID is: " + str(self.com_init_obj.get_node_nbr()))

		print('Share your ID to start the game !')

		print('Connection parameters:')
		print(self.com_init_obj.get_node_ip())
		print(self.com_init_obj.get_node_tcp_port())
		print(self.com_init_obj.get_node_subnet_ip())
		print(self.com_init_obj.get_can_play())

		isAllPlayersIn = False
		# Starting the TCP listener (it should be a thread !)
		while not isAllPlayersIn:
			# Should be put in a thread !
			self.tcp_obj.tcp_listen() # blocking instruction

			for player in self.tcp_obj.get_participants():
				print('Player "'+ str(player) + '" has joint the game !')
			
			answer = input('Are those all the players ?\n1 => yes \t 2 => no\n==> ')

			if answer == '1':
				isAllPlayersIn = True
				self.tcp_obj.close_tcp_listener() # close listener if still open

		for player, udp_ports in self.tcp_obj.get_participants().items():
			print('Player: {}, listening at {}, publishing at {}'.format(player, udp_ports[0], udp_ports[1]))


		#Initialization of udp_pubsub object
		udp_pubsub = com_udp_pubsub.udp_pubsub(self.com_init_obj.get_node_subnet_ip(), self.tcp_obj.get_participants())
		print('From udp_pubsub')
		print(udp_pubsub.get_participants_ips())
		
		udp_pubsub.udp_subscriber()
		print('Neighbor said :')
		print(udp_pubsub.get_other_nodes_msgs())

		# Use udp_pubsub udp_publisher to send data to other nodes
		udp_pubsub.udp_publisher([150,150,8000])
				

	def slave_starter(self):

		# implement an ID verification !
		join_id = int(input("Enter your friend's ID: "))
		
		self.tcp_obj.tcp_joiner(join_id, self.com_init_obj.get_node_subnet_ip())

		udp_pubsub = com_udp_pubsub.udp_pubsub(self.com_init_obj.get_node_subnet_ip(), self.tcp_obj.get_participants())
		print('From udp_pubsub')
		print(udp_pubsub.get_participants_ips())
		
		udp_pubsub.udp_subscriber()
		print('Neighbor said :')
		print(udp_pubsub.get_other_nodes_msgs())

		# Use udp_pubsub udp_publisher to send data to other nodes
		udp_pubsub.udp_publisher([150,150,8000])


	def get_playability(self):
		return self.playability
