# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 22:57:21 2016

@author: ch
"""

# import math
# import numpy as np
import pandas as pd
from datetime import datetime
import re
# Documentation for df.replace
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.df.replace.html
''' ToDo: Kinder aufsplitten auf mehrere Reihen -> Problem mit umlauten ! --> done
          Anschlußmitglieder, 
                     einzieher betrag aufsplitten 
                     kein DE --> done
          Mitgliedskategorien --> done
          Beitrittsdatum --> done
          SEPA  --> done
          Export für Serienbrief
'''

kinder = {}
header = []
headerfile = open('c:/Users/ch/radfahren/filemaker/input/radlobby_header.txt', 'rb')
header = headerfile.readline().split(',')
headerfile.close()
"""set skiprow to remove first three lines,
set header to zero to use own header through names
set dtype to str for telefonnumbers"""

infile = 'c:/Users/ch/radfahren/filemaker/input/mitglied_in_ihrem_bundesland_werden.csv'
outfile = 'c:/Users/ch/radfahren/filemaker/output/Argusimport'

df = pd.read_csv(infile,
                 sep=';',
                 skiprows=3, header=None, names=header,
                 index_col=False,
                 dtype={'mobil': str},
                 encoding='utf-8')
# format mobil number, split into predial and number
# and add new column for predial

# Anschlußmitglieder
for row in df.index:
    Name = ''
    VN = ''
    gebdatum = ''
    email = ''
    anschluss = df.Notizen.ix[row]
    if pd.notnull(anschluss):
        series_index = df.shape[0] + 1
        series = df.ix[row]     # copy row of Hauptmitglied
        series = series.rename(index=series_index)
        series = series.drop(['kinder_bis', 'kinder_bis_19'])
        series.ix['Mitgliedskategorien'] = 2
        series.ix['keinDE'] = 1
        data = re.split(',|;', anschluss)
        series['Hauptmitglied'] = series.ix['VN'] + ' ' + series.ix['NAME']
        gesamtname = re.search(ur'[A-Za-zäüöß\-]+\s[A-Za-zäüöß\-]+', anschluss)
        VN = gesamtname.group(0).split(' ')[0]
        NAME = gesamtname.group(0).split(' ')[1]
        gebdatum = re.search('[\d+\.]+|\d+', anschluss)
        email = re.search('\w+\@[\w.]+', anschluss)
        if NAME:
            series.loc['NAME'] = NAME
        if VN:
            series.loc['VN'] = VN
        if gebdatum:
            series.loc['Gebdatum'] = gebdatum.group(0)
        if email:
            series.loc['EMAIL'] = email.group(0)
        df = df.append(series)


mobil = df.mobil.tolist()
row_vorwahl = []
row_nummer = []
pattern = ['\s+', '^0043', '^\+43', '^43', '^0', '[^\d]']
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
# df.VN = df.VN.str.title()
# df.NAME = df.NAME.str.title()

# add columns for up to seven children + birthday
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
        date = re.findall('\d+\.\d+\.\d+|\d+', kind)
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

# Add SNR Number for testing
# df['SNR'] = range(50000, 50000+int(len(df.index)))
# set Anrede to (Herr, Frau, Firma, sonstiges)
df.replace(u'männlich', u'Herr', inplace=True)
df.replace(u'weiblich', u'Frau', inplace=True)

# Beitritt Datum, Herkunft
df.Beitritt.replace('\s-\s\d+:\d+', '', regex=True, inplace=True)
df['Herkunft'] = 'radlobby.at'

# Set entries to Mitglied and Mitgliedkategorie normal
# df['Mitgliedskategorien'] = 1
# 1 = normal, 2= Anschluss, 3= Student, 4= Juniormitglied , 5= Fördermitglied
# 6 = Gratis-Mitgliedschaft, 7= Sozialtarif
df['Mitglied'] = 1

df.Mitgliedskategorien.replace('Vollmitglied', 1, inplace=True)
df.Mitgliedskategorien.replace('Haushaltsmitglied', 2, inplace=True)
df.Mitgliedskategorien.replace('StudentIn (bis 26 Jahre)', 3, inplace=True)
df.Mitgliedskategorien.replace('Junior (bis 18 Jahre)', 4, inplace=True)
df.Mitgliedskategorien.replace('Fördermitglied', 5, inplace=True)

# SEPA
df['einzieher_check'].replace('X', 'einzieher', inplace=True)

for index, einzieher in zip(df.einzieher_check.index, df.einzieher_check):
    if (einzieher == 'einzieher'):
        df.ix[index, 'EinzNotizen'] = datetime.strftime(datetime.now(), '%B')
        if df.anschlussmembers.ix[index] < 1:
            df.ix[index, 'einzbeitrag2015'] = str(df.ix[index, 'summe']).replace('.', ',')

df.Notizen = df.Notizen + ";" + df.summe.map(str)
# Writing to csv file, for import to filemaker 5 it has to be named .mer and
# use ";" as seperator
timestamp = datetime.strftime(datetime.now(), '%Y%m%d_%H_%M')
df.to_csv(outfile + '_' + timestamp + '.mer',
       sep=";",
       index=False,
       encoding='windows-1252',
       columns=['SNR', 'Mitglied', 'Mitgliedskategorien', 'VN', 'NAME', 'Anrede',
                'STRASSE', 'PLZ', 'ORT', 'vorwahltelmobil', 'mobil',
                'EMAIL', 'GEBDATUM', 'iban15', 'bic15', 'einzieher_check',
                'kind1', 'kind1_dat', 'kind2', 'kind2_dat', 'kind3',
                'kind3_dat', 'kind4', 'kind4_dat', 'kind5', 'kind5_dat',
                'moremembers', 'summe', 'einzbeitrag2015', 'EinzNotizen', 'Beitritt', 
                'Herkunft', 'Notizen', 'keinDE'])
