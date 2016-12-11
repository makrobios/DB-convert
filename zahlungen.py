# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

'''TODO=> How to handle identical names??'''
'''TODO=> strip title from names (Dr., Univ.Prof, Ing...)'''


import pandas as pd
import datetime
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

file = open('/home/ch/filemaker/zahlungen/csv_daten_komplett.csv',encoding='windows-1252')
    
headers = ['argus_iban','text','datum','datum2','betrag','eur']
df = pd.read_csv(file,
                 sep=';',
                 header=None,
                 names=headers,
                 index_col=False,
                 dtype = {'datum':datetime.date},
                 encoding = 'utf-8')
    
df.datum = pd.to_datetime(df.datum,dayfirst=True)
df = df[df.datum > '2015-01-01']  ### get only 2 years of data for testing
df.text.replace('[A-Z]{2}/\d{9}.+[A-Z]{2}\d{4,}\s',r'|',inplace=True,regex=True)
                 
    
################# create lookup table from Kartei  ####################

kartei = {}
file = open('/home/ch/filemaker/kartei_23_11_2016/export/kartei-SNR-NAME-VN-PLZ.csv',encoding='iso-8859-14')
header = file.readline()
for line in file:
    snr = line.split(',')[0]
    vn = line.split(',')[2]
    name = line.split(',')[1]
    gesamt = vn + ' ' + name
    try: 
        kartei[gesamt].append(snr)
    except:
        kartei[gesamt] = [snr]


#####################  match name from zahlungen with entry in Kartei #######
''' was passiert bei Namen mit scharfes ß ???? => kein Problem '''

#misslist = []
#hitlist = []
zdf = pd.DataFrame(columns=['datum','betragEur','text','belnr','beitrag spende','Text Spende'])

#testset = names[:100]
for index,row in df.iterrows():
     if '|' in row.text:
        text, name = row.text.split('|')
     else:
         name = row.text
     extracted = process.extractOne(name,kartei.keys(), scorer=fuzz.token_set_ratio)
     if extracted[1] > 90:    
        snr = kartei[extracted[0]]
        datum = row.datum.strftime('%d.%m.%Y')
        beleg = row.datum.strftime('%y%m%d')
        zseries = pd.Series({'datum': datum,'betragEur' : row.betrag,'text': row.text,'belnr':beleg,'snr':','.join(snr)},name = index)
        zdf = zdf.append(zseries)
        print(index,name)
#        hitlist.append([extracted,name,snr])
#        print('''{0};{1};{2};{3}'''.format(row.datum.strftime('%d.%m.%Y'),
#                                   row.betrag,
#                                   name,
#                                   ','.join(snr))  ) 
#     else:
#        misslist.append([extracted,name])


#auszug = list(new_df['text'])

#names = []
#element_mod = []
#for element in auszug:
#    element = re.sub('[A-Z]{2}/\d{9}.+[A-Z]{2}\d{4,}\s',r'|',element) 
#    element_mod.append(element)
#    try:    
#        names.append(element.split('|')[1])
#    except:
#        names.append(element)



###################    remove titles    #######################
#titel = []
#file = open('titel.mer', encoding='windows-1250')
#for line in file:
#    titel.append(line.strip())
#result = list( filter(lambda x: not re.findall(r'""',x),titel) )
#titel = set(result)
#titel = list(map((lambda x: re.sub(r'"','',x)),titel))
#titel.remove('.')
   

#from fuzzywuzzy import process
#from fuzzywuzzy import fuzz
#match=0
#for zahlungsname in df.Name:
#    for karteiname in kartei:
#        if not i % 10000:
#            print(i)
#        new_match = fuzz.partial_token_set_ratio(zahlungsname, karteiname)
#        if new_match > match:
#            highestmatch = " ".join([karteiname,zahlungsname,str(match)])
#        match = new_match
##        if match > 90:
##            print('******** Zahlungsname: {} Karteiname: {} ******* Match: {}'.format(zahlungsname, karteiname, match,"\n"))
##        i += 1
#print(highestmatch)
#
#
#for zahlungsname in df.Name:
#    extracted = process.extractOne(zahlungsname, kartei.keys())
#    hitlist[zahlungsname] = [extracted,kartei[(extracted[0])]]