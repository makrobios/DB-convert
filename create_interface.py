# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 21:04:34 2016

@author: ch
"""
from tkinter import *
from tkinter import ttk
import tkFileDialog

root = Tk()
input_file = tk.StringVar()
output_file = tk.StringVar()


root.title("Radlobby Import")

mainframe = ttk.Frame(root)
mainframe.grid()

e_in = Entry(mainframe, textvariable=input_file)
e_out = Entry(mainframe, textvariable= output_file)
b_in = ttk.Button(mainframe, text="input file",
    command=lambda: input_file.set(tkFileDialog.askopenfilename()))
b_out = ttk.Button(mainframe, text="input file",
    command=lambda: output_file.set(tkFileDialog.askopenfilename()))
b_run = ttk.Button(mainframe,text = "Start Script", command ="").grid(column=5, row=5, sticky=E)

b_in.grid_configure()
b_out.grid_configure()
e_in.grid_configure()
e_out.grid_configure()
root.mainloop()


