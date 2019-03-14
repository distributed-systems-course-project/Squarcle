from squarcle_data import squarcle_data
from ComOrchestrator import ComOrchestrator
import threading

data = squarcle_data()
#Starting GUI to acquire initial information




##Launching the communication thread here
# Initializing a communication orchestrator object
orchestrator_obj = ComOrchestrator(data)

# Check if user has a wireless card connected !
if data.playability:
	# User can play the game

	# This should be replaced by a function from the GUI
	choice = input('1 => Start a new game\t 2=> Join a game\n===> ')
	com_thread = threading.Thread()

	if choice == "1":
		# This node is a master
		com_thread = threading.Thread(name='Com_thread', target=orchestrator_obj.master_starter)
		com_thread.start()

	else:
		# This node is a slave
		com_thread = threading.Thread(name='Com_thread', target=orchestrator_obj.slave_starter)
		com_thread.start()

	com_thread.join()
	# Wait for start instruction
	input('Press enter to start the game')

	if choice == '1': # Master mode
		com_thread = threading.Thread(name='Com_game_start', target=orchestrator_obj.game_starter, args=(True,))
		com_thread.start()
	else: # Slave mode
		com_thread = threading.Thread(name='Com_game_start', target=orchestrator_obj.game_starter, args=(False,))
		com_thread.start()


else:
	# User cannot play this game since no wireless card was found on his device
	print('Unable to identify any wireless network card on this node !')
	print('Sorry ! Your computer does not support this game')

################## End of communication thread #############################


##once launched, and number of nodes is known in the communication thread, call set_parameters
##Also you need to decide a unique ID for each node, this could be ordering by connection time, like 0, 1, 2 depending on connecting rank
#data.set_parameters(4, 1)


##GUI continues

#=======
#print(data.corners)

