# Temporal main for communication !
from Communication import com_init 		   ## Initializer of communication parameters
from Communication import com_tcp_initiator ## Other node addition manager
from Communication import com_udp_pubsub	# UDP publish subscribe implementation 
from squarcle_data import squarcle_data
import threading


class ComOrchestrator:

    data 		 = ''	# Squarcle_data object !
    com_init_obj = ""   # Communication initializer
    tcp_obj 	 = ''	# TCP object
    '''
    ComOrchestrator class constructor takes a squarcle_data object
    This objects would be shared between all aspects of this program
    The access to this object is through a lock  => Entry data consistency
    '''
    def __init__(self, data):
        self.data = data 	# Initialization of squarcle data object

        # Communication initializer object
        # Initialization done whether player wants to start a new game or joining an existing game
        self.com_init_obj = com_init.Com_Init(self.data)

        # TCP listener object
        self.tcp_obj = com_tcp_initiator.Tcp_Initiator( self.com_init_obj.get_node_ip(),
                                                        self.com_init_obj.get_node_tcp_port(),
                                                        self.com_init_obj.get_node_nbr(),
                                                        self.com_init_obj.get_node_subnet_ip(),
                                                        self.data)

        # Check if user has a wireless card connected !
        self.data.acquire()
        self.data.set_playability(self.com_init_obj.get_can_play())
        self.data.release()

    '''
    Starter function starts the communication thread and all what's needed !
    '''
    def master_starter(self):
        print("Your ID is: " + str(self.com_init_obj.get_node_nbr()))

        print('Share your ID to start the game !')

        print('Connection parameters:')
        print(self.com_init_obj.get_node_ip())
        print(self.com_init_obj.get_node_tcp_port())
        print(self.com_init_obj.get_node_subnet_ip())
        print(self.com_init_obj.get_can_play())

        # Should be put in a thread !
        self.data.acquire()
        self.tcp_obj.set_participants(self.data.participants)
        self.data.release()

        self.tcp_obj.tcp_listen() # blocking instruction

        for player in self.tcp_obj.get_participants():
            print('Player "' + str(player) + '" has joint the game !')

        if not self.tcp_obj.get_timeout():
            # Adding connected
            self.data.acquire()
            self.data.set_participants(self.tcp_obj.get_participants())
            self.data.set_nodes_to_admin(list(self.tcp_obj.get_participants().keys())[-1])
            self.data.release()

        # Building finalized participants dictionary {'node_name': [<node_ID>, <l_port>, <pub_port>, <IP>]}
        participants = self.tcp_obj.neighboring_nodes_ips(self.tcp_obj.get_participants())

        self.data.acquire()
        self.data.nodes_at_game_start = participants
        self.data.release()

    def close_master_tcp_connection(self):

        self.tcp_obj.close_tcp_listener()

    def slave_starter(self):

        # implement an ID verification !
        self.data.acquire()
        join_id = int(self.data.creator_ID)
        self.data.release()

        self.tcp_obj.tcp_joiner(join_id, self.com_init_obj.get_node_subnet_ip())
        participants = self.tcp_obj.neighboring_nodes_ips(self.tcp_obj.get_participants())

        self.data.acquire()
        self.data.nodes_at_game_start = participants
        self.data.number_of_nodes	  = len(participants)
        self.data.slave_master 		  = participants
        self.data.release()

    def game_starter(self,master):

        '''
        add a new function here named master_game_starter
        The function would be able to use participants from the shared squarcle_data
        This thread should be called from the GUI start button click
        It is simulated below as input()
        It can be used as a master an slave with the right parameters !
        '''
        self.data.acquire()
        participants = self.data.nodes_at_game_start
        self.data.release()

        if master:

            # Publish start message
            self.tcp_obj.start_the_game(participants.copy(), master=True)

            self.data.acquire()
            print('nodes at game start after running start the game func')
            print(self.data.nodes_at_game_start)
            self.data.release()

        else:

            self.tcp_obj.start_the_game(participants, master=False)

            self.data.acquire()
            print(self.data.nodes_at_game_start)
            self.data.release()

    def udp_start(self, master):
        print('UDP called !')

        self.data.acquire()
        participants =  self.data.nodes_at_game_start
        self.data.release()

        if master:
            # Master
            #Initialization of udp_pubsub object
            udp_pubsub = com_udp_pubsub.udp_pubsub( self.com_init_obj.get_node_ip(),
                                                    participants,
                                                    self.data,
                                                    True) # Master mode = True

        else:
            # Slave

            #Initialization of udp_pubsub object
            self.data.acquire()
            master_participant = self.data.slave_master
            self.data.release()

            udp_pubsub = com_udp_pubsub.udp_pubsub( self.com_init_obj.get_node_ip(),
                                                    master_participant,
                                                    self.data,
                                                    False,	# Master mode = False
                                                    slave_participants = self.tcp_obj.get_participants())


        subscriber_thread = threading.Thread(name='subscriber_thread',
                                             target=udp_pubsub.udp_subscriber)

        # Use udp_pubsub udp_publisher to send data to other nodes
        publisher_thread = threading.Thread(name='publisher_thread',
                                             target= udp_pubsub.udp_publisher)

        # Start the subscriber thread
        subscriber_thread.start()
        # Start the publisher thread
        publisher_thread.start()

