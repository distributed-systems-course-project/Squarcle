import tkinter as tk
from tkinter import *
from GUI import Main_Game

class Wait_member(object):
    def __init__(self):

	    root_1 = Tk()

	    root_1.geometry('400x400')

	    self.Wait_label=Label(root_1,text="Wait Please",relief="solid",font="Times 32 bold " ,width=15,height=4,anchor=CENTER)
	    self.Wait_label.pack()
	    if(1):
	        root_1.destroy()
	        maingui=Main_Game()


	    root_1.mainloop()


