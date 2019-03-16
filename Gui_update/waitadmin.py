import tkinter as tk
from tkinter import *
from GUI import Main_Game

class Wait_admin(object):
    s_data = 0
    def __init__(self, s_data):
        self.s_data = s_data
        def close_window():
        	root_2.destroy()
        	maingui=Main_Game()

        root_2 =Tk()

        root_2.geometry('600x600')

        self.Wait_label=Label(root_2,text="Wait Please",relief="solid",font="Times 20 bold " ,width=15,height=4,anchor=N)
        self.Wait_label.pack()
        
        self.button = Button (root_2, text = "Start",height=10,width=25, command = close_window)
        self.button.pack()
        self.node_label=Label(root_2,text="Joined Nodes:",relief="solid",font="Times 14 bold ")
        self.node_label.pack()
        self.node_label.place(bordermode=OUTSIDE, height=50, width=150,x=100,y=300)
        
        
        #number of nodes
        self.var_2=StringVar()       
        self.label_2=Label(root_2,relief="solid",font="Times 14 bold ",textvariable=self.var_2,)
        self.label_2.pack()
        self.label_2.place(bordermode=OUTSIDE, height=50, width=50,x=300,y=300)
        #number of nodes variable
        self.s_data.acquire()
        self.var_2.set(len(self.s_data.nodes_to_admin))
        self.s_data.release()
        root_2.mainloop()
