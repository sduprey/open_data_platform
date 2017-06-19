import csv
import pandas as pd
import json
import pickle

with open('../BIGBASE/insee_opendata_dictionary.pickle', 'rb') as handle:
    insee_dictionary = pickle.load(handle)

print(len(insee_dictionary))

iris_path = "../BIGBASE/iris.json"
iris_data = None
with open(iris_path) as json_data:
    iris_data = json.load(json_data)

# print(iris_data.__class__.__name__)
# print(type(iris_data))
# print(len(iris_data))
#
# for key, value in iris_data.iteritems():
#     print("@@@@@@key")
#     print(key)
#     print("@@@@@@value")
#     print(value.__class__.__name__)
#     print(type(value))
#     print(len(value))

iris_features = iris_data["features"]
print(type(iris_features))
print(len(iris_features))

iris_df = pd.DataFrame(index=range(len(iris_features)),columns=["DEPCOM","NOM_COM","IRIS","DCOMIRIS","NOM_IRIS","TYP_IRIS","ORIGINE","GEOMETRY"])
row_index = 0
for iris_feature in iris_features:
    print("Row index")
    print(row_index)
    properties = iris_feature["properties"]
    geometry = iris_feature["geometry"]
    print("IRIS done")
    DEPCOM = properties["DEPCOM"]
    NOM_COM = properties["NOM_COM"]
    IRIS = properties["IRIS"]
    DCOMIRIS = properties["DCOMIRIS"]
    NOM_IRIS = properties["NOM_IRIS"]
    TYP_IRIS = properties["TYP_IRIS"]
    ORIGINE = properties["ORIGINE"]
    iris_df.iloc[row_index] = pd.Series({'DEPCOM':DEPCOM, 'NOM_COM':NOM_COM, 'IRIS':IRIS, 'DCOMIRIS':DCOMIRIS ,'NOM_IRIS':NOM_IRIS, 'TYP_IRIS':TYP_IRIS, 'ORIGINE':ORIGINE, 'GEOMETRY':geometry})
    row_index=row_index+1
    # print(type(iris_feature))
    # print(len(iris_feature))
    # for key, value in iris_feature.iteritems():
    #     print("@@@@@@key")
    #     print(key)
    #     print("@@@@@@value")
    #     print(value.__class__.__name__)
    #     print(type(value))
    #     print(len(value))

filehandler = open("../BIGBASE/iris_dataframe.pickle","wb")
pickle.dump(iris_df,filehandler)
print("file saved")