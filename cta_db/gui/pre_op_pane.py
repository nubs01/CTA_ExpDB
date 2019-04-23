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
        self.pane = ttk.Frame(self)
        self.pane.pack(side='left',anchor='nw',fill='both',expand=True)
        
        if self.data is None:
            return
        # Make Variables
        self.date_var = tk.StringVar()
        self.date_var.set('mm/dd/yy HH:MM')
        self.event_var = tk.StringVar()
        self.event_var.set('')
        self.comment_var = tk.StringVar()
        self.comment_var.set('')

        # Make Labels
        event_label = ttk.Label(self.pane,text='Event:  ')
        date_label = ttk.Label(self.pane,text='Date:  ')
        comment_label = ttk.Label(self.pane,text='Comments:  ')

        # Make Buttons
        add_button = ttk.Button(self.pane,text='Add',command=self.add_preop)
        delete_button = ttk.Button(self.pane,text='Delete',command=self.delete_preop)

        # Make entries
        self.date_entry = tkw.date_entry(self.pane,textvariable=self.date_var,
                                    nullstr='mm/dd/yy HH:MM',
                                    accepted_formats=['%m/%d/%y %H:%M'],
                                    outfmt='%m/%d/%y %H:%M')
        event_entry = ttk.Entry(self.pane,textvariable=self.event_var)
        comment_entry = ttk.Entry(self.pane,textvariable=self.comment_var)

        # Make Tree
        self.make_tree()

        date_label.grid(row=0,column=0,sticky='w')
        self.date_entry.grid(row=0,column=1,sticky='w')
        event_label.grid(row=0,column=2,sticky='e')
        event_entry.grid(row=0,column=3)
        comment_label.grid(row=1,column=0,sticky='w')
        comment_entry.grid(row=1,column=1,columnspan=3,sticky='ew')
        add_button.grid(row=1,column=4,sticky='e')
        delete_button.grid(row=5,column=4,sticky='e')
        #self.pane.grid_columnconfigure(2,weight=1,pad=15)
        self.pane.grid_rowconfigure(0,pad=5)
        self.pane.grid_rowconfigure(1,pad=5)
        self.pane.grid_rowconfigure(2,pad=5)
        self.pane.grid_rowconfigure(3,pad=5)
        self.pane.grid_rowconfigure(4,pad=5)

    def add_preop(self):
        date = get_datetime_from_str(self.date_var.get())
        event = self.event_var.get()
        comment = self.comment_var.get()
        if date is None or event=='':
            return
        self.data = self.master.add_pre_op(date,event,comment)
        self.make_tree()
        self.date_entry.set('')
        self.event_var.set('')
        self.comment_var.set('')

    def delete_preop(self):
        self.master.saved = False
        try:
            item = self.tree.selection()[0]
        except IndexError:
            return

        date_str = self.tree.item(item,'values')[0]
        index = get_datetime_from_str(date_str)
        self.data = self.data.drop(index)
        self.tree.delete(item)
        children = self.tree.get_children()
        n=0
        for x in children:
            self.tree.item(x,text=str(n))
            n+=1
        self.master.set_pre_op(self.data)

    def set_data(self,data):
        self.pane.destroy()
        self.data = data
        self.initUI()

    def make_tree(self):
        if hasattr(self,'tree_frame'):
            self.tree_frame.destroy()

        tree_frame = ttk.Frame(self.pane)
        self.tree = ttk.Treeview(tree_frame,height=5,column=['Date','Event','Comments'])
        sbar = ttk.Scrollbar(tree_frame,orient='vertical',command=self.tree.yview)
        self.tree.config(yscrollcommand=sbar.set)
        self.tree.column('#0',anchor='center',width=40)
        self.tree.heading('#0',text='Idx')
        self.tree.column('Date',anchor='center',width=170)
        self.tree.heading('Date',text='Date/Time')
        self.tree.column('Event',anchor='center',width=170)
        self.tree.heading('Event',text='Event')
        self.tree.column('Comments',anchor='center',width=180)
        self.tree.heading('Comments',text='Comments')
        self.tree.grid(row=0,column=0,columnspan=5,rowspan=3,sticky='ew')
        sbar.grid(row=0,column=6,rowspan=3,sticky='ns')
        tree_frame.grid(row=2,column=0,rowspan=3,columnspan=6,sticky='ew')

        data = self.data
        x = 0
        for row in data.iterrows():
            tmp_id = self.tree.insert('','end',text=str(x),
                                    values=[get_date_str(row[0],fmt='%m/%d/%y %H:%M'),
                                            row[1]['Pre-op'],row[1]['Comments']])
            x+=1

