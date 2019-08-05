from collections.abc import Mapping
from copy import deepcopy

class BaseMapping(Mapping):
    def __init__(self,initial_dict):
        self._storage = deepcopy(initial_dict)

    def __getitem__(self,key):
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def to_json(self):
        pass

class animal_data(BaseMapping):
    def __init__(self,ID,dob=None,gender='M',
                 protocol=19002,genotype=GENOTYPES[0]):
        '''
        Create blank animal metadata structure

        Parameters
        ----------
        ID : str, animal ID
        dob: datetime.date (optional), date of birth, None (default)
        gender: {'M','F'} (optional), gender, 'M' (default)
        protocol: str (optional), protocol number, 19002 (default)
        genotype: str (optional), genotype, 'Stk11 fl/fl' (default)
        '''
        initial_dict = {'Animal Info':{'ID':ID,'dob':dob,
                                        'gender':gender,
                                        'genotype':genotype},
                         'Weight Log':[],
                         'Water Dep Start':None,
                         'Perfusion Date':None,
                         'Surgeries':[],
                         'IOC Tests':[],
                         'Bottle Tests':[]}
        super().__init__(initial_dict)

class bottle_test(BaseMapping):
    def __init__(self,date=pd.datetime.today().strftime('%m-%d-%y'),
                test_length=10,weight_change=0):
        date = get_valid_datestr(date)
        initial_dict = {'Date':date,
                        'Test Length':test_length,
                        'Weight Change':weight_change}
        super().__init__(initial_dict)

class ioc_test(BaseMapping):
    def __init__(self,test_type,test_time=pd.datetime.today(),weight=None):
        initial_dict = {'Test Type':test_type,
                        'Test Time':get_valid_datestr(test_time,out_format='%m-%d-%y %H:%M'),
                        'Weight':weight,
                        'Rec Basename':None,
                        'Rec Settings':None,
                        'IP Injection':[],
                        'Taste Info':[],
                        'Total Volume Consumed':None,
                        'Comments':None}
        super().__init__(initial_dict)

    def __getitem__(self,key):
        if key == 'Total Volume Consumed':
            dat = self._storage
            if dat['Taste Info'] is not []:
                tmp_vols = [x['Total Volume'] for x in dat['Taste Info']]
                try:
                    tmp_tot = round(sum(tmp_vols),2)
                except TypeError:
                    tmp_tot = None
                dat['Total Volume Consumed'] = tmp_tot
            else:
                dat['Total Volume Consumed'] = None
        return self._storage[key]

class taste_info(BaseMapping):
    def __init__(self,tastant=None,port=None,release_time=None,
            vol_per_trial=None,num_trials=None):
        initial_dict = {'Tastant':tastant,'Port':port,
                        'Release Time (ms)':release_time,
                        'Volume per Trial':vol_per_trial,
                        'Num Trials':num_trials,
                        'Total Volume':None}
        if num_trials and vol_per_trial:
            initial_dict['Total Volume'] = round(float(num_trials*vol_per_trial),2)
        super().__init__(initial_dict)

    def __getitem__(self,key):
        if key is 'Total Volume':
            try:
                tmp = round(float(self._storage['Volume per Trial']*self._storage['Num Trials']),2)
            except TypeError:
                tmp = None
            self._storage['Total Volume'] = tmp
            return tmp
        else:
            return self._storage[key]

    def set_taste_info(self,tastant=None,port=None,release_time=None,
            vol_per_trial=None,num_trials=None):
        '''
        Allows edit of some or all values associated with this tastant.
        Recomputes total volume.

        Parameters
        ----------
        tastant : str (optional)
        port : int (optional)
        release_time : float (optional)
        vol_per_trial : float (optional)
        num_trials : int (optional)
        '''
        dat = self._storage
        if tastant is not None:
            dat['Tastant'] = tastant
        if port is not None:
            dat['Port'] = port
        if release_time is not None:
            dat['Release Time (ms)'] = release_time
        if vol_per_trial is not None:
            dat['Volume per Trial'] = vol_per_trial
        if num_trials is not None:
            dat['Num Trials'] = num_trials
        dat['Total Volume'] = round(float(dat['Num_Trials']*dat['Volume per Trial']),2)


DATE_FORMATS = ['%m/%d/%y','%m-%d-%y','%m/%d/%y %H:%M','%m-%d-%y %H:%M','%H:%M']
PREFERRED_DATE_FORMAT = '%m-%d-%y'

def validate_date(date,accepted_formats=DATE_FORMATS):
    try:
        tmp = get_valid_datestr(date)
        return True
    except ValueError:
        return False

def get_valid_datestr(date,out_format=PREFERRED_DATE_FORMAT,
        accepted_formats=DATE_FORMATS):
    '''
    Returns a valid date string when given a datetime.datetime, datetime.date
    or str
    
    Parameters
    ----------
    date : {str, datetime.datetime, datetime.date}
    out_format : str, PREFERRED_DATE_FORMAT (default)
        format wanted for string representation of date
    accepted_formats : list of str, DATE_FORMATS (default)
    
    Returns
    -------
    str
    
    Raises
    ------
    ValueError, if invalid date string is given
    TypeError, if unexpected date type 
    '''
    if isinstance(date,dt.datetime) or isinstance(date,dt.datetime.date):
        out = date.strftime(out_format)
    elif isinstance(date,str):
        tmp = str_to_date(datestr)
        if tmp is None:
            raise ValueError('%s is not a valid date.' % date)
        else:
            out = tmp.strftime(out_format)
    else:
        raise TypeError(('date is not a valid type. str, '
                        'datetime.datetime or datatime.date'))

    return out

def check_datestr(datestr,accepted_formats=DATE_FORMATS):
    '''
    Returns True if datestr is valid
    
    Parameters
    ----------
    datestr : str, date str to validate
    accepted_formats : list of str, DATE_FORMATS (default)
    
    Returns
    -------
    bool, True if valid date string
    '''
    tmp = str_to_date(datestr)
    if tmp is not None:
        return True
    else:
        return False

def str_to_date(datestr,accepted_formats=DATE_FORMATS):
    '''
    applies various possible date string formats to try and convert datestr to
    a date

    Parameters
    ----------
    datestr : str
    accepted_formats : list of str, DATE_FORMATS contains default list

    Returns
    -------
    datetime.datetime
    '''
    out = None
    for fmt in accepted_formats:
        try:
            tmp = pd.datetime.strptime(datestr,fmt)
        except ValueError:
            tmp = None
        if tmp is not None:
            out = tmp
    return out

