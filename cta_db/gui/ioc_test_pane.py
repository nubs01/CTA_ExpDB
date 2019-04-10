import tkinter as tk
from tkinter import ttk
from cta_db.datastructures import data_print as dp

class ioc_test_pane(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        self.data = kwargs.get('data')
        if self.data is not None:
            kwargs.pop('data')
        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.master = master

        if self.data is not None:
            self.initUI()
        else:
            self.pane = ttk.Frame()
            self.pane.pack()

    def initUI(self):
        # Add test widgets
        add_frame = ttk.Frame(self)
        add_button = ttk.Button(add_frame,text='Add IOC Test',command=self.add_test)
        self.new_type_var = tk.StringVar()
        type_opts = ioc_test.DEFAULT_MAP.keys()
        self.new_type_var.set(type_opts[0])
        new_type_menu = ttk.OptionMenu(add_frame,self.new_type_var,type_opts[0],*type_opts)
        new_type_menu.grid(row=0,column=0,sitcky='w')
        add_button.grid(row=0,column=1,sticky='e')
        add_frame.pack(side='top',fill='x')

        # Make Scroll frame of ioc_tests
        self.test_segments = []
        self.pane = tkw.scroll_frame(self)
        n=0
        for ioc in self.data:
            tmp = ioc_test_segment(self.scrollpane.viewport,ioc,n)
            self.test_segments.append(tmp)
            tmp.bind("<Button-4>",self.pane._on_mousewheel)
            tmp.bind("<Button-5>",self.pane._on_mousewheel)
            tmp.pack(side='top',fill='x')
            n+=1

    def set_data(self,data):
        map(lamba x: x.destory(),self.test_segments)
        self.data = data
        self.test_segments = []
        n=0
        for ioc in self.data:
            tmp = ioc_test_segment(self.scrollpane.viewport,self,ioc,n)
            self.test_segments.append(tmp)
            tmp.bind("<Button-4>",self.pane._on_mousewheel)
            tmp.bind("<Button-5>",self.pane._on_mousewheel)
            tmp.pack(side='top',fill='x')
            n+=1

class ioc_test_segment(ttk.Frame):
    def __init__(self,parent,master,data,index):
        self.parent = parent
        self.master = master
        self.index = index
        self.data = data
        self.initUI()

    def initUI(self):
        pane = ttk.Frame(self)
        pane.pack()

        # Labels
        type_label = ttk.Label(pane,text='Type:  ')
        date_label = ttk.Label(pane,text='Date:  ')
        weight_label= ttk.Label(pane,text='Weight:  ')
        rec_label = ttk.Label(pane,text='Rec Name:  ')
        toal_label = ttk.Label(pane,text='Total Volume Consumed:  ')
        taste_label = ttk.Label(pane,text='Tastants')

        # TK Vars
        type_var = tk.StringVar()
        date_var = tk.StringVar()
        weight_var = tk.DoubleVar()
        rec_var = tk.StringVar()
        comment_var = tk.StringVar()
        total_var = tk.DoubleVar()
        inj_var = tk.BooleanVar()

        type_var.set(self.data['Test Type'])
        date_var.set(self.data['Test Time'])
        weight_var.set(self.data['Weight'])
        rec_var.set(self.data['Rec Basename'])
        comment_var.set(self.data['Comments'])
        total_var.set(self.data['Total Volume Consumed'])
        if self.data['Injection']['Injection Time'] is None:
            inj_var.set(False)
        else:
            inj_var.set(True)

        type_var.trace('w',lambda n,s,x:self.set_var('Test Type',type_var))
        date_var.trace('w',lambda n,s,x:self.set_var('Test Time',date_var))
        weight_var.trace('w',lambda n,s,x:self.set_var('Weight',weight_var))
        rec_var.trace('w',lambda n,s,x:self.set_var('Rec Basename',rec_var))
        comment_var.trace('w',lambda n,s,x:self.set_var('Comments',comment_var))
        inj_var.trace('w',lambda n,s,x: self.injection_check(inj_var.get()))

        # Entries
        type_entry = ttk.Entry(pane,textvariable=type_var)
        date_entry = tkw.date_entry(pane,textvariable=date_var)
        weight_entry = ttk.Entry(pane,textvariable=weight_var)
        rec_entry = ttk.Entry(pane,textvariable=rec_var)
        comment_entry = ttk.Entry(pane,textvariable=comment_var)
        total_entry = ttk.Label(pane,textvariable=total_var)
        inj_check = ttk.Checkbutton(pane,text='Injection',variable=inj_var)

        # Taste Tree

        # Buttons

        # Injection Frame 
        inj_time_var = tk.StringVar()
        inj_type_var = tk.StringVar()
        conc_var = tk.DoubleVar()
        vol_var = tk.DoubleVar()
        reason_var = tk.StringVar()


        inj_time_var.set(self.data['Injection']['Injection Time'])
        inj_type_var.set(self.data['Injection']['Injection Type'])
        conc_var.set(self.data['Injection']['Concentration (M)'])
        vol_var.set(self.data['Injection']['Volume (ml)'])
        reason_var.(self.data['Injection']['Injection Reason'])

        inj_time_var.trace('w',lambda n,s,x:self.set_injection_var('Injection Time',inj_time_var))
        inj_type_var.trace('w',lambda n,s,x:self.set_injection_var('Injection Type',inj_type_var))
        conc_var.trace('w',lambda n,s,x:self.set_injection_var('Concentration (M)',conc_var))
        vol_var.trace('w',lambda n,s,x:self.set_injection_var('Volume (ml)',vol_var))
        reason_var.trace('w',lambda n,s,x:self.set_injection_var('Injection Reason',reason_var))

        self.inj_frame = ttk.Frame(pane)

        inj_label = ttk.Label(self.inj_frame,text='Injection')
        inj_time_label = ttk.Label(self.inj_frame,text='Time')
        inj_type_label = ttk.Label(self.inj_frame,text='Type')
        inj_conc_label = ttk.Label(self.inj_frame,text='Concentration (M)')
        inj_vol_label = ttk.Label(self.inj_frame,text='Volume (ml)')
        inj_reason_label = ttk.Label(self.inj_frame,text='Reason')

        inj_time_entry = tkw.date_entry(self.inj_frame,textvariable=inj_time_var,acceptedformats=['%H:%M']))
        inj_type_entry = ttk.Entry(self.inj_frame,textvariable=inj_type_var)
        conc_entry = ttk.Entry(self.inj_frame,textvariable=conc_var)
        vol_entry = ttk.Entry(self.inj_frame,textvariable=vol_var)
        reason_entry = ttk.Entry(self.inj_frame,textvariable=reason_var)

        # Grid everything

        if not inj_var.get():
            self.inj_frame.grid_remove()

    def set_test_type(self,*args):
        pass

    def set_var(self,name,var_type='string'):
        pass

    def calibrate(self):
        pass

    def set_data_variables(self):
        pass

class calibrate_popup(object):
    pass

class taste_popup(object):
    pass

class rec_popup(object):
    pass
