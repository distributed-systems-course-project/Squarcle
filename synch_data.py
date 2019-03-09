class synch_data:
    game_logic_to_gui = False #set when game logic updates score, time, result, collision, end, sequance
    gui_to_game_logic = False #set when gui changes value of center
    communication_to_game_logic = False #set when changing play, end, number of nodes, centers of all nodes
    game_logic_to_communication = False #set when changing centers, end,
    gui_to_communication = False #nothing I guess, you can add though
    communication_to_gui = False #nothing, you can add more
