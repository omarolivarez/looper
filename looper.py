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
import sqlite3
import bstrap as bs


class Looper(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.path = ""
        #self.starting_row = 0
        self.df = 0
        self.con = sqlite3.connect("looper.db")
        self.cur = self.con.cursor()
        
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
        
        region_l = Label(self, text = "Label 1")
        region_l.grid(row = 1, column = 0, padx = 0, sticky=W)
        region_2 = Label(self, text = "Label 2")
        region_2.grid(row = 1, column = 1, padx = 0, sticky=E)
        
        self.progress = Progressbar(self, orient = HORIZONTAL, length=750, mode = 'determinate')
        self.progress.grid(row=0, column = 0, columnspan=2, pady = 3, padx = 3, sticky=N+S+E+W)
        
    def import_csv_data(self):
        csv_file_path = askopenfilename()
        self.setPath(csv_file_path)# .set(csv_file_path)
        d = pd.read_csv(self.getPath())
        self.setDataframe(d)
        self.popup_details()
        print("HERE")
        
    def popup_details(self):
        win = Toplevel()
        win.wm_title("Import Details")
        win.geometry("300x300")
        win.minsize("300", "300")
        win.rowconfigure(5, weight=1)
        win.columnconfigure(1, weight=1)
        v = IntVar()
    
        l = Label(win, text="Column to bootstrap")
        l.grid(row=0, column=0, pady=(10, 0), padx=(10, 0))
        COL_OPTS= list(self.df)
        self.col_var = StringVar(self)
        self.col_var.set(COL_OPTS[0]) # default value
        dropdown_col = OptionMenu(win, self.col_var, *COL_OPTS) #, command=lambda _: self.getFont()
        dropdown_col.config(indicatoron=False)
        dropdown_col.grid(row = 0, column=1, sticky = W, pady=(10, 0)) 
        
        stats_label = Label(win, text="Statistic")
        stats_label.grid(row=1, column=0, sticky=E, pady=(5, 0))
        STAT_OPTS= ['Mean', 'Median', 'St Dev']
        self.stat_var = StringVar(self)
        self.stat_var.set(STAT_OPTS[0]) # default value
        dropdown_stat = OptionMenu(win, self.stat_var, *STAT_OPTS)
        dropdown_stat.config(indicatoron=False)
        dropdown_stat.grid(row = 1, column=1, sticky = W, pady=(5, 0)) 
        
        reps_label = Label(win, text="Repetitions")
        reps_label.grid(row=2, column=0, sticky=E, pady=(5, 0))
        self.reps = Entry(win, width='12')
        self.reps.grid(row=2, column=1, sticky=W, pady=(5, 0))
        
        reps_file_label = Label(win, text="Upload reps file?")
        reps_file_label.grid(row=3, column=0, sticky=E, pady=(5, 0))
        no_rb = Radiobutton(win, text="No", variable=v, value=1)
        no_rb.grid(row = 3, column = 1, pady=(5, 0), sticky = W)
        yes_rb = Radiobutton(win, text="Yes", variable=v, value=2)
        yes_rb.grid(row = 4, column = 1, pady=(5, 0), sticky = W)
    
        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=5, column=1, sticky=S+W, pady=(5, 10), padx=(0, 10))
        
    def getFont(self):
        return
        #col = self.font_var.get()
        #self.myFont.configure(size=int(font_size))
        
    def setPath(self, p):
        self.path = p
    
    def getPath(self):
        return self.path
    
    def setDataframe(self, dataframe):
        self.df = dataframe
        
    def getDataframe(self):
        return self.df

def main():
    global v
    # Create window object
    root = Tk()
    root.title("Looper")
    root.geometry('800x500') # width x height
    root.minsize("400", "400")
    app = Looper()
    root.mainloop()

if __name__ == '__main__':
    main()
