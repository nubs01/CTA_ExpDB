import tkinter as tk
from tkinter import ttk
import pandas as pd
from cta_db.datastructures import data_print as dp
import tk_widgets as tkw
import datetime as dt

class bottle_test_pane(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        self.data = kwargs.get('data')
        if self.data is not None:
            kwargs.pop('data')
        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.master = master
        self.root = master.root
        self.initUI()

    def initUI(self):
        self.pane = ttk.Frame(self)
        self.pane.pack(fill='both',expand=True)
        if self.data is None:
            return

        tree_frame = ttk.Frame(self.pane)
        self.tree = self.make_tree(tree_frame)
        self.fill_tree(self.tree)

        button_frame = ttk.Frame(self.pane)
        add_button = ttk.Button(button_frame,text='+',width=3,command=self.add_test)
        del_button = ttk.Button(button_frame,text='-',width=3,command=self.delete_test)

        del_button.pack(side='right',padx=5,pady=5)
        add_button.pack(side='right',padx=5,pady=5)
        
        tree_frame.grid(row=0,column=0,columnspan=2,sticky='nsew')
        button_frame.grid(row=1,column=1,sticky='e')

    def cstate(self,state,widget=None):
        if widget is None:
            widget = self
        if widget.winfo_children:
            for w in widget.winfo_children():
                try:
                    w.state((state,))
                except:
                    pass
                self.cstate(state,widget=w)

    def enable_all(self):
        self.master.enable()
        self.cstate('!disabled')

    def disable_all(self):
        self.master.disable()
        self.cstate('disabled')

    def set_data(self,data):
        self.pane.destroy()
        self.data = data
        self.initUI()

    def add_test(self):
        new_test = dict.fromkeys(['Date/Time',*self.data.columns])
        today = dt.datetime.combine(dt.datetime.today().date(),dt.time(20,00))
        new_test['Date/Time'] = dp.get_date_str(today,'%m/%d/%y %H:%M')
        popup = tkw.fill_dict_popup(self.root,new_test)
        self.disable_all()
        self.root.wait_window(popup.top)
        self.enable_all()
        types = self.data.dtypes
        date_str = new_test.pop('Date/Time')
        date_obj = dp.get_datetime_from_str(date_str,accepted_formats=['%m/%d/%y %H:%M'])
        if date_obj is None:
            return
        for k,v in new_test.items():
            if types[k]==int:
                try:
                    new_test[k] = int(v)
                except ValueError:
                    new_test[k] = None
            elif types[k]==float:
                try:
                    new_test[k] = round(float(v),2)
                except ValueError:
                    new_test[k] = None
        if any([x is None or x=='' for x in new_test.values()]):
            return
        df = pd.DataFrame(new_test,index=[date_obj])
        self.data = self.data.append(df)
        self.master.set_bottle_tests(self.data)
        row = df.iloc[0].tolist()
        self.tree.insert('','end',text=str(self.data.shape[0]-1),
                        values=[date_str,*row])
        self.master.saved=False


    def delete_test(self):
        self.master.saved = False
        try:
            item = self.tree.selection()[0]
        except IndexError:
            return

        date_str = self.tree.item(item,'values')[0]
        index = dp.get_datetime_from_str(date_str)
        self.data = self.data.drop(index)
        self.tree.delete(item)
        children = self.tree.get_children()
        for n,x in enumerate(children,start=0):
            self.tree.item(x,text=str(n))
        self.master.set_bottle_tests(self.data)
        self.master.saved = False

    def make_tree(self,frame):
        cols = list(self.data.keys())
        cols.insert(0,'Date/Time')
        tree = ttk.Treeview(frame,height=5,column=cols)
        sbar = ttk.Scrollbar(frame,orient='vertical',command=tree.yview)
        tree.config(yscrollcommand=sbar.set)
        tree.column('#0',anchor='center',width=40)
        tree.heading('#0',text='Idx')
        types = self.data.dtypes.tolist()
        if self.data.empty:
            types = [str,int,float,float,float]
        types.insert(0,str)
        for t,c in zip(types,cols):
            if t==float:
                col_width = 90
            else:
                col_width=115
            tree.column(c,anchor='center',width=col_width)
            tree.heading(c,text=c)
        tree.pack(side='left',fill='x')
        sbar.pack(side='left',fill='y')
        return tree

    def fill_tree(self,tree):
        for n, row in enumerate(self.data.iterrows(),start=0):
            tmp = [round(x,2) if isinstance(x,float) else x for x in row[1]]
            tmp_id = tree.insert('','end',text=str(n), 
                                values=[dp.get_date_str(row[0],fmt='%m/%d/%y %H:%M'),*tmp])

    def clear_tree(self):
        for x in self.tree.children():
            self.tree.delete(x)


