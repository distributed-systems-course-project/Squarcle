# Communication TCP listener class
import socket 		# To manage sockets
import traceback


class Tcp_Initiator:

    tcp_ip = 0
    tcp_port = 0
    participants = {}		# Dictionary: {'participant_id': [listening_at, publishing_at]} udp ports
    BUFFER_SIZE = 1024
    sock = '' # Socket
    node_id = 0
    data = '' # Squarecle data object
    node_subnet_ip = ''
    isTimeOut = False

    def __init__(self, tcp_ip, tcp_port, node_id, node_subnet_ip, data):
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.node_id = node_id
        self.BUFFER_SIZE = 1024
        self.participants = dict()
        self.node_subnet_ip = node_subnet_ip
        self.data = data
        self.isTimeOut = False


    '''
    tcp_connect function
    Arguments:
        TCP_IP: (string) server's tcp_ip address to be used
        TCP_PORT: (integer) server's tcp open port
        MESSAGE: (string) Message to send to the server
    return
        data: (binary string) server reply message to our sent message
    Note that tcp_connection initializes the tcp_ip connection of  the client to the server
    the message in encoded into binary string so that it can be sent
    '''
    def tcp_listen(self):
        data = ""

        self.data.acquire()
        node_name = self.data.name
        self.data.release()

        if not self.participants:  # No participants yet !
            udp_port = self.tcp_port + 1
        else: 				 # There are other participants
            # The list bellow takes the last participant's udp port nbr and adds 1 to it to initialize udp_port
            print(self.participants)
            udp_port = self.participants[ list( self.participants.keys())[-1] ][-2] + 1

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        try:
            self.sock.bind((self.tcp_ip, self.tcp_port))

            self.sock.listen(1)
            self.isTimeOut = False

            conn, addr = self.sock.accept()
            while True:
                tmp = conn.recv(self.BUFFER_SIZE)
                if not tmp: break
                data = str(tmp.decode('ascii')) # data is the neighbor node ID

                data = self.first_msg_interpreter(data) # return a list [node_name, node_id]
                print(data)
                # Generate 2 free udp port nbr
                self.participants[data[1]] = [] # Keys of the dictionary are the IDs!
                self.participants[data[1]].append(int(data[0])) # name of the node

                for i in range(2):
                    while(not self.checkPort(udp_port)):
                        udp_port+=1
                    self.participants[data[1]].append(udp_port)
                    udp_port+=1

                to_send = self.tcp_echo_msg(node_name, data[1]) # to send should contain [<node_id>, <node_name>, <udp_listening_port>, <udp_publiishing_port> ]

                conn.send(to_send.encode('utf-8'))  # echo
        except Exception as e:
            self.isTimeOut = True
            traceback.print_exception(type(e), e, e.__traceback__)
            self.data.logger(False, e)

        finally:
            self.sock.close()


    '''
    first_msg_interpreter take the first received tcp msg
    if should have the form name.node_id 
    Retruns: a list of strings of the form: [<node_name>, <node ID>]
    '''
    def first_msg_interpreter(self, data):
        return data.split('.')

    '''
    Function used to check port availability
    Input:
        port: integer => port number to check
    Return:
        result: boolean => True if port is not in use; false otherwise
    '''
    def checkPort(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = False
        try:
            sock.bind(("0.0.0.0", port))
            result = True
        except:
            result = False
        sock.close()
        return result

    '''
    Function to generate TCP/IP communication playback message
    returns a string
    '''
    def tcp_echo_msg(self, current_node_name,neighbor_id):
        msg_struct = [str(current_node_name), str(self.node_id), str(self.participants[neighbor_id][1]), str(self.participants[neighbor_id][2])]
        print('strcut msg')
        print(msg_struct)
        return '.'.join(msg_struct)


    '''
    neighboring nodes ips function uses provided subnet to formulate
    IP addresses of other discovered nodes.
    The results are stores in the global variable participants
    '''
    def neighboring_nodes_ips(self, participants):
        for node_id, udp_ports in participants.items():
            if not isinstance(udp_ports[-1], str):
                udp_ports.append( self.node_subnet_ip + '.' +  str(udp_ports[0]) )
        return participants

    '''
    Used when user needs to join a game !
    '''
    def tcp_joiner(self, neighbor_node_nbr, node_subnet):
        neighbor_ip = node_subnet + '.' + str(neighbor_node_nbr)

        self.data.acquire()
        node_name = self.data.name
        self.data.release()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((neighbor_ip, self.tcp_port))

        to_send = str(self.node_id) + '.' + node_name		# Initial joining TCP msg has the form node_name.node_id

        try:
            self.sock.sendall(to_send.encode('utf-8'))

            while True:
                data = self.sock.recv(self.BUFFER_SIZE) # node_id.node_name.udp_l_port.udp_p_port
                if data: break

            self.participants = self.extract_master_msg(data)	# master is stored here

        finally:
            self.sock.close()


    '''
    extract_master_msg encapsulate the message received from the 
    '''
    def extract_master_msg(self, data):
        data = data.decode('ascii')

        participant = data.split('.') # [node_id, node_name, l_port, pub_port]

        udp_ports = list(map(int, participant[2:]))

        udp_ports.insert(0, int(participant[1]))

        # participant = {'node_ID': [<node_name>, <udp_L_port>, <udp_P_port>]}
        participant = {str(participant[0]):  udp_ports}

        return participant


    '''
    Start the game
    '''
    def start_the_game(self, participants, master):
        if master:
            print('from start the game func')
            print(self.participants.items())
            i = 0
            local_participants = participants.copy()
            for node_name, neighbor_param in local_participants.items():
                i+=1
                print('me9bel')
                print(participants)

                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("neighbor param")
                print(neighbor_param)

                ip = neighbor_param[-1]
                print('li 9alek int')
                print(ip)
                self.sock.connect((ip, self.tcp_port))

                message = self.start_msg_builder(participants, ip)

                self.sock.send(message.encode('utf-8'))
                _ = self.sock.recv(self.BUFFER_SIZE)

                self.sock.close()
            print('i at the end of for loop: {}'.format(i))
        else:

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.sock.bind((self.tcp_ip, self.tcp_port))
            self.sock.listen(1)

            conn, addr = self.sock.accept()

            while 1:
                data = conn.recv(self.BUFFER_SIZE)
                if not data: break
                data = data.decode('ascii')

                self.extract_start_msg_and_update_data(data)

                msg = "OK"
                conn.send(msg.encode('utf-8'))  # echo

            self.sock.close()

    '''
    Starting msg has the form
    True.node_name.node_id
    '''
    def start_msg_builder(self, participants, ip):

        self.data.acquire()
        #self.data.nodes_at_game_start = participants
        current_node_name = self.data.name
        current_node_ID   = self.data.node_ID
        self.data.set_parameters(len(participants), self.node_id)
        self.data.play_from_com = True
        self.data.release()

        message = 'True.'

        # Get all participants' keys
        keys = list(participants.keys())

        to_remove = ''
        # Removing not needed participant
        print('before removing')
        print(participants)
        for key in keys:
            if participants[key][-1] == ip:
                to_remove = key

        del participants[to_remove]
        del keys[keys.index(to_remove)]

        participants[current_node_name] = [current_node_ID]
        keys.append(current_node_name)
        print('participants after removing target')
        print(participants)
        # Build the msg
        for key in keys:
            message += (key + '.')

            message += (str(participants[key][0]) + '.') # node id that corresponds to that key

        print('Start msg: {}'.format(message[:-1]))
        return message[:-1]


    '''
    Start message extractor
    data should have the form
    True.node_name1.node_id1.node_name2.node_id2.......
    '''
    def extract_start_msg_and_update_data(self, data):
        data = data.split('.')
        print(data)
        start_bool = bool(data[0])
        del data[0]
        participants = {}

        print(data)

        for i in range(0, len(data), 2):
            participants[data[i]] = [int(data[i+1])]

        self.data.acquire()
        self.data.nodes_at_game_start = participants
        self.data.set_parameters(len(participants), self.node_id)
        self.data.play_from_com = start_bool
        self.data.release()
        self.participants = participants


    '''
    Timeout checker
    '''
    def get_timeout(self):
        return self.isTimeOut
    '''
    Needed to close connection socket if something unexpected happened
    '''
    def close_tcp_listener(self):
        try:
            self.sock.close()
        except:
            pass
        return

    '''
    getters
    '''
    def get_participants(self):
        return self.participants

    '''
    Setters
    '''
    def set_participants(self, participants):
        self.participants = participants
