# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''TODO=> why are some beitrag missing ??'''

import pandas as pd
import re
import glob
import os 
import datetime

datum = ''
Auszug = ''
count = 1
count_missing_betrag = 0
df = pd.DataFrame()

#for root,dirs,files in os.walk("/home/ch/filemaker/zahlungen"):
file = '/home/ch/filemaker/zahlungen/dezember_zahlungen.txt'#[x for x in files if x.endswith('.txt')]
#for file in files:
text= open(file) #(os.path.join(root,file), 'r')
elements = text.readline()
Auszug = re.search('KONTOAUSZUG\d+',elements).group(0)
datum = re.search('Blatt\d+von\d+vom(\d{2}\.\d{2}\.\d{4})', elements).group(1)
elements = re.sub('^.*?\*{13}','',elements)      # remove start of string
elements= re.split('\*+', elements)#[1:]                 # split on '********'

for i in elements:
    print("##### {} #####\n".format(i))
    m_betrag = re.search('^([+-]?[\d\.]+,\d+)',i)
    m_iban = re.search('(\w\w\d+)\.',i)  
    m_name = re.search('(?:[A-Z]{2}\d+\.\d\d)(.*)006\d+\+',i)
    if not m_name:
        m_name = re.search('(Test)(.*)','Test Unbekannt')
#            if m_betrag:
#                print('betrag: ',m_betrag.group(0))
    if not m_betrag:
        print ('=====>betrag:{} == {} name: {}'.format(file, i,m_name.group(1)))
        count_missing_betrag += 1
        continue
   
#            print ('Name :', m_name.group(1))
#            print ('Datum:',datum)
#            print ('Auszug: ', Auszug,'position: ',count,'\n')
#            print ('Iban04: ',m_iban.group(0)[:-3])
#        
            
    serie = pd.Series((m_name.group(1),m_iban.group(0)[:-3],m_betrag.group(0),datum,Auszug,i), 
                          index=('Name','iban','betrag','Datum','Auszug','Eintrag'),name=count)
        
    df = df.append(serie)
    count = count + 1
    
class Tree(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

kartei = Tree()
not_in_kartei = []
file = open('/home/ch/filemaker/SNR_complete.csv', encoding='cp437')
for mitglied in file:
    vorname = mitglied.lower().strip().split(',')[0]
    nachname = mitglied.lower().strip().split(',')[1]
    snr = mitglied.strip().split(',')[-1]
    gesamtname = vorname + ' ' + nachname
    kartei[gesamtname] = snr

    
#for name in df.Name:
#   elements = name.lower().strip().split()
#   for element in elements:
#           for firstname in elements:
#               print("element: {}, firstname: {}, kartei: {}".format(element,firstname, kartei[element]))
#       




##### Test making names an object with property vorname or nachname#####
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
match=0
for zahlungsname in df.Name:
    for karteiname in kartei:
        if not i % 10000:
            print(i)
        new_match = fuzz.partial_token_set_ratio(zahlungsname, karteiname)
        if new_match > match:
            highestmatch = " ".join([karteiname,zahlungsname,str(match)])
        match = new_match
#        if match > 90:
#            print('******** Zahlungsname: {} Karteiname: {} ******* Match: {}'.format(zahlungsname, karteiname, match,"\n"))
#        i += 1
print(highestmatch)


for zahlungsname in df.Name:
    extracted = process.extractOne(zahlungsname, kartei.keys())
    hitlist[zahlungsname] = [extracted,kartei[(extracted[0])]]


#class Name:
#    def vorname(self, name):
#        vorname = True
#        return vorname
#    def nachname(self, name):
#        nachname = True
#        return nachname
#
#for name in df.Name:
#       test = fuzz.ratio('Mayerhofer',name)
#       if test > 90:
#           print( name, test)
