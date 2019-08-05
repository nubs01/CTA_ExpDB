import pandas as pd
import datetime as dt
from copy import deepcopy
from ..datastructures import ioc_test as ioc, mouse_surgery as surgery
from .data_print import *
import matplotlib
matplotlib.use('TkAgg')
import seaborn as sns

# Re work to have dict of dicts and dataframes, 
# Have dataframe of weights for animals for each day,
#

# Data structure to hold animal info and handling, habituation and experiment logs 
class animal():
    GENOTYPES = ['Stk11 fl/fl','C57Bl/6J','Df(16)1/+']

    def __init__(self,ID='',dob=None, gender='M', protocol=19002, genotype=GENOTYPES[0]):
        self.creation_date = dt.date.today()
        self.ID = ID
        self.anim_info = {'Log Creation Date':dt.date.today(),
                'Protocol':protocol,'DOB':dob,
                'Gender':gender,'Genotype':genotype}
        self.pre_op = pd.DataFrame(columns=['Pre-op','Comments']) # dataframe date as index
        self.surgery = [] # list of mouse_surgery objects
        self.water_dep_start = None # datetime.datetime(year,month,day,min,hr)
        self.bottle_tests =  pd.DataFrame(columns=['Substance','Test Length (min)',
            'Bottle Start (g)','Bottle End (g)','Change (g)'])# dataframe, datetime index
        self.ioc_tests = [] # List of ioc_test objects
        self.perfusion_date = None

    def to_string(self,tabs=0):
        out = 'Log Output Date: ' + dt.date.today().strftime('%m-%d-%y') + '\n\n'
        out = out + "{:<25}{}".format('Animal ID',self.ID) + '\n'
        out = out + print_dict(self.anim_info)
        out = out+'\n\n----------\nPre-op\n----------\n\n'
        if not self.pre_op.empty:
            out = out + print_dataframe(self.pre_op.copy(),idxfmt='Datetime')
            out = out +'\n\n'
        out = out+'----------\nSurgery\n----------\n\n'
        if self.surgery != []:
            for ms in self.surgery:
                out = out + ms.to_string(tabs=tabs+1) + '\n---\n'
            out = out+'\n'
        if self.water_dep_start != None:
            out = out+'Water Deprivation Start Date: ' + self.water_dep_start.strftime('%m-%d-%y %H:%M') + '\n\n'
        out = out+'----------\nBottle Tests\n----------\n\n'
        if not self.bottle_tests.empty:
            out = out + print_dataframe(self.bottle_tests.copy(),idxfmt='Datetime') + '\n\n'

        out = out+'----------\nIOC Tests\n----------\n\n'
        if self.ioc_tests != []:
            for t in self.ioc_tests:
                out = out + t.to_string(tabs=tabs+1) + '\n---\n'
            out = out+'\n'
        if self.perfusion_date != None:
            out = out+'----------\n\nPerfusion Date: ' + self.perfusion_date.strftime('%m-%d-%y')

        return out

    def __str__(self):
        return self.to_string()

    def copy(self):
        return deepcopy(self)

    def add_pre_op(self,opt,comment=None,date=dt.datetime.today()):
        if isinstance(date,str):
            date = get_datetime_from_str(date)
        df = pd.DataFrame([[opt,comment]],index=[date],columns=self.pre_op.columns)
        self.pre_op = self.pre_op.append(df)

    def add_bottle_test(self,start_weight,end_weight,date=dt.datetime.today(),
            substance='Water',length=10):
        if isinstance(date,str):
            date = get_datetime_from_str(date)
        df = pd.DataFrame([[substance,length,start_weight,end_weight,start_weight-end_weight]],
                index=[date],columns=self.bottle_tests.columns)
        self.bottle_tests = self.bottle_tests.append(df)

    def add_ioc_test(self,new_test):
        if not isinstance(new_test,ioc.ioc_test):
            new_test = ioc.ioc_test(new_test)
        self.ioc_tests.append(deepcopy(new_test))
    
    def set_pre_op(self,pre_op):
        self.pre_op = deepcopy(pre_op)

    def set_bottle_tests(self,bottle_tests):
        self.bottle_tests = deepcopy(bottle_tests)

    def set_ioc_tests(self,ioc_tests):
        self.ioc_tests = deepcopy(ioc_tests)

    def add_surgery(self,new_surgery):
        if self.surgery == None:
            self.surgery = []
        if not isinstance(new_surgery,surgery.mouse_surgery):
            raise ValueError('New Surgeries must be mouse_surgery objects.')
        self.surgery.append(deepcopy(new_surgery))

    def get_ioc_summaries(self):
        out = ''
        for t in self.ioc_tests:
            out = out+t.get_summary()+'\n'
        return out

    def get_animal_data(self):
        out = {'Creation Date':self.creation_date,'Animal Info':self.anim_info.copy(),
                'Pre-op':self.pre_op.copy(),'Surgery':self.surgery.copy(),
                'Water Dep Start':self.water_dep_start,
                'Bottle Tests':self.bottle_tests.copy(),'IOC Tests':self.ioc_tests.copy(),
                'Perfusion Date':self.perfusion_date}
        return deepcopy(out)

    def set_all_animal_data(self,newDat):
        self.creation_date = newDat['Creation Date']
        self.anim_info = newDat['Animal Info']
        self.pre_op = newDat['Pre-Op']
        self.surgery = newDat['Surgery']
        self.water_dep_start = newDat['Water Dep Start']
        self.bottle_tests = newDat['Bottle Tests']
        self.ioc_tests = newDat['IOC Tests']
        self.perfusion_date = newDat['Perfusion Date']

    def set_perfusion_date(self,date=dt.datetime.today()):
        if isinstance(date,str):
            date = get_datetime_from_str(date)
        self.perfusion_date = date

    def plot_bottle_tests(self):
        tmp = self.bottle_tests.copy()
        ctaDay = next(item['Test Time'] for item in self.ioc_tests if item['Test Type']=='CTA Training')
        a = ctaDay.replace(hour=0,minute=0,second=0)
        b = ctaDat.replace(hour=23,minute=59,second=59)
        tmp2 = tmp.truncate(after=a).append(tmp.truncate(before=b))
        tmp2['Norm Change'] = tmp2['Change (g)']/tmp2.groupby('Substance').mean()['Change (g)']['Water']
        g = sns.barplot(data=tmp2,x='Substance',y='Norm Change')
        return g
