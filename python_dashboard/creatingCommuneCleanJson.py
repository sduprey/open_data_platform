# -*- coding: utf-8 -*-
import csv
import pandas as pd
import json
import pickle
import sys

reload(sys)
sys.setdefaultencoding('utf8')

print("just getting a sense of the incoming structure")
iris_path = "../BIGBASE/iris_clean.json"
iris_data = None
with open(iris_path) as json_data:
    iris_data = json.load(json_data)

commune_df = pd.read_csv('../BIGBASE/commune_insee.csv', sep=';', encoding='utf-8')
print(commune_df.shape)
print(commune_df.head())

print("Mimicking previous structure")
commune_data = {}
commune_data[u"type"] = u"FeatureCollection"

commune_features = []
limit=50
for index, row in commune_df.iterrows():
    if index <= limit :
        properties = {}
        properties[u'Code INSEE'] = row[u'Code INSEE']
        properties[u'Code Postal'] = row[u'Code Postal']
        properties[u'Commune'] = row[u'Commune']
        properties[u'Département'] = row[u'Département']
        properties[u'Région'] = row[u'Région']
        properties[u'Statut'] = row[u'Statut']
        properties[u'Altitude Moyenne'] = row[u'Altitude Moyenne']
        properties[u'Superficie'] = row[u'Superficie']
        properties[u'Population'] = row[u'Population']
        properties[u'geo_point_2d'] = row[u'geo_point_2d']
    #    properties[u'geo_shape'] = row[u'geo_shape']
        properties[u'ID Geofla'] = row[u'ID Geofla']
        properties[u'Code Commune'] = row[u'Code Commune']
        properties[u'Code Canton'] = row[u'Code Canton']
        properties[u'Code Arrondissement'] = row[u'Code Arrondissement']
        properties[u'Code Département'] = row[u'Code Département']
        properties[u'Code Région'] = row[u'Code Région']

    #    geometry = json.load(row[u'geo_shape'])
        geometry = json.loads(row[u'geo_shape'])

        commune_dictionary = {}
        commune_dictionary[u"geometry"]=geometry
        commune_dictionary[u"properties"]=properties
        commune_dictionary[u"type"]=u"Feature"
        commune_features.append(commune_dictionary)

commune_data[u'features'] = commune_features

print("writing file")
commune_path = "../BIGBASE/commune_clean.json"
# with open(commune_path, 'w') as outfile:
#     json.dump(commune_data, outfile)

import io, json
with io.open(commune_path, 'w', encoding='utf-8') as f:
  f.write(json.dumps(commune_data, ensure_ascii=False))

print('this is done')