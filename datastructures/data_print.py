import pandas as pd
import datetime as dt
from copy import deepcopy

# check datetime string format and convert to datetime
def get_datetime_from_str(date_str):
    accepted_formats = ['%m/%d/%y','%m/%d/%y %H:%M','%m%d%y %H:%M']
    out = None
    for fmt in accepted_formats:
        try:
            out = dt.datetime.strptime(date_str,fmt)
            if out != None:
                break
        except ValueError:
            out = None
    if out==None:
        raise ValueError('Invalid date string format')
    return out

# Turns a dict into a string recursively
def print_dict(dic,tabs=0):
    dic = deepcopy(dic)
    if isinstance(dic,str) or isinstance(dic,int):
        out = str(dic)
        for i in range(tabs):
            out = '    '+out
        return out
    out = ''
    spacing = str(max([len(x) for x in dic.keys()])+4)
    for k,v in dic.items():
        if isinstance(v,pd.DataFrame):
            v_str = '\n'+print_dataframe(v,tabs+1)+'\n'
        elif isinstance(v,dict):
            v_str = '\n'+print_dict(v,tabs+1)
        elif isinstance(v,list):
            v_str = [print_dict(x,tabs) for x in v]
            v_str = '\n'+''.join(v_str)
            v_str = v_str.replace('\n','\n    ')
        elif isinstance(v,dt.datetime):
            if v.hour==0 and v.minute==0:
                v_str = v.strftime('%m/%d/%y')
            else:
                v_str = v.strftime('%m/%d/%y %H:%M')
        elif isinstance(v,dt.date):
            v_str = v.strftime('%m/%d/%y')
        else:
            v_str = v
        fmt = "{:<"+spacing+"}{}"
        out = out + fmt.format(k,v_str) + '\n'
    for i in range(tabs):
        out = '    '+out.replace('\n','\n    ')
    return out

# Turns a pandas dataframe into a string without numerical index, date index will print and be formatted according to idxfmt Date, Datetime or Time
def print_dataframe(df,tabs=0,idxfmt='Date'):
    df = df.copy()
    if df.empty:
        return ''
    if isinstance(df.index,pd.DatetimeIndex):
        if idxfmt == 'Date':
            df.index = df.index.strftime('%m-%d-%y')
        elif idxfmt == 'Datetime':
            df.index = df.index.strftime('%m-%d-%y %H:%M')
            df.index = [re.sub(' 00:00','',x) for x in df.index]
        elif idxfmt == 'Time':
            df.index = df.index.strftime('%h:%M:%S')
        out = df.to_string(index=True)
    else:
        out = df.to_string(index=False)
    for i in range(tabs):
        out = '    '+out.replace('\n','\n    ')
    return out
