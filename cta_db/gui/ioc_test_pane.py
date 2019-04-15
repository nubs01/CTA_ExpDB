import tkinter as tk
from tkinter import ttk
import tk_widgets as tkw
from cta_db.datastructures import data_print as dp, ioc_test

class ioc_test_pane(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        self.data = kwargs.get('data')
        if self.data is not None:
            kwargs.pop('data')
        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.master = master

        self.initUI()

    def initUI(self):
        # Add test widgets
        add_frame = ttk.Frame(self)
        add_button = ttk.Button(add_frame,text='Add IOC Test',command=self.add_test)
        self.new_type_var = tk.StringVar()
        type_opts = list(ioc_test.DEFAULT_MAP.keys())
        self.new_type_var.set(type_opts[0])
        new_type_menu = ttk.OptionMenu(add_frame,self.new_type_var,type_opts[0],*type_opts)
        new_type_menu.grid(row=0,column=0,sticky='w')
        add_button.grid(row=0,column=1,sticky='e')
        add_frame.pack(side='top',fill='x')
        ttk.Separator(self,orient='horizontal').pack(side='top',fill='x',pady=10)

        # Make Scroll frame of ioc_tests
        self.test_segments = []
        self.pane = tkw.scroll_frame(self)
        self.pane.pack(side='top',fill='both',padx=10,pady=10,expand=True)
        n=0
        if self.data is None:
            return

        for ioc in self.data:
            tmp = ioc_test_segment(self.pane.viewport,ioc,n)
            self.test_segments.append(tmp)
            tmp.pack(side='top',fill='x')
            ttk.Separator(self.pane.viewport,orient='horizontal').pack(side='top',fill='x',pady=5)
            n+=1

        self.pane.bind_children_to_mouse()

    def set_data(self,data):
        [x.destroy() for x in self.test_segments]
        self.data = data
        self.test_segments = []
        n=0
        for ioc in self.data:
            tmp = ioc_test_segment(self.pane.viewport,self,ioc,n)
            self.test_segments.append(tmp)
            tmp.pack(side='top',fill='x')
            n+=1
        self.pane.bind_children_to_mouse()

    def add_test(self):
        pass

    def drop_test(self,index):
        pass

class ioc_test_segment(ttk.Frame):
    def __init__(self,parent,master,data,index):
        ttk.Frame.__init__(self,parent)
        self.parent = parent
        self.master = master
        self.index = index
        self.data = data
        self.initUI()

    def initUI(self):
        pane = ttk.Frame(self)
        pane.pack(fill='both',expand=True)

        line1 = ttk.Frame(pane)
        line2 = ttk.Frame(pane)
        line3 = ttk.Frame(pane)
        line4 = ttk.Frame(pane)

        del_pane_button = ttk.Button(line1,text='X',command=lambda:self.parent.drop_test(self.index),
                                    width=3)

        # Labels
        type_label = ttk.Label(line1,text='Type:  ')
        date_label = ttk.Label(line1,text='Date:  ')
        weight_label= ttk.Label(line1,text='Weight:  ')
        rec_label = ttk.Label(line1,text='Rec Name:  ')
        total_label = ttk.Label(line3,text='Total (μL):  ')
        taste_label = ttk.Label(line1,text='Tastants',foreground='red')
        comment_label = ttk.Label(line1,text='Comments:  ')

        type_label.grid(row=0,column=0,sticky='w')
        date_label.grid(row=1,column=0,sticky='w')
        weight_label.grid(row=0,column=3,sticky='w')
        rec_label.grid(row=1,column=3,sticky='w')
        total_label.grid(row=0,column=4,sticky='e')
        taste_label.grid(row=3,column=0,sticky='w')
        comment_label.grid(row=2,column=3,sticky='w')
        line3.grid_columnconfigure(3,weight=2)
        line1.grid_columnconfigure(2,weight=1)

        # TK Vars
        type_var = tk.StringVar()
        date_var = tk.StringVar()
        weight_var = tk.DoubleVar()
        rec_var = tk.StringVar()
        comment_var = tk.StringVar()
        self.total_var = tk.DoubleVar()
        inj_var = tk.BooleanVar()

        type_var.set(self.data['Test Type'])
        date_var.set(dp.get_date_str(self.data['Test Time'],fmt='%m/%d/%y %H:%M'))
        weight_var.set(self.data['Weight'])
        rec_var.set(self.data['Rec Basename'])
        comment_var.set(self.data['Comments'])
        self.total_var.set(round(self.data['Total Volume Consumed'],2))
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
        type_entry = ttk.Entry(line1,textvariable=type_var)
        date_entry = tkw.date_entry(line1,textvariable=date_var,accepted_formats=['%m/%d/%y %H:%M'])
        weight_entry = ttk.Entry(line1,textvariable=weight_var,width=5)
        rec_entry = ttk.Entry(line1,textvariable=rec_var,width=35)
        comment_entry = ttk.Entry(line1,textvariable=comment_var,width=35)
        total_entry = ttk.Label(line3,textvariable=self.total_var,justify='left')
        inj_check = ttk.Checkbutton(line3,text='Injection',variable=inj_var)

        type_entry.grid(row=0,column=1,sticky='w')
        date_entry.grid(row=1,column=1,sticky='w')
        weight_entry.grid(row=0,column=4,sticky='w')
        rec_entry.grid(row=1,column=4,sticky='w')
        comment_entry.grid(row=2,column=4,sticky='w')
        total_entry.grid(row=0,column=5,sticky='w')
        inj_check.grid(row=0,column=2)
        del_pane_button.grid(row=0,column=5,sticky='e')
        line1.grid_columnconfigure(4,weight=2)

        # Taste Tree
        self.fill_tree(frame=line2)

        # Buttons
        calibrate_button = ttk.Button(line3,text='Calibrate',command=self.calibrate)
        rec_button = ttk.Button(line3,text='Rec Settings',command=self.edit_rec_settings)
        plus_button = ttk.Button(line3,text='+',command=self.add_taste,width=3)
        minus_button = ttk.Button(line3,text='-',command=self.delete_taste,width=3)

        calibrate_button.grid(row=0,column=0)
        rec_button.grid(row=0,column=1)
        plus_button.grid(row=0,column=7,sticky='e')
        minus_button.grid(row=0,column=8,sticky='w')
        line3.grid_columnconfigure(6,weight=2)

        # Injection Frame 
        inj_time_var = tk.StringVar()
        inj_type_var = tk.StringVar()
        conc_var = tk.DoubleVar()
        vol_var = tk.DoubleVar()
        reason_var = tk.StringVar()


        inj_time_var.set(dp.get_date_str(self.data['Injection']['Injection Time'],fmt='%H:%M'))
        inj_type_var.set(self.data['Injection']['Injection Type'])
        conc_var.set(self.data['Injection']['Concentration (M)'])
        vol_var.set(self.data['Injection']['Volume (ml)'])
        reason_var.set(self.data['Injection']['Injection Reason'])

        inj_time_var.trace('w',lambda n,s,x:self.set_injection_var('Injection Time',inj_time_var))
        inj_type_var.trace('w',lambda n,s,x:self.set_injection_var('Injection Type',inj_type_var))
        conc_var.trace('w',lambda n,s,x:self.set_injection_var('Concentration (M)',conc_var))
        vol_var.trace('w',lambda n,s,x:self.set_injection_var('Volume (ml)',vol_var))
        reason_var.trace('w',lambda n,s,x:self.set_injection_var('Injection Reason',reason_var))

        self.inj_frame = ttk.Frame(pane)

        inj_label = ttk.Label(self.inj_frame,text='Injection')
        inj_time_label = ttk.Label(self.inj_frame,text='Time')
        inj_type_label = ttk.Label(self.inj_frame,text='Type')
        inj_conc_label = ttk.Label(self.inj_frame,text='Conc. (M)')
        inj_vol_label = ttk.Label(self.inj_frame,text='Vol. (ml)')
        inj_reason_label = ttk.Label(self.inj_frame,text='Reason')

        inj_time_entry = tkw.date_entry(self.inj_frame,textvariable=inj_time_var,
                                        accepted_formats=['%H:%M'],width=5)
        inj_type_entry = ttk.Entry(self.inj_frame,textvariable=inj_type_var,width=17)
        inj_conc_entry = ttk.Entry(self.inj_frame,textvariable=conc_var,width=8)
        inj_vol_entry = ttk.Entry(self.inj_frame,textvariable=vol_var,width=8)
        inj_reason_entry = ttk.Entry(self.inj_frame,textvariable=reason_var,width=17)

        self.inj_frame.grid_columnconfigure(0,pad=5)
        self.inj_frame.grid_columnconfigure(1,pad=5)
        self.inj_frame.grid_columnconfigure(2,pad=5)
        self.inj_frame.grid_columnconfigure(3,pad=5)
        self.inj_frame.grid_columnconfigure(4,pad=5)
        inj_time_label.grid(row=0,column=0,sticky='w')
        inj_type_label.grid(row=0,column=1,sticky='w')
        inj_conc_label.grid(row=0,column=2)
        inj_vol_label.grid(row=0,column=3)
        inj_reason_label.grid(row=0,column=4,sticky='w')
        inj_time_entry.grid(row=1,column=0,sticky='w')
        inj_type_entry.grid(row=1,column=1,sticky='w')
        inj_conc_entry.grid(row=1,column=2)
        inj_vol_entry.grid(row=1,column=3)
        inj_reason_entry.grid(row=1,column=4,sticky='w')


        # Grid lines
        line1.pack(side='top',fill='x',pady=5)
        line2.pack(side='top',anchor='w',pady=5)
        line3.pack(side='top',fill='x',pady=5)
        self.inj_frame.pack(side='bottom',fill='x',anchor='se',pady=5)
        ttk.Separator(self,orient='horizontal').pack(side='bottom',fill='x',pady=5)

        if not inj_var.get():
            self.inj_frame.pack_forget()

    def injection_check(self,var):
        if var:
            self.inj_frame.pack(side='bottom',fill='x',anchor='se',pady=5)
        else:
            self.inj_frame.pack_forget()

    def fill_tree(self,frame=None):
        if frame is not None or not hasattr(self,tree):
            self.tree = ttk.Treeview(frame,height=6)
            sbar = ttk.Scrollbar(frame,orient='vertical',command=self.tree.yview)
            self.tree.configure(yscrollcommand=sbar.set)
            self.tree['columns'] = ['tastant','port','release','n_trials','vol_per_trial','total_vol']

            self.tree.column('#0',anchor='center',width=50)
            self.tree.heading('#0',text='Idx')

            self.tree.column('tastant',anchor='center',width=110)
            self.tree.heading('tastant',text='Tastant')
            self.tree.column('port',anchor='center',width=50)
            self.tree.heading('port',text='Port')
            self.tree.column('release',anchor='center',width=90)
            self.tree.heading('release',text='Time (ms)')
            self.tree.column('vol_per_trial',anchor='center',width=110)
            self.tree.heading('vol_per_trial',text='Vol/Trial (μL)')
            self.tree.column('total_vol',anchor='center',width=110)
            self.tree.heading('total_vol',text='Total Vol (μL)')
            self.tree.column('n_trials',anchor='center',width=90)
            self.tree.heading('n_trials',text='Num Trials')
            self.tree.pack(side='left',fill='both')
            sbar.pack(side='right',fill='y')

        dat = self.data['Taste Info']
        for x in range(len(dat['Tastant'])):
            tmp_id = self.tree.insert('','end',text=str(x),
                                    values=[dat['Tastant'][x],dat['Port'][x],dat['Release Time (ms)'][x],
                                        dat['Num Trials'][x],dat['Volume per Trial'][x],
                                        round(dat['Total Volume'][x],2)])

        self.total_var.set(round(self.data['Total Volume Consumed'],2))

    def set_test_type(self,*args):
        pass

    def set_var(self,name,var_type='string'):
        pass

    def calibrate(self):
        pass

    def set_data_variables(self):
        pass

    def add_taste(self):
        pass

    def delete_taste(self):
        pass

    def edit_rec_settings(self):
        pass

class calibrate_popup(object):
    pass

class taste_popup(object):
    pass

class rec_popup(object):
    pass
