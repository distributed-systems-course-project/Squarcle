import tkinter as tk
from tkinter import *

from squarcle_data import squarcle_data


class Game_Over(object):
    s_data = 0
    def __init__(self, s_data):
        self.s_data = s_data
        root_3 = Tk()
        root_2 = 0

        root_3.geometry('600x600')

        self.over_label=Label(root_3,text="Game Over",relief="solid",font="Times 32 bold " ,width=15,height=4,anchor=CENTER)
        self.over_label.pack()
        self.ranking_label=Label(root_2,text="Your Ranking is:",relief="solid",font="Times 14 bold ")
        self.ranking_label.pack()
        self.ranking_label.place(bordermode=OUTSIDE, height=50, width=170,x=100,y=300)


        self.var_1=StringVar()       
        self.ranking_var=Label(root_2,relief="solid",font="Times 14 bold ",textvariable=self.var_1)
        self.ranking_var.pack()
        self.ranking_var.place(bordermode=OUTSIDE, height=50, width=50,x=350,y=300)
        #number of nodes variable
        self.s_data.acquire()
        self.var_1.set(self.s_data.node_index)
        self.s_data.release()
        root_3.mainloop()




if __name__ == "__main__":
    import sys
    s_data = squarcle_data()
    gameover = Game_Over(s_data)