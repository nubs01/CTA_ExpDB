import os
import pickle
import platform

DB_FILE = 'data/cta_anim_db.p'
OS = platform.node()

def save_anim_db(anim_db,save_file=DB_FILE):
    with open(save_file,'wb') as f:
        pickle.dump(anim_db,f)

def load_anim_db(open_file=DB_FILE):
    if not os.path.isfile(open_file):
        anim_db = {OS:{}}
        save_anim_db(anim_db)
    else:
        with open(open_file,'rb') as f:
            anim_db = pickle.load(f)
    return anim_db

def add_animal_to_db(animID,animFile):
    anim_db = load_anim_db()
    if anim_db.get(OS) is None:
        anim_db[OS] = {}
    anim_db[OS].update({animID:animFile})
    save_anim_db(anim_db)

def delete_animal_from_db(animID):
    anim_db = load_anim_db()
    if anim_db.get(OS) is None:
        raise ValueError('Database entries not found for '+OS)
    else:
        if anim_db[OS].get(animID) is not None:
            anim_db[OS].pop(animID)
            save_anim_db(anim_db)
        else:
            warning.warn('Could not delete %s. Animal not found in local database' % animID)

def load_anim_data(animID):
    anim_db = load_anim_db()
    if anim_db.get(OS) is None:
        anim_db[OS] = {}
        save_anim_db(anim_db)
    anim_path = anim_db[OS].get(animID)
    if anim_path == None:
        return None
    with open(anim_path,'rb') as f:
        anim_dat = pickle.load(f)
    return anim_dat
