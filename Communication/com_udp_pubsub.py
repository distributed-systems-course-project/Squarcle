# Communication publisher class
import socket
import time
import traceback

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
            ENC_MESSAGE = self.encrypt(MESSAGE)
            ENC_MESSAGE = ENC_MESSAGE.encode('utf-8')  # encoding the message before sending it


            print('length of participants: {}'.format(len(self.participants)))
            print(self.participants)

            for node_id in self.participants:
                self.sock = socket.socket(socket.AF_INET,  # Internet
                                          socket.SOCK_DGRAM)  # UDP

                IP = self.participants[node_id][-1]
                if self.master:
                    PORT = self.participants[node_id][2]
                else:  # slave
                    PORT = self.participants[node_id][1]

                print('UDP publisher msg: {}'.format(MESSAGE))
                print('UDP publisher encrypted msg: {}'.format(ENC_MESSAGE))
                try:
                    self.sock.sendto(ENC_MESSAGE, (IP, int(PORT)))
                except Exception as e:
                    print("error in publisher")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    self.data.logger(False, e)
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

        print('Message formulation: Node centers: {}'.format(nodes_centers))
        print('Message formulation: Node scores: {}'.format(all_score))


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

        print('Message before sending: {}'.format(message))

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
                            PORT = self.participants[node_id][1]  # Neighbor's publishing port (we listener to the publishing port of the neighbor)
                        else:
                            PORT = self.participants[node_id][2]
                        #print('UDP subscriber msg:{}'.format())
                        # print('IP: {}, PORT: {}'.format(IP, PORT))
                        self.sock.bind((IP, PORT))

                        data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes

                        print("received UDP encrypted message: {}".format(data.decode('ascii')))

                        # Decryption
                        data = self.decrypt(data.decode('ascii'))
                        print("received UDP message: {}".format(data))
                        # Update the other_nodes_msgs
                        self.data_extraction_from_udp_msg(data)
                        # Update shared store
                        self.update_squarcle_data()

                        self.sock.close()
                    except Exception as e:
                        print("error here ")
                        traceback.print_exception(type(e), e, e.__traceback__)
                        self.data.logger(False, e)


            except Exception as e:
                print('Problem with UDP')
                traceback.print_exception(type(e), e, e.__traceback__)
                self.data.logger(False, e)
            finally:
                self.sock.close()

    '''
	data_extraction_from_udp_msg
	received msg have the following format
	node_name1.cx1.cy1.score1
	'''

    def data_extraction_from_udp_msg(self, message):
        # Old information extraction
        self.data.acquire()
        old_scores = self.data.all_scores
        old_nodes_centers = self.data.nodes_centers
        self.data.release()

        centers_gatherer = []
        score_gatherer = []
        self.received_centers = []
        self.received_scores = []
        # splitting the message on '.'
        received_info = message.split('.')

        # Create correct all scores
        if old_scores[0][0] == 'name':
            old_scores = []
            for key, participant_data in self.participants.items():
                old_scores.append([str(key), 0])
            self.data.acquire()
            self.all_scores = old_scores
            print('Updated local scores: {}'.format(old_scores))
            print('Updated squarcle scores: {}'.format(self.all_scores))
            self.data.release()

        if old_nodes_centers[0][0] == 'name':
            old_nodes_centers = []
            for key, participant_data in self.participants.items():
                old_nodes_centers.append([str(key), [0, 0]])
            self.data.acquire()
            self.nodes_centers = old_nodes_centers
            print('Updated local nodes centers²: {}'.format(old_nodes_centers))
            print('Updated squarcle nodes centers: {}'.format(self.data.nodes_centers))
            self.data.release()

        if self.master:
            # master receives a msg of the form : node_name.cx.cy.score from slave


            # Casting the message elements from strings to integers
            for particpant in old_nodes_centers:
                if particpant[0] == str(received_info[0]):
                    particpant[1] = [int(received_info[1]), int(received_info[2])]# [node_name, [cx, cy]]
                self.received_centers = old_nodes_centers

            for particpant in old_scores:
                if particpant[0] == str(received_info[0]):
                    particpant[1] = int(received_info[3])
                #self.received_scores.append([str(received_info[0]), int(received_info[3])])  # [node_name, score]
                self.received_scores = old_scores
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
    encrypt function
    Arguments:
        content: (string) udp packet content to encrypt
        key: (string) key to use for encryption
    Return:
        cypher: (string) encrypted udp packet content
    The encryption consists of XORing each character of the content with
    the corresponding character of the key 
    '''
    def encrypt(self, content):
        cypher = ''
        key = len(content)*'A'

        for [x, y] in zip(content, key):

            cypher+=chr(ord(x) ^ ord(y))

        return cypher

    '''
    decrypt function
    Arguments:
        cypher: (string) cypher content to decrypt
        key: (string) key to use for decryption
    Return:
        plain_text: (string) decrepted udp encrypted packet content
    The decryption consists of XORing each character of the cypher string with
    the corresponding character of the key 
    '''
    def decrypt(self, cypher):
        plain_text = ''
        key = len(cypher) * 'A'

        for [x, y] in zip(cypher, key):

            plain_text+=chr(ord(x) ^ ord(y))

        return plain_text

    '''
	Getters
	'''

    def get_other_nodes_msgs(self):
        return self.other_nodes_msgs

    def get_participants_ips(self):
        return self.participants
