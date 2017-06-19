# -*- coding: utf-8 -*-
import csv
import pandas as pd
import json
import pickle
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def compare_var(tab1, tab2, var):
    # assert max(tab1[var].value_counts()) == 1
    # assert max(tab2[var].value_counts()) == 1
    cond_1_in_2 = tab1[var].isin(tab2.IRIS)
    cond_2_in_1 = tab2[var].isin(tab1.IRIS)
    in_1_not_in_2 = tab1[var][~cond_1_in_2]
    in_2_not_in_1 = tab2[var][~cond_2_in_1]
    print("il y a " + str(len(in_1_not_in_2)) + " " + var + " dans 1 et pas dans 2")
    print("il y a " + str(len(in_2_not_in_1)) + " " + var + " dans 2 et pas dans 1")

print("Loading IRIS dataframe")
with open('../BIGBASE/iris_dataframe.pickle', 'rb') as dataframe_handle:
    iris_dataframe = pickle.load(dataframe_handle)
print(iris_dataframe.shape)

print("Loading INSEE CSV")
#insee_dataframe = pd.read_csv('../BIGBASE/insee_output.csv',sep=';',encoding='utf-8')
insee_restricted_dataframe = pd.read_csv('../BIGBASE/insee_income_df.csv',sep=';',encoding='utf-8')

print("IRIS size")
#iris_dataframe.columns = [u'DEPCOM', u'NOM_COM', u'IRIS', u'DCOMIRIS', u'NOM_IRIS', u'TYP_IRIS',u'ORIGINE', u'GEOMETRY']
iris_dataframe.columns = [u'DEPCOM', u'NOM_COM', u'SMALLIRIS', u'IRIS', u'NOM_IRIS', u'TYP_IRIS',u'ORIGINE', u'GEOMETRY']

print(iris_dataframe.shape)
print(iris_dataframe.head())

print("INSEE Data size")
print(insee_restricted_dataframe.shape)
print(insee_restricted_dataframe.head())

compare_var(iris_dataframe,insee_restricted_dataframe,"IRIS")
print("end of script")
print(iris_dataframe.shape)

insee_restricted_dataframe = insee_restricted_dataframe.merge(iris_dataframe,how='left',on='IRIS')

print("joined dataframe")
print(insee_restricted_dataframe.shape)

print("IRIS revenu data visualization")
with open('../BIGBASE/iris_revenu_dataviz.pickle', 'wb') as handle:
    pickle.dump(insee_restricted_dataframe, handle, protocol=pickle.HIGHEST_PROTOCOL)
