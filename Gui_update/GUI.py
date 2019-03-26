import time
import tkinter as tk
from tkinter import *
from Gameover import Game_Over
from squarcle_data import  squarcle_data
    

class Main_Game(object):
    s_data = squarcle_data()
    master = False
    def __init__(self, s_data, master):
        self.s_data = s_data
        self.master = master

        def _create_circle(self, x, y, r, color):
            return self.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)
            


        root = Tk()

        root.geometry('920x800')
        




        c = Canvas(root,width=800,height=600,bg='black')
        b=  Canvas(root,width=70,height=70,bg='black')

        xx = False
        print("mazal majit")
        while not xx:
            self.s_data.acquire()
            print("acquired")
            xx = self.s_data.play_from_com
            self.s_data.release()
            print("still waiting")
            time.sleep(1)
        print("yaw khrajt")

        self.s_data.acquire()
        self.s_data.set_play(True)
        self.s_data.MAX_X = 800
        self.s_data.MAX_Y = 600
        center = self.s_data.corners_and_colours_pairs[0]
        colors = self.s_data.corners_and_colours_pairs[1]
        n_color = self.s_data.next_color_corner_pair[1]
        self.s_data.release()

        tk.Canvas.create_circle = _create_circle
        b.create_oval(10, 10, 60, 60, fill=n_color)

        for i in range(len(center)):
            c.create_circle(center[i][0], center[i][1], 18, color=colors[i])
            # flff
        self.x = center[0][0]
        self.y = center[0][1]

        c.pack()
        b.pack()
        shape=c.create_circle(self.x,self.y, r=16, color="#f00001")

        def down(zero):
            dx = 0
            dy = 10
            if self.y + dy < self.s_data.MAX_Y:
                c.move(shape, dx, dy)
                self.x = self.x
                self.y = self.y + dy
                self.s_data.acquire()
                self.s_data.set_node_center([self.x, self.y])
                self.var_1.set(self.s_data.score)
                self.s_data.release()
                b.create_oval(10, 10, 60, 60, fill=self.s_data.next_color_corner_pair[1])
            self.s_data.acquire()
            if self.s_data.end:
                self.s_data.release()
                root.destroy()
                gameover = Game_Over(self.s_data)
            self.s_data.release()

        def up(zero):

            dx = 0
            dy = -10
            if self.y + dy > 0:
                c.move(shape, dx, dy)
                self.x = self.x
                self.y = self.y + dy
                self.s_data.acquire()
                self.s_data.set_node_center([self.x, self.y])
                self.var_1.set(self.s_data.score)
                self.s_data.release()
                b.create_oval(10, 10, 60, 60, fill=self.s_data.next_color_corner_pair[1])
            self.s_data.acquire()
            if self.s_data.end:
                self.s_data.release()
                root.destroy()
                gameover = Game_Over(self.s_data)
            self.s_data.release()

        def right(zero):

            dx = 10
            dy = 0
            if self.x + dx < self.s_data.MAX_X:
                c.move(shape, dx, dy)
                self.x = self.x + dx
                self.y = self.y
                self.s_data.acquire()
                self.s_data.set_node_center([self.x, self.y])
                self.s_data.release()
                b.create_oval(10, 10, 60, 60, fill=self.s_data.next_color_corner_pair[1])
            self.s_data.acquire()
            if self.s_data.end:
                self.s_data.release()
                root.destroy()
                gameover = Game_Over(self.s_data)
            self.s_data.release()

        def left(zero):
            global x
            global y
            dx = -10
            dy = 0
            if self.x + dx > 0:
                c.move(shape, dx, dy)
                self.x = self.x + dx
                self.y = self.y
                self.s_data.acquire()
                self.s_data.set_node_center([self.x, self.y])
                self.var_1.set(self.s_data.score)
                self.s_data.release()
                b.create_oval(10, 10, 60, 60, fill=self.s_data.next_color_corner_pair[1])
            self.s_data.acquire()
            if self.s_data.end:
                self.s_data.release()
                root.destroy()
                gameover = Game_Over(self.s_data)
            self.s_data.release()

        root.bind("s", down)
        root.bind("z", up)
        root.bind("d", right)
        root.bind("q", left)
        #score label
        self.score_label=Label(root,text="Score:",relief="solid",font="Times 14 bold ")
        
        self.var_1=StringVar()       
        self.label_1=Label(root,relief="solid",font="Times 14 bold ",textvariable=self.var_1,)
        
        self.score_label.pack()
        self.label_1.pack()
        
        self.score_label.place(bordermode=OUTSIDE, height=40, width=60,x=50,y=625)
        self.label_1.place(bordermode=OUTSIDE, height=50, width=50,x=140,y=620)
        #score variable
        self.var_1.set(0)

        #color label
        self.color_label=Label(root,text="Move to:",relief="solid",font="Times 14 bold ")
        
        
        
        self.color_label.pack()
        
        
        self.color_label.place(bordermode=OUTSIDE, height=40, width=100,x=300,y=625)
       
        
        #color variable 
       






        root.mainloop()
