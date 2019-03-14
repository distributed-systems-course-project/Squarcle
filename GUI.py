
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
        




        c = Canvas(root,width=800,height=600,bg='black')

        
        tk.Canvas.create_circle = _create_circle

        center=self.s_data.corners_and_colours_pairs[0]

        colors = self.s_data.corners_and_colours_pairs[1]




        for i in range(len(center)):
            c.create_circle(center[i][0],center[i][1], 5, color=colors[i])
        #flff
        self.x=100
        self.y=100
        c.pack()
        shape=c.create_circle(100,100, r=20, color="#f00001")

        def down(zero) :
            #global x
            #global y
            dx = 0
            dy = 10
            c.move(shape, dx, dy)
            self.x=self.x
            self.y=self.y+10
            self.s_data.set_node_center([self.x, self.y])
            # score variable
            self.var_1.set(self.s_data.score)

        def up(zero) :
            
            dx = 0
            dy = -10
            c.move(shape, dx, dy)
            self.x=self.x
            self.y=self.y-10
            self.s_data.set_node_center([self.x, self.y])
            # score variable
            self.var_1.set(self.s_data.score)
        def right(zero) :
            
            dx = 10
            dy = 0
            c.move(shape, dx, dy)
            self.x=self.x+10
            self.y=self.y
            self.s_data.set_node_center([self.x, self.y])
            # score variable
            self.var_1.set(self.s_data.score)

        def left(zero) :
            global x
            global y
            dx = -10
            dy = 0
            c.move(shape, dx, dy)
            self.x=self.x-10
            self.y=self.y
            self.s_data.set_node_center([self.x, self.y])
            # score variable
            self.var_1.set(self.s_data.score)

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
