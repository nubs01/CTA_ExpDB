import pandas as pd
import datetime as dt
import numpy as np
import seaborn as sns

def print_dict(dic,tabs=0):
    out = ''
    for k,v in dic.items():
        if type(v) == pd.DataFrame:
            v_str = '\n'+print_dataframe(v,tabs+1)
        elif type(v) == dict:
            v_str = '\n'+print_dict(v,tabs+1)
        else:
            v_str = v
        out = out + "{:<20}{}".format(k,v_str) + '\n'
    for i in range(tabs):
        out = '    '+out.replace('\n','\n    ')
    return out

def print_dataframe(df,tabs=0,idxfmt='Date'):
    if df.empty:
        return ''
    if isinstance(df.index,pd.DatetimeIndex):
        if idxfmt == 'Date':
            df.index = df.index.strftime('%m-%d-%y')
        elif idxfmt == 'Datetime':
            df.index = df.index.strftime('%m-%d-%y %H:%M')
        elif idxfmt == 'Time':
            df.index = df.index.strftime('%h:%M:%S')
        out = df.to_string(index=True)
    else:
        out = df.to_string(index=False)
    for i in range(tabs):
        out = '    '+out.replace('\n','\n    ')
    return out


class animal():
    def __init__(self,ID='',dob=[], gender='M', protocol=19002, genotype='Stk11 fl/fl'):
        self.creation_date = dt.date.today()
        self.anim_info = {'ID':ID,'Log Creation Date':dt.date.today(),
                'Protocol':protocol,'DOB':dob,
                'Gender':gender,'Genotype':genotype}
        self.pre_op = pd.DataFrame(columns=['Pre-op','Comments']) # dataframe date as index
        self.surgery = {'Date':[],'Pre-op Weight':[],'Post-op Weight':[],'Injection':[]} # dict
        self.water_dep_start = [] # datetime.datetime(year,month,day,min,hr)
        self.bottle_tests =  pd.DataFrame(columns=['Substance','Test Length (min)',
            'Bottle Start (g)','Bottle End (g)','Change (g)'])# dataframe, datetime index
        self.ioc_tests = [] # List of ioc_test objects
        self.perfusion_date = []

    def to_string(self,tabs=0):
        out = 'Log Output Date: ' + dt.date.today().strftime('%m-%d-%y') + '\n\n'
        out = out + print_dict(self.anim_info)
        out = out+'\n\n----------\nPre-op\n----------\n\n'
        if not self.pre_op.empty:
            out = out + print_dataframe(self.pre_op.copy())
            out = out +'\n\n'
        out = out+'----------\nSurgery\n----------\n\n'
        if self.surgery['Date'] != []:
            out = out + print_dict(self.surgery) + '\n\n'
        if self.water_dep_start != []:
            out = out+'Water Deprivation Start Date: ' + self.water_dep_start.strftime('%m-%d-%y %H:%M') + '\n\n'
        out = out+'----------\nBottle Tests\n----------\n\n'
        if not self.bottle_tests.empty:
            out = out + print_dataframe(self.bottle_tests.copy(),idxfmt='Datetime') + '\n\n'

        out = out+'----------\nIOC Tests\n----------\n\n'
        if self.ioc_tests != []:
            for t in ioc_tests:
                out = out + t.to_string(tabs=tabs+1) + '\n---\n'
            out = out+'\n'
        if self.perfusion_date != []:
            out = out+'----------\n\nPerfusion Date: ' + self.perfusion_date.strftime('%m-%d-%y')

        return out

    def add_pre_op(self,opt,comment,date=dt.datetime.today()):
        df = pd.DataFrame([[opt,comment]],index=[date],columns=self.pre_op.columns)
        self.pre_op = self.pre_op.append(df)

    def add_bottle_test(self,start_weight,end_weight,date=dt.datetime.today(),
            substance='Water',length=10):
        df = pd.DataFrame([[substance,length,start_weight,end_weight,start_weight-end_weight]],
                index=[date],columns=self.bottle_tests.columns)
        self.bottle_tests = self.bottle_tests.append(df)
    

