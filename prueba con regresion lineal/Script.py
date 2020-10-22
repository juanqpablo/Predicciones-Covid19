import pandas as pd
#from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
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
listX = []
#print(datos)
for i in range(0,len(list_col_head)):
    listX.append(i+1)
    #print(listX)
#print(listX)
x=np.array(listX).reshape(-1,1)
y=np.array(datos['Metropolitana']).reshape(-1,1)
plt.plot(y,'-m')
#16
polyFt=PolynomialFeatures(degree=8)
x=polyFt.fit_transform(x)
#print(x)
model=linear_model.LinearRegression()
model.fit(x,y)
ajuste=model.score(x,y)
ajusteP=round(ajuste*100,3)
print('Porcentaje de Exactitud:'+ str(ajusteP)+'%')
y0=model.predict(x)
plt.plot(y0,'-b')


plt.show()
