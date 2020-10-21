import pandas as pd
from pymongo import MongoClient
#-------------------------------------------------------------------------------
# VAriables
#-------------------------------------------------------------------------------
url = "./data/producto3/TotalesPorRegion.csv"
file = pd.read_csv(url, sep=',')

def get_data(file, list_days):
    list_data = []
    array_data = {}
    for row in range(17,33):
        region = file.iloc[row][0]
        data = []
        for col in list_days:
            data.append(file.iloc[row][col])
        array_data[region] = data
    return array_data


list_col = list(file.columns.values)
list_col_head = file.columns.values[2:len(list_col)]

datos = get_data(file, list_col_head)

print(datos)
