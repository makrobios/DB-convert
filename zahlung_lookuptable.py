#!/usr/bin/python
# -*- coding: iso-8859-14 -*-

'''TODO=> strip title from names (Dr., Univ.Prof, Ing...)'''
file = open('/home/ch/filemaker/kartei_23_11_2016/export/kartei-SNR-NAME-VN-PLZ.csv',encoding='iso-8859-14')


class Tree(dict):
    '''autovivification of dictionaries by 
    subclassing dict and overriding __missing__ method '''
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

names = Tree()
for line in file:
      snr,name,vn,plz = line.split(',')[:-1] 
      names[name][vn] = snr
    
zahlungen_file = open('/home/ch/filemaker/zahlungen/out.file','r',encoding='iso-8859-14')

for line in zahlungen_file:
    print(line)
    if line.startswith('Name :'):
        try:
            name_1 = line.lstrip('Name :').split(' ')[0]
            name_2 = line.lstrip('Name :').split(' ')[1]
            print('{} {}\n'.format(name_1, name_2))
            print('{} {}\n'.format(names[name_1], names[name_2]))
        except:
            print('Error at {}: '.format(line)) 
