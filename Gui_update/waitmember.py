import tkinter as tk
from tkinter import *
from Gui_update.GUI import Main_Game
import time
import threading
from squarcle_data import  squarcle_data
from ComOrchestrator import ComOrchestrator

class Wait_member(object):
    s_data = 0
    def __init__(self, s_data):
        self.s_data = s_data
        root_1 = Tk()
        root_1.geometry('400x400')
        orchestrator_obj = ComOrchestrator(self.s_data)
        com_thread = threading.Thread(name='Com_game_start', target=orchestrator_obj.game_starter, args=(False,))
        com_thread.start()
        self.Wait_label=Label(root_1,text="Wait Please",relief="solid",font="Times 32 bold " ,width=15,height=4,anchor=CENTER)
        self.Wait_label.pack()
        wait_thread = threading.Thread(name='wait_game_start', target=self.set_thread, args=(s_data,root_1))
        wait_thread.start()
        root_1.mainloop()

    def set_thread(self, s_data, root_1):
        while True:
            self.s_data.acquire()
            if self.s_data.play_from_com:
                print("ro7 t9awad men hna")
                self.s_data.release()
                maingui = Main_Game(self.s_data, False)
                root_1.destroy()
            else:
                self.s_data.release()
                time.sleep(1)



