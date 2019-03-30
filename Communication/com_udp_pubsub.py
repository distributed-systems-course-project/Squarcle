# Communication publisher class
import socket
import time


class udp_pubsub:
    participants = {}
    slave_participants = {}
    other_nodes_msgs = {}
    master = False  # Operating mode
    sock = ''
    data = ''  # Squarcle data
    received_centers = []
    received_scores = []
    node_ip = ''  # Current node IP

    '''
	Constructor
	Takes a string that contains master node subnet network
	and dictionary of participants (created at tcp_listener class) 
	Dictionary: {'participant_id': [listening_at, publishing_at]} udp ports
	'''

    def __init__(self, node_ip, participants, data, master, slave_participants={}):
        self.node_ip = node_ip
        self.participants = participants
        self.other_nodes_msgs = {}
        self.data = data
        self.slave_participants = slave_participants
        self.master = master
        self.received_centers = []
        self.received_scores = []

    # It should start udp_subscriber thread and udp_publisher thread

    '''
	Publishes current node information and states to other neighboring nodes ! 
	centers_score is a list of integers of the form [<center_x>, <center_y>, <score>]
	The message will be published to all neighboring nodes at their listening ports
	the published message form is described in message_formulation function 

	'''

    def udp_publisher(self):
        while True:
            time.sleep(1 / 10)
            MESSAGE = self.message_formulation()  # Formulating the write msg to send

            MESSAGE = MESSAGE.encode('utf-8')  # encoding the message before sending it

            # print('Message from UDP: {}'.format(MESSAGE))

            self.sock = socket.socket(socket.AF_INET,  # Internet
                                      socket.SOCK_DGRAM)  # UDP
            # print('participants: {}'.format(len(self.participants)))
            for node_id in self.participants:
                IP = self.participants[node_id][-1]
                if self.master:
                    PORT = self.participants[node_id][2]
                else:  # slave
                    PORT = self.participants[node_id][1]
                try:
                    print('UDP publisher msg: {}'.format(MESSAGE.decode('ascii')))
                    self.sock.sendto(MESSAGE, (IP, PORT))
                except Exception as e:
                    print("error in publisher")
                finally:
                    self.sock.close()

    '''
	message_formulation function reads data from the shared squarcle_data and send it 
	The operation is asynchronous (UDP) 

	message format
	node_name1.cx1.cy1.score1.node_name2.cx2.cy2.score2....
	'''

    def message_formulation(self):

        self.data.acquire()
        nodes_centers = self.data.nodes_centers  # [['name', [cx, cy]]]
        current_node_location = self.data.node_center  # [cx, cy]
        all_score = self.data.all_scores  # [['name', score]]
        current_node_score = self.data.score  # score (int)
        current_node_name = self.data.name
        self.data.release()

        message = ''

        if self.master:
            # appending other nodes informations
            for i in range(len(nodes_centers)):  # nodes_centers[['name', [cx,cy]],..]
                message += (str(nodes_centers[i][0]) + '.' +  # node_name.
                            str(nodes_centers[i][1][0]) + '.' +  # cx
                            str(nodes_centers[i][1][1]) + '.' +  # cy
                            str(all_score[i][1]) + '.')  # score
            # starting by current node information
        message = (current_node_name + '.' +  # node_name.
                   str(current_node_location[0]) + '.' +  # cx
                   str(current_node_location[1]) + '.' +  # cy.
                   str(current_node_score) + '.')

        return message[:-1]  # removing last '.'

    '''
	UDP subscriber
	'''

    def udp_subscriber(self):
        while True:
            time.sleep(1 / 10)
            self.other_nodes_msgs = {}  # Initializing other_nodes msgs to none
            try:

                for node_id in self.participants:
                    self.sock = socket.socket(socket.AF_INET,  # Internet
                                              socket.SOCK_DGRAM)  # UDP
                    try:
                        # IP   = self.participants[node_id][-1] # IP of neighbor
                        IP = self.node_ip
                        if self.master:
                            PORT = self.participants[node_id][
                                1]  # Neighbor's publishing port (we listener to the publishing port of the neighbor)
                        else:
                            PORT = self.participants[node_id][2]
                        #print('UDP subscriber msg:{}'.format())
                        # print('IP: {}, PORT: {}'.format(IP, PORT))
                        self.sock.bind((IP, PORT))

                        data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes

                        print("received UDP message: {}".format(data.decode('ascii')))
                        # Update the other_nodes_msgs
                        self.data_extraction_from_udp_msg(data.decode('ascii'))
                        # Update shared store
                        self.update_squarcle_data()

                        self.sock.close()
                    except Exception as e:
                        print("error here ")


            except Exception as e:
                print('Problem with UDP')
                print(e.with_traceback())
            finally:
                self.sock.close()

    '''
	data_extraction_from_udp_msg
	received msg have the following format
	node_name1.cx1.cy1.score1
	'''

    def data_extraction_from_udp_msg(self, message):
        received_info = []
        centers_gatherer = []
        score_gatherer = []
        self.received_centers = []
        # splitting the message on '.'
        received_info = message.split('.')

        if self.master:
            # master receives a msg of the form : node_name.cx.cy.score from slave

            # Casting the message elements from strings to integers
            self.received_centers.append([str(received_info[0]),
                                          [int(received_info[1]), int(received_info[2])]])  # [node_name, [cx, cy]]

            self.received_scores.append([str(received_info[0]), int(received_info[3])])  # [node_name, score]

        else:
            # slave receives msg from master of the form : node_name1.cx1.cy1.score1.node_name2.cx2.cy2.score2...
            for i in range(0, len(received_info), 4):
                centers_gatherer.append([str(received_info[i]),
                                         [int(received_info[i + 1]),
                                          int(received_info[i + 2])]])  # [node_name, [cx, cy]]

                score_gatherer.append([str(received_info[i]),
                                       int(received_info[i + 3])])

            self.received_centers = centers_gatherer
            self.received_scores = score_gatherer
        '''	
		print('Treated received udp msg')
		print(self.received_centers)
		print(self.received_scores)
		'''
        return

    '''
	After the reception of the message is confirmed from the subscriber
	The message will be decomposed using data_extraction_from_udp_msg
	Once data is extracted, this function will update the shared data store
	'''

    def update_squarcle_data(self):
        self.data.acquire()
        self.data.set_nodes_centers(self.received_centers)
        self.data.set_all_scores(self.received_scores)
        self.data.all_scores_ready = True
        self.data.release()

    '''
	Getters
	'''

    def get_other_nodes_msgs(self):
        return self.other_nodes_msgs

    def get_participants_ips(self):
        return self.participants
