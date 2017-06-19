# -*- coding: utf-8 -*-

import csv
import pandas as pd
import json
import pickle
import sys
import caf_opendata_dictionnary_mapping

reload(sys)
sys.setdefaultencoding('utf8')

caf_open_dictionnary=caf_opendata_dictionnary_mapping.caf_open_dictionnary

print("Loading dictionary")

print("Dictionary size")
print(len(caf_open_dictionnary))


my_index = 0
for key, value in caf_open_dictionnary.iteritems():
    my_index=my_index+1
    if key == unicode("NOMBRE TOTAL DE FOYERS ALLOCATAIRES RSA"):
        print("found")
        print(key)
    if key == unicode("NB_allocataire_RSA"):
        print("found")
        print(key)

RSA_TOT_KEY=unicode("NB_allocataire_RSA")
RSA_TOT=caf_open_dictionnary[RSA_TOT_KEY]

print("Loading CAF CSV")
caf_dataframe = pd.read_csv('../BIGBASE/caf_data.csv',sep=',',encoding='utf-8')

print("Data size")
print(caf_dataframe.shape)

print("Test column presence")

print("displaying all columns")
column_list = []
for my_col in caf_dataframe.columns:
    if RSA_TOT in my_col:
         print("found")
         print(my_col)
         column_list.append(my_col)
    if RSA_TOT_KEY in my_col:
         print("found")
         print(my_col)
         column_list.append(my_col)


# staple_columns = \
# [u'Code INSEE',
# u'Code Postal',
# u'Commune',
# u'Département',
# u'Région',
# u'Statut',
# u'Altitude Moyenne',
# u'Superficie',
# u'Population',
# u'geo_point_2d',
# u'geo_shape',
# u'ID Geofla',
# u'Code Commune',
# u'Code Canton',
# u'Code Arrondissement',
# u'Code Département',
# u'Code Région']

staple_columns = \
[u'Codes_Insee',
u'Code_Postal',
u'Commune',
u'Departement',
u'Region',
u'Statut',
u'Altitude_Moyenne',
u'Superficie',
u'Population',
u'geo_shape',
u'ID_Geogla',
u'Code_Commune',
u'Code_Canton',
u'Code_Arrondissement',
u'Code_Departement',
u'Code_Region',
u'lat',
u'lon']

all_columns = staple_columns + column_list
for my_col in caf_dataframe.columns:
    if my_col not in all_columns:
        print("trouble")
cat_restricted_dataframe = caf_dataframe[all_columns]
del caf_dataframe

print(cat_restricted_dataframe.shape)
print(cat_restricted_dataframe.head())

print("saving cleaned file")
cat_restricted_dataframe.to_csv("../BIGBASE/caf_rsa_df.csv", sep=';', index=False, encoding='utf-8')

print(cat_restricted_dataframe.shape)
print("file saved")
print(cat_restricted_dataframe.columns)
