import tkinter as tk
from tkinter import ttk
from copy import deepcopy
from cta_db import dbio
import platform

class animal_list_pane(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        if kwargs.get('animal_list') != None:
            self.animal_list = deepcopy(kwargs.pop('animal_list'))
            self.animal_list.sort()
        else:
            anim_db = dbio.load_anim_db()
            node = platform.node()
            if anim_db.get(node) is None:
                anim_db[node] = {}
                dbio.save_anim_db(anim_db)
            self.animal_list = list(anim_db[node].keys())
            self.animal_list.sort()
        ttk.Frame.__init__(self,parent,width=20,*args,**kwargs)
        self.parent = parent
        self.initUI()

    def initUI(self):
        parent = self.parent
        self.list_frame = ttk.Frame(self)
        self.yscroll = ttk.Scrollbar(self.list_frame,orient='vertical')
        self.list_box = tk.Listbox(self.list_frame,exportselection=False,
                                    selectmode='single',width=15,
                                    yscrollcommand=self.yscroll.set)
        self.list_box.bind("<<ListboxSelect>>",parent.anim_select)
        self.yscroll.config(command=self.list_box.yview)
        self.list_box.pack(side='left',fill='both',expand=True)
        self.yscroll.pack(side='left',fill='y')
        self.list_frame.pack(side='top',fill='both',expand=True)

        self.button_frame = ttk.Frame(self)
        self.add_button = ttk.Button(self.button_frame,text='+',
                                    command=parent.add_animal,width=3)
        self.del_button = ttk.Button(self.button_frame,text='-',width=3,
                                    command=parent.delete_animal)
        self.save_button = ttk.Button(self.button_frame,text='Save',
                                    command=parent.save,width=5)
        self.close_button = ttk.Button(self.button_frame,text='Close',
                                    command=parent.close,width=5)
        self.add_button.pack(side='left',padx=1,pady=1)
        self.del_button.pack(side='left',padx=1,pady=1)
        self.save_button.pack(side='left',padx=1,pady=1)
        self.close_button.pack(side='left',padx=1,pady=1)
        self.button_frame.pack(side='bottom',fill='x')

        # add animals to list
        for anim in self.animal_list:
            self.list_box.insert('end',anim)


    def cstate(self,state):
        buttons = self.button_frame.winfo_children()
        for b in buttons:
            b.configure(state=state)
        self.list_box.configure(state=state)

    def add_animal(self,animID):
        self.list_box.insert('end',animID)
        idx = self.list_box.index('end')
        self.list_box.selection_clear(0,'end')
        self.list_box.selection_set('end')
        self.list_box.selection_anchor(idx)
        return idx

    def re_anchor(self):
        idx = int(self.list_box.curselection()[0])
        self.list_box.selection_anchor(idx)

    def remove_animal(self,idx):
        self.list_box.delete(idx)
