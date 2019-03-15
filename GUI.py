
import tkinter as tk
from tkinter import *

    

class Main_Game(object):
    s_data = 0
    def __init__(self, s_data):
        self.s_data = s_data
        #remove later
        self.s_data.set_play(True)
        

        def _create_circle(self, x, y, r, color):
            return self.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)
            


        root = Tk()

        root.geometry('920x800')
        




        c = Canvas(root,width=s_data.MAX_X,height=s_data.MAX_Y,bg='black')

        
        tk.Canvas.create_circle = _create_circle

        center=self.s_data.corners_and_colours_pairs[0]

        colors = self.s_data.corners_and_colours_pairs[1]




        for i in range(len(center)):
            c.create_circle(center[i][0],center[i][1], 16, color=colors[i])
        #flff
        self.x=center[0][0]
        self.y=center[0][1]
        c.pack()
        shape=c.create_circle(center[0][0],center[0][1], r=15, color="#f00001")
        c.create_circle(750, 550, 50, color=colors[self.s_data.color_counter])

        def down(zero) :
            self.s_data.acquire()
            if self.s_data.end:
                return 10
                #put transition to final window
            self.s_data.release()
            c.create_circle(750, 550, 50, color= colors[self.s_data.color_counter])
            #global x
            #global y
            dx = 0
            dy = 10
            if (self.y + dy) < s_data.MAX_Y :
                c.move(shape, dx, dy)
                self.x=self.x
                self.y=self.y+ dy
                self.s_data.acquire()
                self.s_data.set_node_center([self.x, self.y])
                # score variable
                self.var_1.set(self.s_data.score)
                self.s_data.release()

        def up(zero) :
            self.s_data.acquire()
            if self.s_data.end:
                return 10
                #put transition to final window
            self.s_data.release()
            c.create_circle(750, 550, 50, color= colors[self.s_data.color_counter])
            dx = 0
            dy = -10
            if self.y + dy > 0 :
                c.move(shape, dx, dy)
                self.x=self.x
                self.y=self.y+dy
                self.s_data.acquire()
                self.s_data.set_node_center([self.x, self.y])
                 # score variable
                self.var_1.set(self.s_data.score)
                self.s_data.release()

        def right(zero) :
            self.s_data.acquire()
            if self.s_data.end:
                return 10
                #put transition to final window
            self.s_data.release()
            c.create_circle(750, 550, 50, color= colors[self.s_data.color_counter])

            dx = 10
            dy = 0
            if (self.x + dx) < s_data.MAX_X :
                c.move(shape, dx, dy)
                self.x=self.x+dx
                self.y=self.y
                self.s_data.acquire()
                self.s_data.set_node_center([self.x, self.y])
                   # score variable
                self.var_1.set(self.s_data.score)
                self.s_data.release()

        def left(zero) :
            self.s_data.acquire()
            if self.s_data.end:
                return 10
                #put transition to final window
            self.s_data.release()
            c.create_circle(750, 550, 50, color=colors[self.s_data.color_counter])

            global x
            global y
            dx = -10
            dy = 0
            if self.x + dx > 0 :
                c.move(shape, dx, dy)
                self.x=self.x+dx
                self.y=self.y
                self.s_data.acquire()
                self.s_data.set_node_center([self.x, self.y])
                # score variable
                self.var_1.set(self.s_data.score)
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


        #color label
        self.color_label=Label(root,text="Move to:",relief="solid",font="Times 14 bold ")
        
        self.var_2=StringVar()       
        self.label_2=Label(root,relief="solid",font="Times 14 bold ",textvariable=self.var_2,)
        
        self.color_label.pack()
        self.label_2.pack()
        
        self.color_label.place(bordermode=OUTSIDE, height=40, width=100,x=670,y=625)
        self.label_2.place(bordermode=OUTSIDE, height=50, width=50,x=800,y=620)
        
        #color variable 
        self.var_2.set(self.y)






        root.mainloop()
