import tkinter as tk
from tkinter import ttk, scrolledtext
import tk_widgets as tkw
from cta_db.datastructures import mouse_surgery as surgery
from cta_db.datastructures.data_print import *

class surgery_pane(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        tmp = kwargs.get('data')
        if tmp is not None:
            self.surgery_data = kwargs.pop('data')
        else:
            self.surgery_data = []
        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.pack(expand=True,fill='both',anchor='nw')
        self.parent = parent
        self.master = master
        self.initUI()

    def initUI(self):
        self.surgery_segments = []
        
        # Button and droplist for new surgeries
        self.template_var = tk.StringVar(self)
        self.templates = list(surgery.SURGERY_MAP.keys())
        self.button_frame = ttk.Frame(self)
        self.template_var.set(self.templates[0])
        self.template_select = ttk.OptionMenu(self.button_frame,self.template_var,self.template_var.get(),*self.templates)
        self.template_select.pack(side='left',padx=2,pady=1)
        self.add_button = ttk.Button(self.button_frame,text='New Surgery',
                                    command=self.new_surgery)
        self.add_button.pack(side='left',padx=1,pady=1)
        self.button_frame.pack(side='top',fill='x',padx=1,pady=1)
        ttk.Separator(self,orient='horizontal').pack(side='top',fill='x')


        # Add surgery frames to canvas
        self.scrollpane = tkw.scroll_frame(self)
        self.scrollpane.pack(side='top',fill='both',expand=True)
        n = 0
        for s in self.surgery_data:
            tmp = surgery_segment(self.scrollpane.viewport,self.master,data=s,index=n)
            tmp.bind("<Button-4>",self.scrollpane._on_mousewheel)
            tmp.bind("<Button-5>",self.scrollpane._on_mousewheel)
            self.surgery_segments.append(tmp)
            tmp.pack(side='top',fill='x')
            n+=1

        # Scroll test filling
        #for x in range(30):
        #    tmp = ttk.Button(self.scrollpane.viewport,text='Testing %i' % x)
        #    tmp.pack(side='top',fill='x')
        #    tmp.bind("<Button-4>",self.scrollpane._on_mousewheel)
        #    tmp.bind("<Button-5>",self.scrollpane._on_mousewheel)

    def set_data(self,data):
        self.surgery_data = data
        for s in self.surgery_segments:
            s.destroy()
        self.surgery_segments = []
        n = 0
        for s in self.surgery_data:
            tmp = surgery_segment(self.scrollpane.viewport,self.master,data=s,index=n)
            tmp.bind("<Button-4>",self.scrollpane._on_mousewheel)
            tmp.bind("<Button-5>",self.scrollpane._on_mousewheel)
            self.surgery_segments.append(tmp)
            tmp.pack(side='top',fill='x')
            n+=1


    def new_surgery(self):
        tmp = surgery(self.template_var.get())
        self.surgery_data.append(tmp)
        tmp_frame = surgery_segment(self.scrollpane.viewport,self.master,data=tmp,index=len(self.surgery_data)-1)
        self.surgery_segments.append(tmp_frame)
        tmp_frame.pack(side='top',fill='x')
        self.master.saved=False

    def delete_surgery(self,index):
        self.surgery_data.pop(index)
        self.surgery_segments.pop(index).destroy()
        if len(self.surgery_segments)>index:
            for s in self.surgery_segments[index:]:
                s.index-=1
        self.master.saved=False


# segments for each surgery
# Has lock function to prevent changes when checked
class surgery_segment(ttk.Frame):
    def __init__(self,parent,master,*args,**kwargs):
        self.data = kwargs.pop('data')
        self.index = kwargs.pop('index')
        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.master = master
        self.initUI()

    def initUI(self):
        line = ttk.Frame(self,relief='sunken')
        line.bind("<Button-4>",self.parent.parent._on_mousewheel)
        line.bind("<Button-5>",self.parent.parent._on_mousewheel)

        # Make Date field
        date_label = ttk.Label(line,text='Date:  ')
        self.date_var = tk.StringVar()
        text = get_date_str(self.data['Date'])
        self.date_var.set(text)
        self.date_box = tkw.date_entry(line,self.date_var)
        self.date_var.trace('w',lambda n,s,x:self.set_var('Date',self.date_var))
        date_label.grid(row=0,column=0,sticky='e')
        self.date_box.grid(row=0,column=1,columnspan=2,sticky='ew')

        # Make Surgery Type Field
        type_label = ttk.Label(line,text='Surgery Type:  ')
        self.type_var = tk.StringVar()
        self.type_var.set(self.data['Surgery Type'])
        self.type_var.trace('w',lambda n,s,x: self.set_var('Surgery Type',self.type_var))
        type_entry = ttk.Entry(line,textvariable=self.type_var)
        type_label.grid(row=1,column=0,sticky='e')
        type_entry.grid(row=1,column=1,columnspan=3,sticky='ew')


        # Pre-op weight Field
        preop_label = ttk.Label(line,text='Pre-op Weight:  ')
        self.preop_var = tk.DoubleVar(self)
        self.preop_var.set(self.data['Pre-op Weight'])
        self.preop_var.trace('w',lambda n,s,x: self.set_var('Pre-op Weight',self.preop_var))
        preop_entry = ttk.Entry(line,textvariable=self.preop_var,width=10)
        preop_label.grid(row=2,column=0,sticky='e')
        preop_entry.grid(row=2,column=1)

        # Post-op weight Field
        postop_label = ttk.Label(line,text='Post-op Weight:  ')
        self.postop_var = tk.DoubleVar(self)
        self.postop_var.set(self.data['Post-op Weight'])
        self.postop_var.trace('w',lambda n,s,x: self.set_var('Post-op Weight',self.postop_var))
        postop_entry = ttk.Entry(line,textvariable=self.postop_var,width=10)
        postop_label.grid(row=3,column=0,sticky='e')
        postop_entry.grid(row=3,column=1)

        # Implant Channels Field
        imp_ch_label = ttk.Label(line,text='Num channels')
        self.imp_ch_var = tk.IntVar(self)
        self.imp_ch_var.set(self.data['Working Implant Channels'])
        self.imp_ch_var.trace('w',lambda n,s,x: self.set_var('Working Implant Channels',self.imp_ch_var))
        imp_ch_entry = ttk.Entry(line,textvariable=self.imp_ch_var,width=5)
        imp_ch_label.grid(row=2,column=3)
        imp_ch_entry.grid(row=3,column=3)
        line.grid_columnconfigure(2,weight=1)


        # Comment field
        comment_label =ttk.Label(line,text='Comments:  ')
        self.comment_var = tk.StringVar()
        self.comment_var.set(self.data['Comments'])
        self.comment_var.trace('w',lambda n,s,x: self.set_var('Comments',self.comment_var))
        comment_entry = scrolledtext.ScrolledText(line,wrap=tk.WORD,height=5,width=25)
        comment_entry.replace('1.0','end',self.comment_var.get())
        comment_entry.bind('<KeyRelease>',lambda evt: self.set_stringvar(comment_entry,self.comment_var))
        comment_label.grid(row=4,column=0,sticky='ne')
        comment_entry.grid(row=4,column=1,columnspan=3,rowspan=2,sticky='nsew')


        # Injections
        injection_label = ttk.Label(line,text='Injections',foreground='red',font=('Arial Bold',16))
        self.virus_var = tk.StringVar()
        self.site_var = tk.StringVar()
        self.virus_list = surgery.INJECTION_VIRUSES
        self.site_list = surgery.INJECTION_SITES
        self.virus_var.set(list(self.virus_list.keys())[0])
        self.site_var.set(list(self.site_list.keys())[0])
        select_virus = ttk.OptionMenu(line,self.virus_var,self.virus_var.get(),*list(self.virus_list.keys()))
        select_site = ttk.OptionMenu(line,self.site_var,self.site_var.get(),*list(self.site_list.keys()))
        self.new_injection_button = ttk.Button(line,text='Add Injection',command=self.add_injection)
        self.delete_inection_button = ttk.Button(line,text='Delete Injection',command=self.delete_injection)

        self.injection_tree = ttk.Treeview(line,height=5)
        sbar = ttk.Scrollbar(line,orient='vertical',command=self.injection_tree.yview)
        self.injection_tree.config(yscrollcommand=sbar.set)
        self.injection_tree['columns'] = ('Virus','Site','Num')
        self.injection_tree.column('#0',anchor='center',width=50)
        self.injection_tree.heading('#0',text='Idx')
        self.injection_tree.column('Virus',anchor='center')
        self.injection_tree.heading('Virus',text='Virus')
        self.injection_tree.column('Site',anchor='center',width=50)
        self.injection_tree.heading('Site',text='Target')
        self.injection_tree.column('Num',anchor='center',width=50)
        self.injection_tree.heading('Num',text='# Sites')
        for x in range(len(self.data['Injections'])):
            tmp_id = self.injection_tree.insert('','end',text=str(x))
            self.injection_tree.set(tmp_id,'Virus',self.data['Injections'][x]['Virus'])
            self.injection_tree.set(tmp_id,'Site',self.data['Injections'][x]['Site'])
            self.injection_tree.set(tmp_id,'Num',str(len(self.data['Injections'][x]['Coords'])))

        injection_label.grid(row=6,column=0,columnspan=2,sticky='w')
        select_virus.grid(row=7,column=0)
        select_site.grid(row=7,column=1)
        self.new_injection_button.grid(row=7,column=2)
        self.delete_inection_button.grid(row=7,column=3)
        self.injection_tree.grid(row=8,column=0,columnspan=4,rowspan=2,sticky='nesw')
        sbar.grid(row=8,column=4,rowspan=2,sticky='ns')

        # Pack lines
        ttk.Button(line,text='X',width=5,
                command=lambda: self.parent.parent.parent.delete_surgery(self.index)).grid(row=0,column=7,rowspan=2,sticky='ne')
        line.grid_columnconfigure(6,weight=1)
        line.pack(side='top',fill='both',expand=True)
        ttk.Separator(self,orient='horizontal').pack(side='bottom',fill='x')
        col_count, row_count = line.grid_size()
        for row in range(row_count):
                line.grid_rowconfigure(row, minsize=20)

    def set_stringvar(self,text,var):
        var.set(text.get("1.0",'end'))
        self.master.saved=False

    def delete_injection(self):
        self.master.saved = False
        try:
            item = self.injection_tree.selection()[0]
        except IndexError:
            return
        index = int(self.injection_tree.item(item,'text'))
        self.data['Injections'].pop(index)
        self.injection_tree.delete(item)
        children = self.injection_tree.get_children()
        n=0
        for x in children:
            self.injection_tree.item(x,text=str(n))
            n+=1

    def add_injection(self):
        self.data.add_injection(self.virus_var.get(),self.site_var.get())
        index = len(self.data['Injections'])-1
        tmp_id = self.injection_tree.insert('','end',text=str(index))
        self.injection_tree.set(tmp_id,'Virus',self.data['Injections'][index]['Virus'])
        self.injection_tree.set(tmp_id,'Site',self.data['Injections'][index]['Site'])
        self.injection_tree.set(tmp_id,'Num',str(len(self.data['Injections'][index]['Coords'])))
        self.master.saved=False

    def set_var(self,name,var):
        try:
            if name=='Date':
                tmp = get_datetime_from_str(var.get())
            else:
                tmp = var.get()
            self.data[name] = tmp
        except tk.TclError:
            self.data[name] = None
            var.set('')
        self.master.saved=False
