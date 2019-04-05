import re
import pandas as pd
import datetime as dt
from copy import deepcopy
from .data_print import *

class ioc_test(dict):

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
                                'Concentration (M)':0.15,'Volume (ml)':None,
                                'Injection Reason':'CTA'},
                        'Sham':{'Injection Time':None,'Injection Type':'Saline',
                                'Concentration (M)':None,'Volume (ml)':None,
                                'Injection Reason':'Sham CTA'},
                        'None':{'Injection Time':None,'Injection Type':None,
                                'Concentration (M)':None,'Volume (ml)':None,
                                'Injection Reason':None}}

    HABITUATION = {'Test Type':'Habituation','Test Time':None,
                    'Weight':None,'Taste Info':taste_defaults['habituation'],
                    'Total Volume Consumed':sum(taste_defaults['habituation']['Total Volume']),
                    'Rec Basename':None,'Rec Settings':rec_defaults['none'],
                    'Injection':injection_defaults['None'],'Comments':None}

    CTA_TRAIN = {'Test Type':'CTA Training','Test Time':None,
                'Weight':None,'Taste Info':taste_defaults['cta_train'],
                'Total Volume Consumed':sum(taste_defaults['cta_train']['Total Volume']),
                'Rec Basename':None,'Rec Settings':rec_defaults['array'],
                'Injection':injection_defaults['CTA'],'Comments':None}

    TASTE_ARRAY = {'Test Type':'Taste Array','Test Time':None,
                    'Weight':None,'Taste Info':taste_defaults['array'],
                    'Total Volume Consumed':sum(taste_defaults['array']['Total Volume']),
                    'Rec Basename':None,'Rec Settings':rec_defaults['array'],
                    'Injection':injection_defaults['None'],'Comments':None}

    CTA_TEST = {'Test Type':'CTA Test','Test Time':None,
                'Weight':None,'Taste Info':taste_defaults['cta_test'],
                'Total Volume Consumed':sum(taste_defaults['cta_test']['Total Volume']),
                'Rec Basename':None,'Rec Settings':rec_defaults['array'],
                'Injection':injection_defaults['None'],'Comments':None}

    DEFAULT_MAP = {'habituation':HABITUATION,'train':CTA_TRAIN,'test':CTA_TEST,
                    'array':TASTE_ARRAY}

    def __init__(self,test_data=None):
        if isinstance(test_data,str):
            test_data = ioc_test.DEFAULT_MAP.get(test_data)
            if test_data == None:
                raise ValueError('Invalid default type. options are: ' + ioc_test.DEFAULT_MAP.keys())
        if test_data != None:
            super().__init__(**test_data)
        else:
            super().__init__(**ioc_test.HABITUATION)

    def add_comment(self,comment):
        if self['Comments'] == None:
            self['Comments'] = comment
        else:
            self['Comments'] = '; ' + comment

    def set_test_data(self,test_data):
       self.__init__(test_data)

    def set_test_time(self,time):
        if isinstance(time,str):
            time_obj = get_datetime_from_str(time)
        elif isinstance(time,dt.datetime):
            time_obj = time
        else:
            raise ValueError('Invalid input type. requires str or datetime')
        self['Test Time'] = time_obj

    def set_injection(self,injection):
        self['Injection'] = deepcopy(injection)

    def set_rec_settings(self,rec_settings):
        self['Rec Settings'] = deepcopy(rec_settings)

    def set_taste_info(self,taste_info):
        self['Taste Info'] = deepcopy(taste_info)
        self['Total Volume Consumed'] = sum(taste_info['Total Volume'])

    def to_string(self,tabs=0):
        tmp = deepcopy(self)
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

    def __str__(self):
        return self.to_string()

    def get_summary(self):
        out = ''
        if self['Test Time'] != None:
            out = self['Test Time'].strftime('%m-%d-%y')
        else:
            out = 'No Date'
        out = out+'    '+self['Test Type']
        if self['Rec Basename'] != None:
            out = out+'*'
        return out

    def calibration(self,release_times,vol_per_trial):
        tmp = self['Taste Info']
        if len(release_times) != len(tmp['Tastant']):
            raise ValueError('Expected input for %d tastes, got %d.' % (len(tmp['Tastant']),len(release_times)))
        tmp['Release Time (ms)'] = release_times
        tmp['Volume per Trial'] = vol_per_trial
        tmp['Total Volume'] = [x*y for x,y in zip(vol_per_trial,tmp['Num Trials'])]
        self['Total Volume Consumed'] = sum(tmp['Total Volume'])

    def set_rec_info(self,rec_basename,rec_settings=rec_defaults['array']):
        self['Rec Basename']=rec_basename
        self['Rec Settings'] = rec_settings

    def set_trial_nums(self,trial_nums):
        tmp = self['Taste Info']
        if len(trial_nums) != len(tmp['Tastant']):
            raise ValueError('Expected input for %d tastes, got %d.' % (len(tmp['Tastant']),len(trial_nums)))
        tmp['Num Trials']=trial_nums
        tmp['Total Volume'] = [x*y for x,y in zip(tmp['Volume per Trial'],trial_nums)]
        self['Total Volume Consumed'] = sum(tmp['Total Volume'])

    def set_injection_details(self,inj_time,inj_vol,inj_comments=None):
        tmp = self['Injection']
        if isinstance(inj_time,str):
            m = re.search('\d{2}:\d{2}',inj_time)
            time = dt.datetime.strptime(
                    self['Test Time'].strftime('%m/%d/%y') + ' ' + m.group(0),'%m/%d/%y %H:%M')
        elif isinstance(inj_time,dt.datetime):
            time = inj_time
        else:
            raise ValueError('Invalid time format')
        tmp['Injection Time'] = time
        tmp['Volume (ml)'] = inj_vol
        if inj_comments != None:
            tmp['Injection Reason'] = tmp['Injection Reason'] + '; ' + inj_comments
