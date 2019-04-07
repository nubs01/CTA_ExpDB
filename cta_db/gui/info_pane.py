import tk_widgets as tkw
from tkinter import ttk
import tkinter as tk
from cta_db.datastructures.animal import animal
import datetime as dt
from cta_db.datastructures.data_print import *

class anim_info_pane(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        self.data = kwargs.get('data')
        if self.data is not None:
            kwargs.pop('data')
        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.master = master
        self.parent = parent
        self.pack(fill='both',anchor='nw',expand=True)
        if self.data is not None:
            self.initUI()
        else:
            self.pane = tk.Frame(self)
            self.pane.pack()

    def initUI(self):
        self.pane = tk.Frame(self)
        self.pane.pack(side='left',anchor='nw',pady=10)

        # Labels
        protocol_label = ttk.Label(self.pane,text='Protocol:  ')
        dob_label = ttk.Label(self.pane,text='DOB:  ')
        gender_label = ttk.Label(self.pane,text='Gender:  ')
        geno_label = ttk.Label(self.pane,text='Genotype:  ')
        water_dep_label = ttk.Label(self.pane,text='Water Dep Start:  ')
        perfusion_label = ttk.Label(self.pane,text='Perfusion Date:  ')

        # Variables
        self.protocol_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.geno_var = tk.StringVar()
        self.water_var = tk.StringVar()
        self.perfusion_var = tk.StringVar()

        # Traces
        self.protocol_var.trace('w',lambda n,s,x: self.set_var('Protocol',self.protocol_var,out_type='int'))
        self.dob_var.trace('w',lambda n,s,x: self.set_var('DOB',self.dob_var,out_type='date'))
        self.gender_var.trace('w',lambda n,s,x: self.set_var('Gender',self.gender_var))
        self.geno_var.trace('w',lambda n,s,x: self.set_var('Genotype',self.geno_var))
        self.water_var.trace('w',lambda n,s,x: self.set_water(self.water_var))
        self.perfusion_var.trace('w',lambda n,s,x: self.set_perfusion(self.perfusion_var))

        # Set initial values
        self.set_data_vars()

        # Entry fields
        proto_entry = ttk.Entry(self.pane,textvariable=self.protocol_var)
        dob_entry = tkw.date_entry(self.pane,textvariable=self.dob_var)
        gender_option = ttk.OptionMenu(self.pane,self.gender_var,'M','M','F')
        geno_option = ttk.OptionMenu(self.pane,self.geno_var,self.geno_var.get(),*animal.GENOTYPES)
        water_entry = tkw.date_entry(self.pane,textvariable=self.water_var)
        perfusion_entry = tkw.date_entry(self.pane,textvariable=self.perfusion_var)

        # Grid it all
        self.pane.grid_rowconfigure(0,pad=5)
        self.pane.grid_rowconfigure(1,pad=5)
        self.pane.grid_rowconfigure(2,pad=5)
        self.pane.grid_rowconfigure(3,pad=5)
        self.pane.grid_rowconfigure(4,pad=5)
        self.pane.grid_rowconfigure(5,pad=5)


        protocol_label.grid(row=0,column=0,sticky='w')
        dob_label.grid(row=1,column=0,sticky='w')
        gender_label.grid(row=2,column=0,sticky='w')
        geno_label.grid(row=3,column=0,sticky='w')
        water_dep_label.grid(row=4,column=0,sticky='w')
        perfusion_label.grid(row=5,column=0,sticky='w')

        proto_entry.grid(row=0,column=1)
        dob_entry.grid(row=1,column=1)
        gender_option.grid(row=2,column=1)
        geno_option.grid(row=3,column=1)
        water_entry.grid(row=4,column=1)
        perfusion_entry.grid(row=5,column=1)

    def set_var(self,name,var,out_type='string'):
        if self.data is None:
            return
        if out_type is 'string':
            out = var.get()
        elif out_type is 'int':
            if var.get() is '':
                out = None
            else:
                val = var.get()
                if val.isnumeric():
                    out = int(val)
                else:
                    out = None
        elif out_type is 'date':
            out = get_datetime_from_str(var.get())

        self.data.anim_info[name] = out
        self.master.saved=False

    def set_water(self,var):
        if self.data is None:
            return
        self.data.water_dep_start = get_datetime_from_str(var.get())
        self.master.saved=False

    def set_perfusion(self,var):
        if self.data is None:
            return
        self.data.perfusion_date = get_datetime_from_str(var.get())
        self.master.saved=False

    def set_data(self,data):
        self.pane.destroy()
        self.data = data
        if data is not None:
            self.initUI()

    def set_data_vars(self):
        dat = self.data.anim_info
        self.protocol_var.set(str(dat['Protocol']))

        date_str = get_date_str(dat['DOB'])
        self.dob_var.set(date_str)

        date_str = get_date_str(self.data.water_dep_start)
        self.water_var.set(date_str)

        date_str = get_date_str(self.data.perfusion_date)
        self.perfusion_var.set(date_str)

        self.gender_var.set(dat['Gender'])
        self.geno_var.set(dat['Genotype'])
