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
from configparser import ConfigParser


class Looper(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.path = ""
        self.reps_path = ""
        #self.starting_row = 0
        self.df = 0
        self.con = sqlite3.connect("looper.db")
        self.cur = self.con.cursor()
        self.table_name = ""
        
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
        #print("HERE")
        
    def import_reps(self):
        print("IMPORT REPS()")
        if self.radio == 2:
            reps_file_path = askopenfilename()
            self.set_reps_path(reps_file_path)# .set(csv_file_path)
            f = open(self.get_reps_path(), "r")
            self.set_reps(f)
        
    def popup_details(self):
        win = Toplevel()
        win.wm_title("Details")
        win.geometry("230x230") #  width by height
        win.minsize("220", "230")
        win.rowconfigure(5, weight=1)
        win.columnconfigure(1, weight=1)
        self.radio = IntVar() # use this to store the value of the radio button
        self.radio.set(1)
        
        reps_file_label = Label(win, text="Upload reps file?")
        reps_file_label.grid(row=0, column=0, sticky=E, pady=(5, 0))
        no_rb = Radiobutton(win, text="No", variable=self.radio, value=1)
        no_rb.grid(row = 0, column = 1, pady=(5, 0), sticky = W)
        self.yes_rb = Radiobutton(win, text="Yes", variable=self.radio, value=2)
        self.yes_rb.grid(row = 1, column = 1, pady=(5, 0), sticky = W)
    
        l = Label(win, text="Column to bootstrap", state = 'disabled')
        l.grid(row=2, column=0, pady=(10, 0), padx=(10, 0))
        COL_OPTS= list(self.df)
        self.col_var = StringVar(self)
        self.col_var.set(COL_OPTS[0]) # default value
        dropdown_col = OptionMenu(win, self.col_var, *COL_OPTS, state = 'disabled') #, command=lambda _: self.getFont()
        dropdown_col.config(indicatoron=False)
        dropdown_col.grid(row = 2, column=1, sticky = W, pady=(10, 0)) 
        
        stats_label = Label(win, text="Statistic", state = 'disabled')
        stats_label.grid(row=3, column=0, sticky=E, pady=(5, 0))
        STAT_OPTS= ['Mean', 'Median', 'St Dev']
        self.stat_var = StringVar(self)
        self.stat_var.set(STAT_OPTS[0]) # default value
        dropdown_stat = OptionMenu(win, self.stat_var, *STAT_OPTS, state = 'disabled')
        dropdown_stat.config(indicatoron=False)
        dropdown_stat.grid(row = 3, column=1, sticky = W, pady=(5, 0)) 
        
        reps_label = Label(win, text="Repetitions", state = 'disabled')
        reps_label.grid(row=4, column=0, sticky=E, pady=(5, 0))
        self.reps = Entry(win, width='12', state = 'disabled')
        self.reps.grid(row=4, column=1, sticky=W, pady=(5, 0))
        
        
    
        b = Button(win, text="Next", command= self.create_table) #lambda:[win.destroy, self.create_table, self.import_reps]
        b.grid(row=5, column=1, sticky=S+W, pady=(5, 10), padx=(0, 10))
        
    def create_table(self):
        print("CREATE TABLE()")
        # NOTE: in a future feature, I need to know how to handle what happens if someone wants to run bootstrap for the same column and metric all over
        # again given that I think in the current state it would just append to the previous results
        self.set_table_name()
        print(self.table_name)
        #col_1 = self.col_var.get().upper() + "_"  + self.stat_var.get().upper() + "S"
        #print(col_1)
        
        """self.cur.execute('SELECT * FROM ?', (self.table_name))
        entry = self.cur.fetchone()
        if entry is None:
            self.cur.execute('CREATE TABLE ? ', ('a', 'b', 'c'))
            print('New table created')
        else:
            print('Table already exists')
        return"""
        create_table_query = "CREATE TABLE IF NOT EXISTS " + self.table_name + " (id integer PRIMARY KEY,statistic integer);"
        #create_table_query = "CREATE TABLE IF NOT EXISTS liwc_means (id integer PRIMARY KEY,statistic integer);"
        print(create_table_query)
        self.cur.execute(create_table_query)
    
    def getFont(self):
        return
        #col = self.font_var.get()
        #self.myFont.configure(size=int(font_size))
        
    def setPath(self, p):
        self.path = p
        
    def set_table_name(self):
        self.table_name = self.col_var.get().upper() + "_" + self.stat_var.get().upper() + "S"  # 
    
    def getPath(self):
        return self.path
    
    def set_reps_path(self, p):
        self.reps_path = p
        
    def get_reps_path(self):
        return self.reps_path
        
    def set_reps(self, f):
        r = f.readline()
        self.reps = int(r)
    
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
