import pandas as pd
import datetime as dt
import numpy as np
import seaborn as sns

# Turns a dict into a string recursively
def print_dict(dic,tabs=0):
    out = ''
    for k,v in dic.items():
        if type(v) == pd.DataFrame:
            v_str = '\n'+print_dataframe(v,tabs+1)+'\n'
        elif type(v) == dict:
            v_str = '\n'+print_dict(v,tabs+1)
        else:
            v_str = v
        out = out + "{:<25}{}".format(k,v_str) + '\n'
    for i in range(tabs):
        out = '    '+out.replace('\n','\n    ')
    return out

# Turns a pandas dataframe into a string without numerical index, date index will print and be formatted according to idxfmt Date, Datetime or Time
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

# Data strcture to contain IOC trial information (Habtuation and recording)
class ioc_defaults():

    taste_defaults = {'habituation':{'Tastant':['Water'],'Port':[31],'Intan Channel':[24],
                                'Release Time (ms)':[8],'Volume per Trial':[20],
                                'Num Trials':[45],
                                'Total Volume':[x*y for x,y in zip([20],[45])]},
                    'array':{'Tastant':['Water','Quinine','NaCl','Citric Acid'],
                        'Port':[31,33,35,37],'Intan Channel':[24,26,19,21],
                        'Release Time (ms)':[8,9,9,7],'Volume per Trial':[20,20,20,20],
                        'Num Trials':[15,15,15,15],
                        'Total Volume':[x*y for x,y in zip([20,20,20,20],[15,15,15,15])]},
                     'cta_train':{'Tastant':['Saccharin'],'Port':[31],'Intan Channel':[24],
                        'Release Time (ms)':[8],'Volume per Trial':[20],
                        'Num Trials':[45],
                        'Total Volume':[x*y for x,y in zip([20],[45])]},
                     'cta_test':{'Tastant':['Saccharin'],'Port':[31],'Intan Channel':[24],
                        'Release Time (ms)':[8],'Volume per Trial':[20],
                        'Num Trials':[15],
                        'Total Volume':[x*y for x,y in zip([20],[15])]}}

    rec_defaults = {'none':{'Num Channels':None,'Sampling Rate (Hz)':None,
                        'High-Pass Filter (Hz)':None,'Notch Filter (Hz)':None,
                        'Digital Inputs':[]}, #TODO: Correct this
                    'array':{'Num Channels':32,'Sampling Rate (Hz)':30000,
                        'High-Pass Filter (Hz)':250,'Notch Filter (Hz)':60,
                        'Digital Inputs':[1,2,3,4]}} #TODO: Correct this

    injection_defaults = {'CTA':{'Injection Time':None,'Injection Type':'LiCl',
                            'Concentration (M)':0.15,'Volume (ml)':None},
                        'Sham':{'Injection Time':None,'Injection Type':'Saline',
                            'Concentration (M)':None,'Volume (ml)':None},
                        'None':{'Injection Time':None,'Injection Type':None,
                            'Concentration (M)':None,'Volume (ml)':None}}

