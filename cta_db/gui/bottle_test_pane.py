import tkinter as tk
from tkinter import ttk
import pandas as pd

class bottle_test_pane(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        self.data = kwargs.get('data')
        if self.data is not None:
            kwargs.pop('data')
        ttk.Frame().__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.master = master
        self.root = master.root
        self.initUI()

    def initUI(self):
        self.pane = ttk.Frame(self)
        self.pane.pack(fill='both',expand=True)
        if self.data is None:
            return

        self.make_tree(self.pane)


    def enable_all(self):
        pass

    def disable_all(self):
        pass

    def set_data(self):
        pass

    def add_test(self):
        pass

    def delete_test(self):
        pass

    def make_tree(self,frame):
        pass

    def fill_tree(self):
        pass

    def clear_tree(self):
        pass

