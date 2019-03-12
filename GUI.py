
import tkinter as tk
from tkinter import *

root = Tk()

root.geometry('920x800')
c = Canvas(root,width=800,height=600,bg='black')

def _create_circle(self, x, y, r, color):
    return self.create_oval(x-r, y-r, x+r, y+r, outline=color, fill=color)
tk.Canvas.create_circle = _create_circle

center=[(15,20),(500,500),(300,300)]
colors = ["blue", "red", "white"]




for i in range(len(center)):
    c.create_circle(center[i][0],center[i][1], 5, color=colors[i])


c.pack()
shape=c.create_circle(100,100, 20, color="blue")

def down(zero) :
    dx = 0
    dy = 10
    c.move(shape, dx, dy)



def up(zero) :
    dx = 0
    dy = -10
    c.move(shape, dx, dy)

def right(zero) :
    dx = 10
    dy = 0
    c.move(shape, dx, dy)

def left(zero) :
    dx = -10
    dy = 0
    c.move(shape, dx, dy)





root.bind("s", down)
root.bind("z", up)
root.bind("d", right)
root.bind("q", left)





root.mainloop()
