import pandas as pd
import math
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

#0-16 TotalAcumulado = Confirmados
#17-33 Totales nuevos por dia
#34-50 Casos nuevos con sintomas
#51-67 Casos nuevos sin sintomas
#68-84 Casos nuevos sin notificar
#85-101 Fallecidos totales
#102-118 Casos confirmados recuperados
#119-135 Casos activos confirmados

def get_data(file, list_days):
    list_data = []
    array_data = {}
    for row in range(85,101):
        region = file.iloc[row][0]
        data = []
        for col in list_days:
            if(math.isnan(file.iloc[row][col])):
                data.append(0)
            else:
                data.append(file.iloc[row][col])
        array_data[region] = data
    return array_data


list_col = list(file.columns.values)
list_col_head = file.columns.values[2:len(list_col)]


datos = get_data(file, list_col_head)
#print(datos)
listX = []

for i in range(0,len(list_col_head)):
    listX.append(i+1)

x=np.array(listX).reshape(-1,1)
y=np.array(datos['Atacama']).reshape(-1,1)
plt.plot(y,'-m')
#Atacama=16 ; Arica y Parinacota=8; Araucanía=7;Metropolitana=8
polyFt=PolynomialFeatures(degree=16)
x=polyFt.fit_transform(x)

model=linear_model.LinearRegression()
model.fit(x,y)
ajuste=model.score(x,y)
ajusteP=round(ajuste*100,3)
print('Porcentaje de Exactitud:'+ str(ajusteP)+'%')
y0=model.predict(x)
plt.plot(y0,'-b')

plt.show()
