# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 22:34:00 2016

@author: ch
"""

from tkinter import *
from tkinter import ttk
import tkFileDialog
from numpy import nan
import pandas as pd
from datetime import datetime
import re
import locale
locale.setlocale(locale.LC_TIME, "deu_deu")

# Documentation for df.replace
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.df.replace.html
''' ToDo: Kinder aufsplitten auf mehrere Reihen -> Problem mit umlauten ! --> done
          Anschlußmitglieder, einzieher betrag aufsplitten ( + kein DE )
          Mitgliedskategorien --> done
          Beitrittsdatum --> done
          SEPA  --> done '''

def run_db_conversion(inputfile):
    print "starting conversion.....\n"
    kinder = {}
    header=['webform_serial','webform_sid','webform_time','Beitritt','webform_modified_time','webform_draft','webform_ip_address','webform_uid','SNR','VN','NAME','Mitgliedskategorien','aktionscode','freiwilliger_beitrag','vorname_v','nachname_v','STRASSE','PLZ','ORT','mobil','EMAIL','GEBDATUM','Anrede','kinder_bis','kinder_bis_19','anschlussmembers','Notizen','zahlungsart','iban15','bic15','einzieher_check','summe','bezahlstatus','orderid','Herkunft,EinzNotizen']
    df = pd.read_csv(inputfile,
                     sep=';',
                     skiprows=3,
                     header=None,
                     names=header,
                     index_col=False,
                     dtype={'mobil': str},
                     encoding='utf-8')
# set new index to achieve that Anschlussmtg are right next to
# the Hauptmtg
    new_index = [x*10 for x in df.index.get_values()]
    df['new_index'] = new_index
    df = df.set_index('new_index')
    df['ANSZU'] = nan
################ Anschlußmitglieder
    for row in df.index:
        Name = ''
        VN = ''
        gebdatum = ''
        email = ''
        series = pd.Series()
        anschluss = df.Notizen.ix[row]
        if pd.notnull(anschluss):
            series = df.ix[row]     # copy row of Hauptmitglied
            series_index = int(series.name) + 1
            series = series.rename(index=series_index)
            series = series.drop(['kinder_bis', 'kinder_bis_19'])
            series.ix['Mitgliedskategorien'] = 2
            series.ix['keinDE'] = '1'   # value has to be of type string  
            series.ix['ANSZU'] = 1  # mark as Anschlußmitglied 
            data = re.split(',|;', anschluss)
            series['Hauptmitglied'] = series.ix['VN'] + ' ' + series.ix['NAME']
            gesamtname = re.search(ur'[A-Za-zäüöß\-]+\s[A-Za-zäüöß\-]+', anschluss)
            VN = gesamtname.group(0).split(' ')[0]
            NAME = gesamtname.group(0).split(' ')[1]
            gebdatum = re.search(r'[\d+\.]+|\d+', anschluss)
            email = re.search(r'\w+\@[\w.]+', anschluss)
            if NAME:
                series.loc['NAME'] = NAME
            if VN:
                series.loc['VN'] = VN
            if gebdatum:
                series.loc['GEBDATUM'] = gebdatum.group(0)
            if email:
                series.loc['EMAIL'] = email.group(0)
            df = df.append(series)
    
    df = df.sort_index()
    
    mobil = df.mobil.tolist()
    row_vorwahl = []
    row_nummer = []
    pattern = [r'\s+', r'^0043', r'^\+43', r'^43', r'^0', r'[^\d]']
    for phonenumber in mobil:
        if pd.isnull(phonenumber):            # checking for value nan
            row_vorwahl.append(phonenumber)
            row_nummer.append(phonenumber)
            continue
        for pat in pattern:
            phonenumber = re.sub(pat, '', phonenumber)
        predial = '0'+phonenumber[0:3]
        rest = phonenumber[3:]
        row_vorwahl.append(predial)
        row_nummer.append(rest)
    
    df['mobil'] = row_nummer
    df.insert(18, 'vorwahltelmobil', row_vorwahl)
    
    # Capitalize first letter of VN and NAME
    df.VN = df.VN.str.title()
    df.NAME = df.NAME.str.title()
    
    ########## children + birthday, add columns for up to seven
    for i in range(1, 8):
        kind = 'kind' + str(i)
        kind_dat = 'kind' + str(i) + '_dat'
        df[kind] = None
        df[kind_dat] = None
    # split entries with more than 1 children
    for index, entry in zip(df.index, df.kinder_bis_19):
        if pd.isnull(entry):
            continue
        elif df.ix[index, 'kinder_bis'] < 2:
            kinder[index] = [entry]
        else:
            entry = re.sub(ur'\r\n|\r|\n', ';', entry)
            kinder[index] = entry.split(';')
    
    for index in sorted(kinder.keys()):
        i = 0
        for kind in filter(lambda x: x != '', kinder[index]):
            i = i + 1
            kinderspalte = 'kind' + str(i)
            kindergeburtstag = kinderspalte + '_dat'
            m = re.search(ur'[A-Za-züöäß\s-]+', kind)
            if m:
                name = m.group(0)
            date = re.findall(r'\d+\.\d+\.\d+|\d+', kind)
            # print index, '\t', kind
            if name:
                df.ix[index, kinderspalte] = name
            if date:
                df.ix[index, kindergeburtstag] = date[0]
    # kind_max = df.kinder_bis.max()
    # for kids in df.kinder_bis_19.replace("\n",",",regex=True).str.split(","):
    #    if isinstance(kids,list):
    #        children.append(kids)
    #    else:
    #        children.append(None)
    # Add SNR Number automatically
    df['SNR'] = range(50000, 50000+int(len(df.index)))
    # add Hauptmitglied SNR to Anschlußmitglied
    for row in df.index:
        if pd.notnull(df.ix[row, 'ANSZU']):
            df.ix[row, 'ANSZU'] = df.ix[row, 'SNR'] - 1
    df['ANSZU'] = df['ANSZU'].map('{:.0f}'.format)
    df['ANSZU'].replace('nan', '', inplace=True)
    # set Anrede to (Herr, Frau, Firma, sonstiges)
    df.replace(u'männlich', u'Herr', inplace=True)
    df.replace(u'weiblich', u'Frau', inplace=True)
    # Beitritt Datum, Herkunft
    df.Beitritt.replace(r'\s-\s\d+:\d+', '', regex=True, inplace=True)
    df['Herkunft'] = 'radlobby.at'
    # Set entries to Mitglied and Mitgliedkategorie normal
    # df['Mitgliedskategorien'] = 1
    # 1 = normal, 2= Anschluss, 3= Student, 4= Juniormitglied , 5= Fördermitglied
    # 6 = Gratis-Mitgliedschaft, 7= Sozialtarif
    df['Mitglied'] = 1
    df.Mitgliedskategorien.replace(u'Vollmitglied', 1, inplace=True)
    df.Mitgliedskategorien.replace(u'Haushaltsmitglied', 2, inplace=True)
    df.Mitgliedskategorien.replace(u'StudentIn (bis 26 Jahre)', 3, inplace=True)
    df.Mitgliedskategorien.replace(u'Junior (bis 18 Jahre)', 4, inplace=True)
    df.Mitgliedskategorien.replace(u'Fördermitglied', 5, inplace=True)
    # SEPA
    df['einzieher_check'].replace('X', 'einzieher', inplace=True)
    for index, einzieher in zip(df.einzieher_check.index, df.einzieher_check):
        if einzieher == 'einzieher':
            df.ix[index, 'EinzNotizen'] = datetime.strftime(datetime.now(), '%B')
            if df.anschlussmembers.ix[index] < 1:
                df.ix[index, 'einzbeitrag2015'] = str(df.ix[index, 'summe']).replace('.', ',')
    # convert Nan in Notizen to empty string '' to allow concatenation
    df.Notizen.replace(nan, '', inplace=True)
    df.Notizen = df.Notizen + ";" + df.summe.map(str) + ';' + df.zahlungsart
    # Writing to csv file, for import to filemaker 5 it has to be named .mer and
    # use ";" as seperator
    timestamp = datetime.strftime(datetime.now(), '%Y%m%d_%H_%M')
    try:
        df.to_csv(inputfile + '_' + timestamp + '.mer',
           sep=";",
           index=False,
           encoding='windows-1252',
           columns=['SNR', 'Mitglied', 'Mitgliedskategorien', 'VN', 'NAME',      'Anrede', 'STRASSE', 'PLZ', 'ORT', 'vorwahltelmobil', 'mobil',
                    'EMAIL', 'GEBDATUM', 'iban15', 'bic15', 'einzieher_check',
                    'kind1', 'kind1_dat', 'kind2', 'kind2_dat', 'kind3',
                    'kind3_dat', 'kind4', 'kind4_dat', 'kind5', 'kind5_dat',
                    'moremembers', 'summe', 'einzbeitrag2015', 'EinzNotizen',         'Beitritt', 'Herkunft', 'Notizen', 'keinDE', 'ANSZU'])
    except IOError:
        print 'ERROR: Could not write to output file'
    print "Conversion finished!"


'''Setup graphical User Interface with inputfile and a start button
TODO=> Start Button should only be clickable after inputfile was chosen
    => Progress Bar or Start Finish messages
'''
root = Tk()
input_file = StringVar()


root.title("Radlobby Import")

mainframe = ttk.Frame(root)
mainframe.grid()

e_in = Entry(mainframe, textvariable=input_file)
b_in = ttk.Button(mainframe, text="input file", command=lambda: input_file.set(tkFileDialog.askopenfilename()))
b_run = ttk.Button(mainframe,text = "Start Script", command = lambda: run_db_conversion(input_file.get())).grid(column=5, row=5, sticky=E)
b_in.grid_configure()
e_in.grid_configure()
root.mainloop()