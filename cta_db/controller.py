import tkinter as tk
from tkinter import ttk, messagebox
from cta_db import gui, dbio

class controller(ttk.Frame):

    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.anim_db = dbio.load_anim_db()
        self.anim_index=0
        self.saved = True
        self.anim_dat = None
        self.initUI()

    def initUI(self):

        self.pack(fill='both',expand=True)

        # add list box frame
        self.list_pane = gui.animal_list_pane(self,root)
        self.list_pane.pack(side='left',fill='y')

        # Notebook for panes
        self.nb = ttk.Notebook(self)
        
        # Setup animal info pane
        self.anim_pane = gui.anim_info_pane(self.nb,self)
        self.nb.add(self.anim_pane,text='Animal Info')

        # Pre-op Pane
        self.pre_pane = gui.pre_op_pane(self.nb,self,width=300)
        self.nb.add(self.pre_pane,text='Pre-Op')

        # Surgery Pane
        self.surgery_pane = gui.surgery_pane(self.nb,self,width=300,height=200)
        self.nb.add(self.surgery_pane,text='Surgery')

        # IOC Test Pane
        self.ioc_test_pane = gui.ioc_test_pane(self.nb,self,width=100,height=200)
        self.nb.add(self.ioc_test_pane,text='IOC Tests')

        self.nb.select(self.anim_pane)
        self.nb.enable_traversal
        self.nb.pack(side='right',fill='both',expand=True)

    def close(self):
        self.parent.destroy()

    def save(self):
        print(self.anim_dat)

    def add_animal(self):
        print(self.saved)
        print('Add Animal')

    def delete_animal(self):
        print('Delete Animal')

    def add_pre_op(self,date,event,comment):
        self.anim_dat.add_pre_op(event,comment,date=date)
        return self.anim_dat.pre_op

    def set_pre_op(self,preop):
        self.anim_dat.set_pre_op(preop)

    def anim_select(self,event):
        w = event.widget
        selection = w.curselection()
        if selection == ():
            return
        idx = int(selection[0])
        self.anim_index = idx
        animID = w.get(idx)
        if self.anim_dat is not None:
            if animID==self.anim_dat.ID:
                return
        if not self.saved:
            save_q = messagebox.askyesno(title='Unsaved Changes',
                                        message='Are you sure you want to change animals without saving?')
            if not save_q:
                # BUG: Highlight does not change with selection
                w.selection_clear(0,tk.END)
                w.select_set(self.anim_index)
                w.activate(self.anim_index)
                w.focus()
                return
        self.anim_dat = dbio.load_anim_data(animID)
        self.surgery_pane.set_data(self.anim_dat.surgery)
        self.anim_pane.set_data(self.anim_dat)
        self.pre_pane.set_data(self.anim_dat.pre_op)
        self.ioc_test_pane.set_data(self.anim_dat.ioc_tests)
        self.saved = True

if __name__=="__main__":
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.theme_use('clam')
    root.geometry('900x600')
    controller(root).pack(side='right',fill='both',expand=True)
    root.mainloop()
