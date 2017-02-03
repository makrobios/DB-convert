# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 22:34:00 2016

@author: ch
"""
import glob
import os
import re
from datetime import datetime
import locale
import pandas as pd
from numpy import nan
from tkinter import Tk, ttk, messagebox, StringVar
from tkinter import filedialog as fdial
import csv

#locale.setlocale(locale.LC_TIME, "deu_deu")

root = Tk()
timestamp = datetime.strftime(datetime.now(),'%Y_%m_%d')
df = pd.DataFrame()
de_input_file = StringVar()
de_SNR = StringVar()
de_outputfile = 'de_import_' + timestamp + '.mer'
de_abotype = ''
header = ''
def de_filepath(file):
    file.set(fdial.askopenfilename(initialdir=r'%HOMEPATH%/Downloads'))
    if isinstance(file.get(), str):
        de_b_run.state(['!disabled'])

        
def drahtesel_reformat(file, snr):
    #fieldnames = ['Geburtsdatum','Anmerkungen','#','Vorname','Titel','Adresse','Wie sind Sie auf den Drahtesel aufmerksam geworden?','Abo','Telefon','Geschlecht','Ort','Willkommenspaket','Addresse','Email','Veranstaltung','Postleitzahl','Zahlung','Telefonnummer','Nachname','E-Mail','Date Submitted','sonstiges']
    header_mitglied = ['SNR', 'Date Submitted', 'Titel', 'VN', 'NAME', 'STRASSE', 'PLZ', 'ORT', 'mobil', 'email', 'Abo', 'Notizen']
    header_geschenk = ['SNR', 'Date Submitted', 'Titel', 'VN', 'NAME', 'STRASSE', 'PLZ', 'ORT', 'mobil', 'email', 'Titel_2', 'VN_2', 'NAME_2', 'STRASSE_2', 'PLZ_2', 'ORT_2', 'email_2', 'Abo', 'Zahlung', 'Willkommenspaket', 'Anmerkungen']
    header_probe =    ['SNR', 'Date Submitted', 'Titel', 'VN', 'NAME', 'STRASSE', 'PLZ', 'ORT', 'mobil', 'email', 'Anrede','Gebdatum','Herkunft','Notizen','Sonstiges']
    with open(file,'r') as f_out:
        header = f_out.readline()
        if len(header.split(',')) == 21:
            header = header_geschenk
        elif len(header.split(',')) == 15:
            header = header_probe
        elif len(header.split(',')) == 12:
            header = header_mitglied
        
        snr = int(snr)
  


        csvreader.fieldnames = fieldnames
        for line in csvreader:            
            writer.writerow(line)
               
        
       
   
    try:
        df.to_csv(de_outputfile,
                  sep=";",
                  index=False,
                  encoding='windows-1252')
    except IOError:
        print('ERROR: Could not write to output file')
#    return df
    messagebox.showinfo('Drahtesel Mitlgieder Konvertierung', 'Drahtesel Konvertierung beendet!\n'+
                         'Die Ausgabedatei ist\n' + de_outputfile)



# Documentation for df.replace
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.df.replace.html


###############################################################################

'''Setup graphical User Interface with inputfile and a start button
'''
### GUI with tkinter



root.title("Reformatierung für Kartei Import")
root.geometry('300x100')
f = ttk.Frame(root, padding=(5, 10), width=300, height=100)
f['borderwidth'] = 5
f['relief'] = 'raised'

#e_in = ttk.Entry(f, textvariable=input_file, width=40)
#e_snr = ttk.Entry(f, textvariable=SNR, width=10)
#b_in = ttk.Button(f, text="Radlobby CSV wählen",
#                  command=lambda: filepath(input_file))
#b_run = ttk.Button(f, text="Start Script",
#               command=lambda: run_db_conversion(input_file.get(), SNR.get()))
#l_snr = ttk.Label(f, text='erste SNR')
# root.columnconfigure and .rowconfigure are important for resizing !
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
#f.grid(column=0, row=0, sticky=("N, W, E, S"))
#f.columnconfigure(0, weight=1)
#f.columnconfigure(1, weight=1)
#f.rowconfigure(3, weight=1)
#f.rowconfigure(0, weight=1)
#### Radlobby grid layout 
#b_in.grid_configure(column=0, row=0, sticky="N")
#e_in.grid_configure(column=0, row=1, sticky="N")
#l_snr.grid(column=0, row=2)
#e_snr.grid(column=0, row=3)
#
#b_run.grid(column=0, row=5, sticky="EW")
#b_run.state(['disabled'])

### Drahtesel part of window

de_f = ttk.Frame(root,padding=(5, 10),width=300, height=100).grid()
de_b_in = ttk.Button(de_f, text = "Drahtesel Abonnement Datei auswählen",
                     command=lambda: de_filepath(de_input_file))
de_e_in = ttk.Entry(de_f, textvariable=de_input_file, width=40)
de_l_snr = ttk.Label(de_f, text='erste SNR')
de_e_snr = ttk.Entry(de_f, textvariable=de_SNR, width=10)
de_b_run = ttk.Button(de_f, text="Start Drahtesel",
               command=lambda: drahtesel_reformat(de_input_file.get(), de_SNR.get()))
### Drahtesel grid layout
de_b_in.grid_configure(column=0, row=6, sticky="N")
de_e_in.grid_configure(column=0, row = 7, sticky = "N")
de_l_snr.grid(column=0, row=9)
de_e_snr.grid(column=0, row=10)
de_b_run.grid(column=0, row = 11, sticky = "EW")

root.mainloop()