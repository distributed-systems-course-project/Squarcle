
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

x=100
y=100
c.pack()
shape=c.create_circle(100,100, r=20, color="#f00001")

def down(zero) :
    global x
    global y
    dx = 0
    dy = 10
    c.move(shape, dx, dy)
    x=x
    y=y+10
    print(x)
    print(y)
    return x,y

def up(zero) :
    global x
    global y
    dx = 0
    dy = -10
    c.move(shape, dx, dy)
    x=x
    y=y-10
    print(x)
    print(y)
    return x,y

def right(zero) :
    global x
    global y
    dx = 10
    dy = 0
    c.move(shape, dx, dy)
    x=x+10
    y=y
    print(x)
    print(y)
    return x,y

def left(zero) :
    global x
    global y
    dx = -10
    dy = 0
    c.move(shape, dx, dy)
    x=x-10
    y=y
    print(x)
    print(y)
    return x,y


root.bind("s", down)
root.bind("z", up)
root.bind("d", right)
root.bind("q", left)






root.mainloop()
