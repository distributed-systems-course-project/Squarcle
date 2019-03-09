import time
import random
class squarcle_data:
    #################################these are constants that would be used###################################################
    ##GUI designer needs to adjust these parameters based on the view and size of display used
    THRESHOLD = 50 ##this is used as collision distance
    MAX_X = 100
    MAX_Y  = 100
    SHIFT_X = 10 ##shift in X axis from border
    SHIFT_Y = 10 ##shift in Y axis from border
    #################################these are the same for all nodes##########################################################
    number_of_nodes = 0 #number of nodes in the game
    nodes_centers = [["name", [0,0]]] #this should have information about node ID and center, ['A', (32,4)]
    all_scores = [["name", 0]] #this has the scores of all nodes
    corners = [] #this has the centers of corners, once GUI makes polygon assign centers to this list
    ##################################these are specific for one node##########################################################
    node_ID = 0 ##this will be used for voting purposes to choose admin, and also it is the first position of a node in the game
    name = "name" ## this has node name, any identifier is fine
    play = False #updated when game is to start, with the communication thread
    end = False #updated by the end of the sequance or game_over, by
    score = 0 #this has the score of the current node
    timer = [False, 0] #timer for node, set to True means started counting, second index has time which is incremented by 1s
    node_center_location = [0,0] #this holds the location of the node in the plane, updated by GUI
    sequence = [0,[]]#first is index of current corner, updated every time a corner is reached, rest are colours of the sequance, first corner is the node_ID
    collision = "node_name" #set this with the name of node that collided with this node



    def __init__(self, name, number_of_nodes, node_ID):
        self.number_of_nodes = number_of_nodes
        self.name = name
        self.node_ID = node_ID
        self.all_scores = [0] * number_of_nodes

    def set_number_of_nodes(self, number_of_nodes):
        self.number_of_nodes = number_of_nodes
        ##once called, create sequances


    def set_nodes_centers(self, nodes_centers):
        self.nodes_centers = nodes_centers
        ##once called, invoke game logic to compare distances

    def set_all_scores(self, all_scores):
        self.all_scores = all_scores
        ##once called, invoke game logic to decide rank
    def set_play(self, play):
        self.play = play
        self.set_sequence_local()
        self.set_timer()

    def set_end(self, end):
        self.end = end
        ##once called, invoke game logic to end game
    def set_score(self):
        self.score = self.sequence[0] * 10 + int(100/self.timer[1]) ## I am using just this simple formula for score, think of something better
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
    def set_collision(self, collision):
        self.collision = collision
        self.set_end(True)

    def set_corners(self, corners):
        self.corners = corners

    def check_distance_with_nodes(self):
        for j in self.nodes_centers:
            dist = pow(j[1][0] - self.node_center[0], 2) + pow(j[1][1] - self.node_center[1], 2)
            if dist < self.THRESHOLD and j[0] != self.name:
                self.set_collision(j[0])

    def check_distance_with_corners(self):
        for j in self.corners:
            dist = pow(j[0] - self.node_center[0], 2) + pow(j[1] - self.node_center[1], 2)
            if dist < self.THRESHOLD:
                self.set_sequance()

    #####################To do: implement getters################################

