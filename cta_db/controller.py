import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from cta_db import gui, dbio, datastructures as ds
import os

class controller(ttk.Frame):

    def __init__(self,parent,*args,**kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.root = parent
        self.anim_db = dbio.load_anim_db()
        self.anim_index=0
        self.saved = True
        self.anim_dat = None
        self.anim_file = None
        self.initUI()

    def initUI(self):

        self.pack(fill='both',expand=True)

        # add list box frame
        self.list_pane = gui.animal_list_pane(self,self.root)
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

        # Bottle Test Pane
        self.bottle_test_pane = gui.bottle_test_pane(self.nb,self,width=300,height=200)
        self.nb.add(self.bottle_test_pane,text='Bottle Tests')

        self.nb.select(self.anim_pane)
        self.nb.enable_traversal()
        self.nb.pack(side='right',fill='both',expand=True)

    def close(self):
        self.parent.destroy()

    def save(self):
        animID = self.anim_dat.ID

        if self.anim_file is None:
            file_dir = filedialog.askdirectory(title='Choose save directory for %s' % animID)
            self.anim_file = os.path.join(file_dir,animID+'_metadata.p')
        dbio.save_anim_data(animID,self.anim_dat,self.anim_file)
        self.list_pane.re_anchor()
        txt_file = sel.anim_file.replace('.p','.txt')
        with open(txt_file, 'w') as f:
            print(self.anim_dat, file=f)

        self.saved=True

    def disable(self):
        '''
        Disable all children to prevent clicking on things
        '''
        # disable other notebook tabs
        tab_id = self.nb.index(self.nb.select())
        curFrame = self.nb.winfo_children()[tab_id]
        for t in self.nb.tabs():
            if self.nb.index(t) is not tab_id:
                self.nb.tab(t,state='disable')

        self.list_pane.cstate('disabled')

    def enable(self):
        '''
        Enable all children to allow clicking on things
        '''
        # disable other notebook tabs
        tab_id = self.nb.index(self.nb.select())
        curFrame = self.nb.winfo_children()[tab_id]
        for t in self.nb.tabs():
            self.nb.tab(t,state='normal')

        self.list_pane.cstate('normal')

    def add_pre_op(self,date,event,comment):
        self.anim_dat.add_pre_op(event,comment,date=date)
        return self.anim_dat.pre_op

    def set_pre_op(self,preop):
        self.anim_dat.set_pre_op(preop)

    def set_bottle_tests(self,bottle_tests):
        self.anim_dat.set_bottle_tests(bottle_tests)

    def anim_select(self,event):
        w = event.widget
        selection = w.curselection()
        if selection == ():
            return
        idx = int(selection[0])
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
                w.selection_set(self.anim_index)
                w.selection_anchor(self.anim_index)
                w.focus()
                return
        dat,fn = dbio.load_anim_data(animID)
        self.set_data(dat,idx=idx,fn=fn)
        self.saved = True

    def add_animal(self):
        animID = simpledialog.askstring('New Animal','Animal ID?',parent=self.root)
        if animID is None or animID=='':
            return
        anim_dat = ds.animal(animID)
        idx = self.list_pane.add_animal(animID)
        self.set_data(anim_dat,idx=idx)
        self.saved=False
        print('Add Animal')

    def delete_animal(self):
        idx = self.anim_index
        if idx is None:
            return
        animID = self.anim_dat.ID
        q = messagebox.askyesno('Remove Animal','Remove %s from database? ' % animID)
        if not q:
            return
        dbio.delete_animal_from_db(animID)
        self.list_pane.remove_animal(idx)
        self.set_data(None)
        print('Delete Animal')

    def set_data(self,anim_dat,idx=None,fn=None):
        self.anim_index = idx
        self.anim_dat = anim_dat
        self.anim_file = fn
        if anim_dat is None:
            self.surgery_pane.set_data(None)
            self.anim_pane.set_data(None)
            self.pre_pane.set_data(None)
            self.ioc_test_pane.set_data(None)
            self.bottle_test_pane.set_data(None)
            return
        self.surgery_pane.set_data(anim_dat.surgery)
        self.anim_pane.set_data(anim_dat)
        self.pre_pane.set_data(anim_dat.pre_op)
        self.ioc_test_pane.set_data(anim_dat.ioc_tests)
        self.bottle_test_pane.set_data(anim_dat.bottle_tests)

if __name__=="__main__":
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.theme_use('clam')
    root.geometry('900x600')
    controller(root).pack(side='right',fill='both',expand=True)
    root.mainloop()
