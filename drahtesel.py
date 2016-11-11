# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy
import os


def drahtesel_reformat(file):
    header = "SNR;Date Submitted;Titel;VN;NAME;STRASSE;PLZ;ORT;mobil;email;\
         Anrede;Gebdatum;Herkunft;Mitglied;Notizen;\
         Nichtmigliedskategorien;NummerProbeabo"

    df = pd.read_csv(file,
                     sep=';',
                     header = None,
                     names = header,
                     )
    return df

for root,dirs,files in os.walk("C:/Users/Adressverwaltung/Downloads/Anhänge/"):
    for file in files:
        df = df.append(read_csv(os.path.join(root, file)))
        