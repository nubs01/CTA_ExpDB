import tkinter as tk
from tkinter import ttk
from cta_db.datastructures.data_print import *
import tk_widgets as tkw

class pre_op_pane(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        if kwargs.get('data') is not None:
            self.data = kwargs.pop('data')
        else:
            self.data = None

        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.master = master

        self.initUI()

    def initUI(self):


        # Make Variables
        self.date_var = tk.StringVar()
        self.date_var.set('mm/dd/yy HH:MM')
        self.event_var = tk.StringVar()
        self.event_var.set('')
        self.comment_var = tk.StringVar()
        self.comment_var.set('')

        # Make Labels
        event_label = ttk.Label(self,text='Event')
        date_label = ttk.Label(self,text='Date')
        comment_label = ttk.Label(self,text='Comments')

        # Make Buttons
        add_button = ttk.Button(self,text='Add',command=self.add_preop)
        delete_button = ttk.Button(self,text='Delete',command=self.delete_preop)

        # Make entries
        date_entry = tkw.date_entry(self,textvariable=self.date_var,
                                    nullstr='mm/dd/yy HH:MM',
                                    accepted_formats=['%m/%d/%y %H:%M'],
                                    outfmt='%m/%d/%y %H:%M')
        event_entry = ttk.Entry(self,textvariable=self.event_var)
        comment_entry = ttk.Entry(self,textvariable=self.comment_var)

        # Make Tree
        self.tree = ttk.Treeview(self,height=5)
        sbar = ttk.Scrollbar(self,orient='vertical',command=self.tree.yview)
        self.tree.config(yscrollcommand=sbar.set)
        self.tree['columns'] = ('Date','Event','Comments')
        self.tree.column('#0',anchor='center',width=50)
        self.tree.heading('#0',text='Idx')
        self.tree.column('Date',anchor='center')
        self.tree.heading('Date',text='Date')
        self.tree.column('Event',anchor='center',width=50)
        self.tree.heading('Event',text='Event')
        self.tree.column('Comments',anchor='center',width=50)
        self.tree.heading('Comments',text='Comments')

        self.set_data()

    def add_preop(self):
        pass

    def delete_preop(self):
        pass

    def set_data(self,data=None):
        if data is not None:
            self.data=data
        else:
            data = self.data

        if data is None:
            return

        x = 0
        for row in data.iterrows():
            tmp_id = self.tree.insert('','end',text=str(x))
            self.tree.set(tmp_id,values=(get_date_str(row[0]),row[1],row[2]))

