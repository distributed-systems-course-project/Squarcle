import threading
import time
import tkinter as tk
from tkinter import *

from squarcle_data import squarcle_data


class Game_Over(object):
    s_data = 0
    def __init__(self, s_data, old_root):

        self.s_data = s_data
        root_3 = Tk()
        root_2 = 0

        root_3.geometry('600x800')

        self.over_label=Label(root_3,text="Mission accomplished !",relief="solid",font="Times 22 bold " ,width=200,height=4,anchor=CENTER)
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
        scores = self.s_data.all_scores
        current_node_score = self.s_data.score
        current_node_name = self.s_data.name
        self.s_data.release()



        ## Score list
        scoreGUIList = Listbox(root_3)
        scoreGUIList.place(x=100, y=200)

        scoreGUIList.insert(1, str(current_node_name) + " => " + str(current_node_score))
        for i in range(0, len(scores)):
            scoreGUIList.insert(i+2, str(scores[i][0]) + " => " + str(scores[i][1]))

        scoreGUIList.pack()
        scoreGUIList.place(bordermode=OUTSIDE, x=200, y=400)

        def update():

            self.s_data.acquire()
            scores = self.s_data.all_scores
            current_node_score = self.s_data.score
            current_node_name = self.s_data.name
            self.s_data.release()
            scoreGUIList.delete(0, len(scores) + 1)
            scoreGUIList.insert(1, str(current_node_name) + " => " + str(current_node_score))
            for i in range(0, len(scores)):
                scoreGUIList.insert(i + 2, str(scores[i][0]) + " => " + str(scores[i][1]))
            scoreGUIList.after(1000, update)

        scoreGUIList.after(1000, update)

        root_3.mainloop()





if __name__ == "__main__":
    import sys
    s_data = squarcle_data()
    gameover = Game_Over(s_data)