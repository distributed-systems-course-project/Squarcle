import tkinter as tk
from tkinter import *
from GUI import Main_Game
from ComOrchestrator import ComOrchestrator
import threading
class Wait_admin(object):
    s_data = 0
    x = 0
    var_2 = 0
    def __init__(self, s_data):
        # number of nodes

        # number of nodes variable
        self.s_data = s_data

        def refresh_number():
            orchestrator_obj = ComOrchestrator(self.s_data)
            com_thread = threading.Thread()

            # This node is a master
            com_thread = threading.Thread(name='Com_thread', target=orchestrator_obj.master_starter)
            #self.s_data.com_thread.join()
            com_thread.start()
            com_thread.join()
            self.label_2 = Label(root_2, relief="solid", font="Times 14 bold ", textvariable=self.var_2)
            self.label_2.pack()
            self.label_2.place(bordermode=OUTSIDE, height=50, width=50, x=300, y=300)
            self.s_data.acquire()
            self.var_2 = StringVar()
            print(self.s_data.nodes_to_admin)
            self.var_2.set(len(self.s_data.nodes_to_admin))
            self.s_data.release()

        def close_window():
            orchestrator_obj = ComOrchestrator(self.s_data)
            com_thread = threading.Thread(name='Com_game_start', target=orchestrator_obj.game_starter, args=(True,))
            com_thread.start()
            root_2.destroy()
            maingui = Main_Game(self.s_data, True)

        root_2 =Tk()

        root_2.geometry('800x600')

        self.Wait_label=Label(root_2,text="Wait Please",relief="solid",font="Times 20 bold " ,width=15,height=4,anchor=N)
        self.Wait_label.pack()
        
        self.button = Button (root_2, text = "Start",height=5,width=25, command = close_window)
        self.button.pack()

        self.ref = Button(root_2, text="Refresh", height=5, width=25, command=refresh_number)
        self.ref.pack()
        self.s_data.acquire()
        name = self.s_data.node_ID
        self.s_data.release()
        self.node_label=Label(root_2,text="Your ID is: " + str(name)+"\nPlease share your ID with your friends to enjoy the game!",relief="solid",font="Times 14 bold ")
        self.node_label.pack()
        self.node_label.place(bordermode=OUTSIDE, height=80, width=500,x=150,y=400)
        
        


        root_2.mainloop()
