from cta_db.gui import surgery_pane, info_pane
from tkinter import ttk
from cta_db import dbio
import cta_db.datastructures as cta
import tkinter as tk
from cta_db.gui import animal_list_pane


class controller(ttk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super(controller,self).__init__(parent)
        self.parent=parent

    def add_animal(self):
        print('Add animal')

    def delete_animal(self,animal):
        print('deleting '+animal)

    def anim_select(self,event):
        print('Selecting Animal')

    def save(self):
        print('save')

    def close(self):
        self.parent.destroy()



if __name__=='__main__':
    anim_dat = dbio.load_anim_data('RN5')
    root = tk.Tk()
    root.geometry('800x400')
    pane = controller(root)
    listbox = animal_list_pane.animal_list_pane(controller,root,animal_list=['RN5','RN6'])
    listbox.pack(side='left')
    pane2 = info_pane.anim_info_pane(pane,root,data=anim_dat)
    pane2.pack(side='right')
    pane.pack()
    root.mainloop()

