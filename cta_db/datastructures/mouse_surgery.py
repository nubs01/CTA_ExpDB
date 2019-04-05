import pandas as pd
from copy import deepcopy
from .data_print import *


class mouse_surgery(dict):

    BLA = pd.DataFrame([[-1.4,3.4,4.6,200],[-1.4,3.4,4.3,200],
                        [-1.4,-3.4,4.3,200],[-1.4,-3.4,4.6,200]],
                        columns=['AP','ML','DV','Volume'])
    RE = pd.DataFrame([[-.9,1.25,4.2,200],[-.9,1.25,4.0,200],
                        [-.9,-1.25,4.2,200],[-.9,-1.25,4,200]],
                        columns=['AP','ML','DV','Volume'])
    BLA_CRE = {'Virus':'AAV5-CamKII-Cre-GFP','Site':'BLA','Coords':BLA}
    BLA_GFP = {'Virus':'AAV5-CamKII-GFP','Site':'BLA','Coords':BLA}
    CRE_IMPLANT = {'Date':None,'Surgery Type':'BLA Virus Injection, Electrode & IOC Implant',
                    'Pre-op Weight':None,'Post-op Weight':None,
                    'Working Implant Channels':32,'Injections':[BLA_CRE],'Comments':None}
    GFP_IMPLANT = {'Date':None,'Surgery Type':'BLA Virus Injection, Electrode & IOC Implant',
                    'Pre-op Weight':None,'Post-op Weight':None,
                    'Working Implant Channels':32,'Injections':[BLA_GFP],'Comments':None}
    BLANK = {'Date':None,'Surgery Type':'','Pre-op Weight':None,'Post-op Weight':None,
            'Working Implant Channels':32,'Injections':[],'Comments':None}


    SURGERY_MAP = {'BLA_Cre_implant':CRE_IMPLANT,'BLA_GFP_implant':GFP_IMPLANT,'blank':BLANK}
    INJECTION_SITES = {'BLA':BLA,'RE':RE}
    INJECTION_VIRUSES = {'AAV-Cre':'AAV5-CamKII-Cre-GFP','AAV-GFP':'AAV5-CamKII-GFP'}

    def __init__(self,surgery_type='blank',date=None,num_ch=None,pre_weight=None,
            post_weight=None,injections=None,comments=None,**kwargs):
        if isinstance(date,str):
            date = get_datetime_from_str(date)
        tmp = {'Date':date,
                'Pre-op Weight':pre_weight,'Post-op Weight':post_weight,
                'Working Implant Channels':num_ch,'Injections':injections,'Comments':comments}

        # if given a dict use the defaults and update with non-None values from dict
        if isinstance(surgery_type,dict):
            tmp.update((k,v) for k,v in surgery_type.items() if v is not None)
        elif isinstance(surgery_type,str):
            # if the string maps to a default use that default and update with function args
            tmp2 = mouse_surgery.SURGERY_MAP.get(surgery_type)
            if tmp2 is None:
                tmp['Surgery Type'] = surgery_type
            else:
                tmp2 = deepcopy(tmp2)
                tmp2.update((k,v) for k,v in tmp.items() if v is not None)
                tmp = tmp2
        super().__init__(**tmp,**kwargs)
    
    def add_injection(self,virus,site='',coords=pd.DataFrame(columns=['AP','ML','DV','Volume'])):
        if self['Injections'] == None:
            self['Injections'] = []
        if isinstance(virus,dict):
            self['Injections'].append(injection)
        else:
            tmp_virus = mouse_surgery.INJECTION_VIRUSES.get(virus)
            tmp_coords = mouse_surgery.INJECTION_SITES.get(site)
            if tmp_virus == None:
                tmp_virus = virus
            if tmp_coords is None:
                tmp_coords == coords
            self['Injections'].append({'Virus':tmp_virus,'Site':site,'Coords':tmp_coords})

    def pop_injection(self,index):
        return self['Injections'].pop(index)

    def add_injection_site(self,site,ap=None,ml=None,dv=None,volume=None,index=0):
        if self['Injections']==[]:
            return
        if isinstance(site,str):
            df = pd.DataFrame([[ap,ml,dv,volume]],columns=['AP','ML','DV','Volume'])
        elif isinstance(site,list):
            tmp_arr = [[w,x,y,z] for w,x,y,z in zip(ap,ml,dv,volume)]
            df = pd.DataFrame(tmp_arr,columns=['AP','ML','DV','Volume'])
        elif isinstance(site,pd.DataFrame):
            df = site
        else:
            raise ValueError('Incorrect input type. Expects DataFrame with columns [AP,ML,DV,Volume] or (float,float,float,float)')
        self['Injections'][index]['Coords'].append(df)
            
    def __str__(self):
        return print_dict(self)

    def to_string(self,tabs=0):
        out = self.__str__()
        for t in range(tabs):
            out = '    '+out.replace('\n','\n    ')
        return out

    def add_comment(self,comment):
        if self['Comments'] == None:
            self['Comments']=comment
        else:
            self['Comments'] += '; '+ comment
