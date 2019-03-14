##### Notes ##############################################################################################################
##### Make sure you use the lock.acquire before you use this object, and before lock.release call self.set_timer
##### GUI uses the following:
#####       -Number of nodes to generate polygon corners, it sets corners list once this is generated
#####       -All constants to decide how close circles are, and window size
#####       -score and time to display them
#####       -Name of node to display it in the GUI
#####       -Play and End to know if there is a collision, if so take the other node center and name from collision
#####       -Read current_sequence to get the center of the next sequance to be followed
#####       -Always check end before anything, if end is true, check lost, if lost is true display game over, else display
#####       score and time while waiting for other nodes to be all done, this will be checked in all_scores_ready == true
#####       -Once all nodes are ready, the ranked scores are in the list all_scores
##### COM uses the following:
#####       -create the object based on number of players, guarantees that each node has unique node_ID in range 0:(number_ofnodes - 1)
#####       -Reads node_center for each node in network, create list with all nodes and update nodes_centers in the same format written below
#####       -Sets play at the beginning of the game to true
#####       -checks End each time, and make a local list oustide this object with all nodes that ended, once all over update scores
#####       -Scores are read from score which gives score of the node, then using all scores update all_scores using its setter
#####
#########################################################################################################################
import time
import random
import threading

class squarcle_data:
    #################################these are constants that would be used###################################################
    ##GUI designer needs to adjust these parameters based on the view and size of display used
    THRESHOLD = 50 ##this is used as collision distance
    MAX_X = 600
    MAX_Y  = 800
    SHIFT_X = 10 ##shift in X axis from border
    SHIFT_Y = 10 ##shift in Y axis from border
    #################################these are the same for all nodes##########################################################
    number_of_nodes = 0 #number of nodes in the game
    nodes_centers = [["name", [0,0]]] #this should have information about node ID and center, ['A', (32,4)]
    all_scores = [["name", 0]] #this has the scores of all nodes
    all_scores_ready = False
    playability = False
    nodes_at_game_start = {}
    slave_master = {} # Master parameters: needed when operating as a slave !
    corners = [] #this has the centers of corners, once GUI makes polygon assign centers to this list
    lock = 0 #this is a lock for the shared data, use it between all threads for synchronization
    colours = []
    corners_and_colours_pairs = 0
    next_color_corner_pair = 0
    color_counter = 0
    ##################################these are specific for one node##########################################################
    node_ID = 0 ##this will be used for voting purposes to choose admin, and also it is the first position of a node in the game
    name = "name" ## this has node name, any identifier is fine
    play = False #updated when game is to start, with the communication thread
    play_from_com = False
    end = False #updated by the end of the sequance or game_over, to know if node lost or won, check sequance[0] == number_of_nodes
    lost = False #set when end is set, to check whether the node won or lost
    score = 0 #this has the score of the current node
    timer = [False, 0] #timer for node, set to True means started counting, second index has time which is incremented by 1s
    node_center = [0,0] #this holds the location of the node in the plane, updated by GUI
    current_sequence = [0,0] #This is the sequance that needs to be achieved next, GUI uses this
    sequence = [0,[]]#first is index of current corner, updated every time a corner is reached, rest are colours of the sequance, first corner is the node_ID
    collision = ["name", [0,0]] #set this with the name of node that collided with this node, and put center




    def __init__(self):
        self.lock = threading.Lock()
    

    def release(self):
        self.lock.release()
        #self.set_timer()

    def acquire(self):
        self.lock.acquire()

    def set_parameters(self, number_of_nodes, node_ID):
        self.number_of_nodes = number_of_nodes
        self.node_ID = node_ID
        self.all_scores = [0] * number_of_nodes
        self.randomize_corners()
        self.generate_colors()
        self.corners_and_colours_pairs = [self.corners, self.colours]
        self.next_color_corner_pair = [self.corners_and_colours_pairs[0][self.color_counter],self.corners_and_colours_pairs[1][self.color_counter]]

    def set_number_of_nodes(self, number_of_nodes):
        self.number_of_nodes = number_of_nodes
        ##once called, create sequances

    def set_name(self, name):
        self.name = name

    def set_node_ID(self, node_ID):
        self.node_ID = node_ID

    def set_nodes_centers(self, nodes_centers):
        self.nodes_centers = nodes_centers
        self.check_distance_with_nodes()
        self.check_distance_with_corners()
        ##once called, invoke game logic to compare distances

    def set_playability(self, playability):
        self.playability = playability

    def set_all_scores(self, all_scores):
        self.all_scores = all_scores
        self.all_scores[self.node_ID] = self.score
        self.rank_scores()
        self.all_scores_ready = True
    def set_play(self, play):
        self.play = play
        self.set_sequence_local()
        self.set_timer()

    def set_end(self, end):
        self.end = end
        if self.sequence[0] == (self.number_of_nodes - 1):
            self.lost = False
        else:
            self.lost = True
            self.score = 0
    def set_score(self):
        if self.timer[1] != 0:
            self.score = self.sequence[0] * 10 + int(100/self.timer[1]) ## I am using just this simple formula for score, think of something better
        else:
            self.score = 0
        self.all_scores[self.node_ID] = self.score
    def set_node_center(self, node_center):
        self.node_center = node_center

    def set_timer(self):# call this function always before you release the lock to keep time up to date
        self.timer[1] = int(time.time()) - self.timer[1]
        self.timer[0] = True
        self.set_score()

    def set_sequence_local(self):
        self.sequence[1].append(self.node_ID)
        for i in range(1, self.number_of_nodes):
            self.sequence[1].append(random.randint(0, self.number_of_nodes-1))
            while self.sequence[1][i] == self.sequence[1][i-1]:
                self.sequence[1][i] = random.randint(0, self.number_of_nodes-1)
    def set_sequance(self):
        self.sequence[0] = self.sequence[0] + 1
        self.set_score()
        if self.sequence[0] == (self.number_of_nodes - 1):
            self.set_end(True)
        else:
            self.set_current_sequence()
    def set_current_sequence(self):
        self.current_sequence = self.corners[self.sequence[1][self.sequence[0]]]
    def set_collision(self, collision):
        self.collision = collision
        self.set_end(True)

    def set_corners(self, corners):
        self.corners = corners

    def check_distance_with_nodes(self):
        for j in self.nodes_centers:
            dist = pow(j[1][0] - self.node_center[0], 2) + pow(j[1][1] - self.node_center[1], 2)
            if dist < self.THRESHOLD and j[0] != self.name:
                self.set_collision(j)

    def check_distance_with_corners(self):
        if not self.end:
            dist = pow(self.current_sequence[0] - self.node_center[0], 2) + pow(self.current_sequence[1] - self.node_center[1], 2)
            if dist < self.THRESHOLD and self.sequence[0]:
                self.set_sequance()
                self.color_counter = self.color_counter + 1
                self.next_color_corner_pair = self.corners_and_colours_pairs[self.color_counter]

    def randomize_corners(self):
        x_slice = int(self.MAX_X / self.number_of_nodes)
        y_slice = int(self.MAX_Y / self.number_of_nodes)
        list_of_regions = []
        for i in range(1, self.number_of_nodes):
            for j in range(1, self.number_of_nodes):
                list_of_regions.append([False, ((x_slice * i), (y_slice * j))])
        for i in range(0, self.number_of_nodes):
            while True:
                m = random.randint(0, len(list_of_regions))
                if not list_of_regions[m][0]:
                    list_of_regions[m][0] = True
                    self.corners.append(list_of_regions[m][1])
                    break
    def generate_colors(self):
        c = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        for j in range(0, self.number_of_nodes):
            x = "#"
            for i in range(0,6):
                x = x + c[random.randint(0,15)]
            self.colours.append(x)
    def rank_scores(self):
        for j in range(0, self.number_of_nodes):
            for i in range(0, self.number_of_nodes):
                if i!=j:
                    if self.all_scores[1][i] < self.all_scores[1][j]:
                        temp = self.all_scores[j]
                        self.all_scores[j] = self.all_scores[i]
                        self.all_scores[i] = temp





    #####################To do: implement getters################################