class ioc_test():
    HABITUATION = {'Test Type':'Habituation','Test Time':None,
            'Weight':None,'Taste Info':ioc_defaults.taste_defaults['habituation'],
            'Total Volume Consumed':sum(ioc_defaults.taste_defaults['habituation']['Total Volume']),
            'Rec Basename':None,'Rec Settings':ioc_defaults.rec_defaults['none'],
            'Injection':ioc_defaults.injection_defaults['None']}

    CTA_TRAIN = {'Test Type':'CTA Training','Test Time':None,
            'Weight':None,'Taste Info':ioc_defaults.taste_defaults['cta_train'],
            'Total Volume Consumed':sum(ioc_defaults.taste_defaults['cta_train']['Total Volume']),
            'Rec Basename':None,'Rec Settings':ioc_defaults.rec_defaults['array'],
            'Injection':ioc_defaults.injection_defaults['CTA']}

    TASTE_ARRAY = {'Test Type':'Taste Array','Test Time':None,
            'Weight':None,'Taste Info':ioc_defaults.taste_defaults['array'],
            'Total Volume Consumed':sum(ioc_defaults.taste_defaults['array']['Total Volume']),
            'Rec Basename':None,'Rec Settings':ioc_defaults.rec_defaults['array'],
            'Injection':ioc_defaults.injection_defaults['None']}
    
    CTA_TEST = {'Test Type':'CTA Test','Test Time':None,
            'Weight':None,'Taste Info':ioc_defaults.taste_defaults['cta_test'],
            'Total Volume Consumed':sum(ioc_defaults.taste_defaults['cta_test']['Total Volume']),
            'Rec Basename':None,'Rec Settings':ioc_defaults.rec_defaults['array'],
            'Injection':ioc_defaults.injection_defaults['None']}

    def __init__(self,test_data):
        self.test_data = test_data.copy()

    def set_test_data(self,test_data):
       self.test_data = test_data.copy()

    def set_injection(self,injection):
        self.test_data['Injection'] = injection.copy()

    def set_rec_settings(self,rec_settings):
        self.test_data['Rec Settings'] = rec_settings.copy()

    def set_taste_info(self,taste_info):
        self.test_data['Taste Info'] = taste_info.copy()
        self.test_data['Total Volume Consumed'] = sum(taste_info['Total Volume'])

    def get_injection_info(self):
        return self.test_data['Injection'].copy()

    def get_test_data(self):
        return self.test_data.copy()

    def get_rec_settings(self):
        return self.test_data['Rec Settings'].copy()

    def to_string(self,tabs=0):
        tmp = self.test_data.copy()
        tmp['Taste Info'] = pd.DataFrame(tmp['Taste Info'])
        if tmp['Injection']['Injection Time']==None:
            tmp.pop('Injection')
        if tmp['Rec Basename'] == None:
            tmp.pop('Rec Basename')
            tmp.pop('Rec Settings')
        out = print_dict(tmp)
        for i in range(tabs):
            out = '    '+out.replace('\n','\n    ')
        return print_dict(tmp)


# Data structure to hold animal info and handling, habituation and experiment logs 
class animal():
    def __init__(self,ID='',dob=None, gender='M', protocol=19002, genotype='Stk11 fl/fl'):
        self.creation_date = dt.date.today()
        self.anim_info = {'ID':ID,'Log Creation Date':dt.date.today(),
                'Protocol':protocol,'DOB':dob,
                'Gender':gender,'Genotype':genotype}
        self.pre_op = pd.DataFrame(columns=['Pre-op','Comments']) # dataframe date as index
        self.surgery = {'Date':None,'Pre-op Weight':None,'Post-op Weight':None,'Injection':None} # dict
        self.water_dep_start = None # datetime.datetime(year,month,day,min,hr)
        self.bottle_tests =  pd.DataFrame(columns=['Substance','Test Length (min)',
            'Bottle Start (g)','Bottle End (g)','Change (g)'])# dataframe, datetime index
        self.ioc_tests = [] # List of ioc_test objects
        self.perfusion_date = None

    def to_string(self,tabs=0):
        out = 'Log Output Date: ' + dt.date.today().strftime('%m-%d-%y') + '\n\n'
        out = out + print_dict(self.anim_info)
        out = out+'\n\n----------\nPre-op\n----------\n\n'
        if not self.pre_op.empty:
            out = out + print_dataframe(self.pre_op.copy())
            out = out +'\n\n'
        out = out+'----------\nSurgery\n----------\n\n'
        if self.surgery['Date'] != None:
            out = out + print_dict(self.surgery) + '\n\n'
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

    def add_pre_op(self,opt,comment,date=dt.datetime.today()):
        df = pd.DataFrame([[opt,comment]],index=[date],columns=self.pre_op.columns)
        self.pre_op = self.pre_op.append(df)

    def add_bottle_test(self,start_weight,end_weight,date=dt.datetime.today(),
            substance='Water',length=10):
        df = pd.DataFrame([[substance,length,start_weight,end_weight,start_weight-end_weight]],
                index=[date],columns=self.bottle_tests.columns)
        self.bottle_tests = self.bottle_tests.append(df)

    def add_ioc_test(self,new_test):
        if not isinstance(new_test,ioc_test):
            new_test = ioc_test(new_test)
        self.ioc_tests.append(new_test)
    

