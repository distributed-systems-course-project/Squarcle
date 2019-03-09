class squarcle_data:
    ##these are the same for all nodes
    number_of_nodes = 0 #number of nodes in the game
    nodes_centers = [["name", (0,0)]] #this should have information about node ID and center, ['A', (32,4)]
    all_scores = [["name", 0]] #this has the scores of all nodes
    #these are specific for one node
    name = "name"
    play = False #updated when game is to start, with the communication thread
    end = False #updated by the end of the sequance or game_over, by
    score = 0 #this has the score of the current node
    node_center_location = (0,0) #this holds the location of the node in the plane, updated by GUI
    sequence = ['blue', 'green', 'red'] #This will have same size for all nodes
    def __init__(self, name, number_of_nodes):
        self.number_of_nodes = number_of_nodes

    def set_number_of_nodes(self, number_of_nodes):
        self.number_of_nodes = number_of_nodes
        ##once called, invoke game logic to change number of corners

    def set_nodes_centers(self, nodes_centers):
        self.nodes_centers = nodes_centers
        ##once called, invoke game logic to compare distances

    def set_all_scores(self, all_scores):
        self.all_scores = all_scores
        ##once called, invoke game logic to decide rank
    def set_play(self, play):
        self.play = play
        ##once called, invoke game logic to start game
    def set_end(self, end):
        self.end = end
        ##once called, invoke game logic to end game
    def set_score(self, score):
        self.score = score

    def set_node_center(self, node_center):
        self.node_center = node_center

    def set_sequence(self):
        pass











