import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
from controller import controller
matplotlib.use('Agg')

if __name__ == '__main__':
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.theme_use('clam')
    root.geometry('900x600')
    controller(root).pack(side='right',fill='both',expand=True)
    root.mainloop()
