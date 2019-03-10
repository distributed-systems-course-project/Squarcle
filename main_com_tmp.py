# Temporal main for communication !
from Communication import com_init 		   ## Initializer of communication parameters
from Communication import com_tcp_listener ## Other node addition manager
from Communication import com_udp_pubsub	# UDP publish subscrib implementation 

# Communication initializer object
# Initialization done whether player wants to start a new game or joining an existing game
com_init_obj = com_init.Com_Init()

# TCP listener object
tcp_listener_obj = com_tcp_listener.Tcp_Listener(com_init_obj.get_node_ip(), 
												com_init_obj.get_node_tcp_port(),
												com_init_obj.get_node_nbr())


# Check if user has a wireless card connected !
if com_init_obj.get_can_play:
	choice = input('1 => Start a new game\t 2=> Join a game\n===> ')

	join_id = 0

	if choice == "1":
		print("Your ID is: " + str(com_init_obj.get_node_nbr()))

		print('Share your ID to start the game !')

		print('Connection parameters:')
		print(com_init_obj.get_node_ip())
		print(com_init_obj.get_node_tcp_port())
		print(com_init_obj.get_node_subnet_ip())
		print(com_init_obj.get_can_play())

		isAllPlayersIn = False
		players = []
		# Starting the TCP listener (it should be a thread !)
		while not isAllPlayersIn:
			players.append( tcp_listener_obj.tcp_listen() )
			for player in players:
				print('Player "'+ player+ '" has joint the game !')
			
			answer = input('Are those all the players ?\n1 => yes \t 2 => no\n==> ')

			if answer == '1':
				isAllPlayersIn = True
				tcp_listener_obj.close_tcp_listener() # close listener if still open

		for player, udp_ports in tcp_listener_obj.get_participants().items():
			print('Player: {}, listening at {}, publishing at {}'.format(player, udp_ports[0], udp_ports[1]))


		#Initialization of udp_pubsub object
		udp_pubsub = com_udp_pubsub.udp_pubsub(com_init_obj.get_node_subnet_ip(), tcp_listener_obj.get_participants())
		print('From udp_pubsub')
		print(udp_pubsub.get_participants_ips())
		
		udp_pubsub.udp_subscriber()
		print('Neighbor said :')
		print(udp_pubsub.get_other_nodes_msgs())


	else:
		# implement an ID verification !
		join_id = int(input("Enter your friend's ID: "))




else:
	print('Sorry ! Your computer does not support this game')
