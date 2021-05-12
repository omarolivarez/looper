# -*- coding: utf-8 -*-
"""
Created on Wed May 12 17:28:46 2021
@author: Omar Olivarez
"""
import tkinter
from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilename
import pandas as pd
from tkinter.ttk import Frame, Button, Style, Progressbar
from tkinter import scrolledtext
import os
import datetime

class Looper(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        #self.path = ""
        #self.starting_row = 0
        self.df = 0
        
    def initUI(self):        
        # this section sets which columns are the ones that move - weight is what will expand when expanded
        self.pack(fill=BOTH, expand=True)
        #self.rowconfigure(5, pad=7)
        #self.rowconfigure(17, weight=1)
        #self.columnconfigure(3, weight=1)
        #self.columnconfigure(3, pad=7)
        
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Import csv", command=self.import_csv_data)
        #filemenu.add_separator()
        #filemenu.add_command(label="Save", command=self.save)
        menubar.add_cascade(label="File", menu=filemenu)
        
        region_l = Label(self, text = "Region of Origin")
        region_l.grid(row = 1, column = 0, padx = 0, sticky=E)
        region_2 = Label(self, text = "Region of 2")
        region_2.grid(row = 1, column = 0, padx = 0, sticky=E)
        
        self.progress = Progressbar(self, orient = HORIZONTAL, length=950, mode = 'determinate')
        self.progress.grid(row=0, column = 0, columnspan=2, pady = 3, padx = 3, sticky=N+S+E+W)
        
    def import_csv_data(self):
        csv_file_path = askopenfilename()
        self.setPath(csv_file_path)# .set(csv_file_path)
        d = pd.read_csv(self.getPath())
        self.setDataframe(d)

def main():
    global v
    # Create window object
    root = Tk()
    root.title("Looper")
    root.geometry('1000x700') # width x height
    root.minsize("400", "400")
    app = Looper()
    root.mainloop()

if __name__ == '__main__':
    main()
