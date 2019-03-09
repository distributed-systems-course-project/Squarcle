# Temporal main for communication !
from Communication import com_init

# Communication initializer object
com_init_obj = com_init.Com_Init()

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

	else:
		# implement an ID verification !
		join_id = int(input("Enter your friend's ID: "))

else:
	print('Sorry ! Your computer does not support this game')
