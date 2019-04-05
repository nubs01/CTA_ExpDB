from cta_db.gui import surgery_pane
from cta_db import dbio
import cta_db.datastructures as cta
import tkinter as tk

anim_dat = dbio.load_anim_data('RN5')



if __name__=='__main__':
    root = tk.Tk()
    pane = surgery_pane.surgery_pane(root,root,data=anim_dat.surgery)
    pane.pack()
    root.mainloop()

