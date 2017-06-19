# -*- coding: utf-8 -*-

import csv
import pandas as pd
import json
import pickle
import sys

reload(sys)
sys.setdefaultencoding('utf8')

print("Loading pickled files")
print("Loading dictionary")
with open('../BIGBASE/insee_opendata_dictionary.pickle', 'rb') as dictionary_handle:
    insee_dictionary = pickle.load(dictionary_handle)
print(len(insee_dictionary))
# my_index = 0
# for key, value in insee_dictionary.iteritems():
#     print(my_index)
#     if my_index == 28 :
#         print("found")
#     print(key)
#     my_index=my_index+1
#     if key == unicode("REVENU PERSONNE@Médiane (€)"):
#         print("found")

PERSONNE=insee_dictionary[unicode("REVENU PERSONNE@Médiane (€)")]
UNITE_CONSO=insee_dictionary[unicode("REVENU PAR UNITE DE CONSOMMATION@Médiane (€)")]
MENAGE=insee_dictionary[unicode("REVENU MENAGE@Médiane (€)")]
GRETA=insee_dictionary["EQUIPEMENT SERVICE ENSEIGNEMENT SUPERIEUR INFRASTRUCTURE@GRETA"]

PERSONNE = PERSONNE.split("@")[-1]
MENAGE = MENAGE.split("@")[-1]
UNITE_CONSO = UNITE_CONSO.split("@")[-1]
GRETA = GRETA.split("@")[-1]

print("Loading INSEE CSV")
insee_dataframe = pd.read_csv('../BIGBASE/insee_output.csv',sep=';',encoding='utf-8')

print("Dictionary size")
print(len(insee_dictionary))
print("Data size")
print(insee_dataframe.shape)

print("Test column presence")
print(PERSONNE in insee_dataframe.columns)
print(MENAGE in insee_dataframe.columns)
print(UNITE_CONSO in insee_dataframe.columns)

print("displaying all columns")
for my_col in insee_dataframe.columns:
    print(my_col)
    # if "RFMQ211" in my_col:
    #     print("found")
    #     print(my_col)
    # if "B101" in my_col:
    #     print("found")
    #     print(my_col)

insee_restricted_dataframe = insee_dataframe[["IRIS","LIB_IRIS","COM","LIB_COM","REG","REG2016","DEP",PERSONNE,MENAGE,UNITE_CONSO]]
del insee_dataframe

print(insee_restricted_dataframe.shape)
print(insee_restricted_dataframe.head())

insee_restricted_dataframe.to_csv("../BIGBASE/insee_income_df.csv", sep=';', index=False, encoding='utf-8')

print(insee_restricted_dataframe.shape)
print("file saved")