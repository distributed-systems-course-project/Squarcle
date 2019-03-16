import tkinter as tk
from tkinter import *
from GUI import Main_Game
from squarcle_data import  squarcle_data

class Wait_member(object):
	s_data = 0
	def __init__(self, s_data):
		self.s_data = s_data
		root_1 = Tk()
		root_1.geometry('400x400')
		print("I am here")
		self.Wait_label=Label(root_1,text="Wait Please",relief="solid",font="Times 32 bold " ,width=15,height=4,anchor=CENTER)
		self.Wait_label.pack()
		if(False):
			root_1.destroy()
			maingui=Main_Game()
		root_1.mainloop()


