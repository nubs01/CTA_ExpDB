from datastructures import cta_animal as cta, mouse_surgery as surgery, ioc_test as ioc
from copy import deepcopy
import pickle
import datetime as dt

a1 = cta.animal('RN5')
a1.dob = dt.datetime.strptime('10/10/18','%m/%d/%y')

a1.add_pre_op('Handling',date = '3/9/19 13:00')
a1.add_pre_op('Handling',date = '3/10/19 13:30')
a1.add_pre_op('Box Habituation',date = '3/11/19 13:00')
a1.add_pre_op('Box Habituation','He hates it','3/12/19 14:00')

s1 = surgery.mouse_surgery('BLA_cre_implant',pre_weight=34.2,post_weight=36,date='3/13/19',num_ch=31)
a1.add_surgery(s1)

i1 = ioc.ioc_test('habituation')
i1.set_test_time('3/22/19 13:30')
i1['Weight'] = 33.2
i1.calibration([8],[18.8])
a1.add_ioc_test(i1)

i2 = ioc.ioc_test('array')
i2.set_test_time('3/23/19 13:30')
i2['Weight'] = 31.4
i2.calibration([8,9,9,7],[18.4,19.6,20,18.8])
i2.set_rec_info('RN5_4taste_preCTA_190323',ioc.ioc_test.rec_defaults['array'])
a1.add_ioc_test(i2)

i3 = ioc.ioc_test('train')
i3.set_test_time('3/24/19 13:00')
i3['Weight'] = 31.3
i3.calibration([8],[19.1])
i3.set_rec_info('RN5_ctaTrain_190324')
i3.set_injection_details('13:30',0.56)
a1.add_ioc_test(i3)

i4 = deepcopy(i2)
i4.set_test_time('3/25/19 14:00')
i4.set_rec_info('RN5_4taste_postCTA_190325')
i4.calibration([8,9,9,7],[18.4,19.8,19.6,18])
a1.add_ioc_test(i4)

i5 =  ioc.ioc_test('test')
i5.set_test_time('3/25/19 12:30')
i5['Weight'] = 30.8
i5.set_rec_info('RN5_SaccTest_190325')
i5.calibration([8],[18.6])
a1.add_ioc_test(i5)

a1.add_bottle_test(55.6,54.7,'3/20/19 20:00')
a1.add_bottle_test(60.1,59.0,'3/21/19 20:00')
a1.add_bottle_test(62.2,61.3,'3/22/19 20:00')
a1.add_bottle_test(58.4,57.9,'3/23/19 20:00')
a1.add_bottle_test(54.7,54.1,'3/24/19 20:30','Saccharin 0.2M')

a2 = deepcopy(a1)
a2.ID='RN6'
a2.surgery[0].add_comment('Gave 0.5cc Ringers after')
a2.surgery[0].add_comment('Super active an hour after')

tmp_path = '/home/roshan/Dropbox/Harmonia/Neuro_Vault/cta_db'
pickle.dump(a1,open('RN5_metadata.p','wb'))
pickle.dump(a2,open('RN6_metadata.p','wb'))
#anim_db = {a1.ID:tmp_path+'/RN5_metadata.p',a2.ID:tmp_path+'/RN6_metadata.p'}
#pickle.dump(anim_db,open('cta_anim_db.p','wb'))
