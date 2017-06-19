import os
import folium
import pickle

import json
import pandas as pd
import branca.colormap as cm
from collections import defaultdict


print(folium.__version__)

#us_states = os.path.join('..\\example\\data', 'us-states.json')
#US_Unemployment_Oct2012 = os.path.join('..\\example\\data', 'US_Unemployment_Oct2012.csv')

fr_iris = "../BIGBASE/commune.json"

print("loading JSON data")
geo_json_data = json.load(open(fr_iris))

print("loading COMMUNE data")
rsa_caf = pd.read_csv("../BIGBASE/caf_rsa_df.csv", sep=';',encoding='utf-8')

#commune_insee = pd.merge(commune_insee, df_temp, how='left', on='Codes_Insee')
print("we join on Codes_Insee")
rsa_caf = rsa_caf[["Codes_Insee","NB_allocataire_RSA_2015"]]
rsa_caf.columns = ["Codes_Insee","RAS_ALLOCATAIRES"]
print(rsa_caf.shape)

print(rsa_caf[["RAS_ALLOCATAIRES"]].min())
print(rsa_caf[["RAS_ALLOCATAIRES"]].max())

fr_rsa_dict = defaultdict(lambda: 0)

for index, row in rsa_caf.iterrows():
    fr_rsa_dict[row["Codes_Insee"]]=row["RAS_ALLOCATAIRES"]

def my_color_function(feature):
    """Maps low values to green and hugh values to red."""
    if fr_rsa_dict[feature['properties']['Code INSEE']] > 15000:
        return '#ff0000'
    else:
        return '#008000'


m = folium.Map([48.8566, 2.3522], tiles='cartodbpositron', zoom_start=4)

folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
        'fillColor':  my_color_function(feature),
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    }
).add_to(m)

m.save(os.path.join('results', 'Colormaps_2.html'))

m

#
# def my_color_function(feature):
#     """Maps low values to green and hugh values to red."""
#     if unemployment_dict[feature['id']] > 6.5:
#         return '#ff0000'
#     else:
#         return '#008000'
#
# m = folium.Map([43, -100], tiles='cartodbpositron', zoom_start=4)
#
# folium.GeoJson(
#     geo_json_data,
#     style_function=lambda feature: {
#         'fillColor': my_color_function(feature),
#         'color': 'black',
#         'weight': 2,
#         'dashArray': '5, 5'
#     }
# ).add_to(m)
#
# m.save(os.path.join('results', 'Colormaps_0.html'))
#
# m