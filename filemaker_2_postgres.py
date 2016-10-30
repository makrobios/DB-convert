# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 18:33:51 2016

@author: ch
"""

from sqlalchemy import create_engine
import pandas as pd
import psycopg2

engine = create_engine('postgresql://postgres:dbconvert@localhost/argus')
df = pd.read_csv('C:/Users/ch/radfahren/filemaker/output/db-import_20161025_21_10.mer ',sep=';', encoding = 'windows-1250')
df.to_sql('ArgusAdressen', engine)