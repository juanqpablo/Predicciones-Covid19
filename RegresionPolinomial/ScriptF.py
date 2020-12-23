#Atacama=16 ; Arica y Parinacota=8; Araucanía=7;Metropolitana=8
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
    for row in range(0,16):
        region = file.iloc[row][0]
        data = []
        for col in list_days:
            if(math.isnan(file.iloc[row][col])):
                data.append(0)
            else:
                data.append(file.iloc[row][col])
        array_data[region] = data
    return array_data

def modeloPred(datos,region,list_x,grd=6,dias=10):
    x=np.array(list_x).reshape(-1,1)
    polyFt=PolynomialFeatures(degree=grd)
    x=polyFt.fit_transform(x)
    model=linear_model.LinearRegression()
    y=np.array(datos[region]).reshape(-1,1)
    model.fit(x,y)
    pred=round(int(model.predict(polyFt.fit_transform([[len(list_x)+dias]]))),2)
    xpred=np.array(list(range(1,len(list_x)+dias))).reshape(-1,1)
    ypred=model.predict(polyFt.fit_transform(xpred))
    return model,x,y,ypred

# def prediccion(modelo,listX,dias=10):
#     polyFt=PolynomialFeatures(degree=grd)
#     pred=round(int(modelo.predict(polyFt.fit_transform([[len(listX)+dias]]))),2)
#     xpred=np.array(list(range(1,len(listX)+dias))).reshape(-1,1)
#     ypred=model.predict(polyFt.fit_transform(xpred))
#     return ypred

url = "./TotalesPorRegion.csv"
file = pd.read_csv(url, sep=',')

list_col = list(file.columns.values)
list_col_head = file.columns.values[2:len(list_col)]

datos = get_data(file, list_col_head)

listX = []
for i in range(0,len(list_col_head)):
    listX.append(i+1)

p,xfit,yfit,y1=modeloPred(datos,'Araucanía',listX)
print(p.score(xfit,yfit)*100)
y0=p.predict(xfit)
plt.plot(yfit,'-m')
plt.plot(y1,'--r')
plt.plot(y0,'-b')
plt.show()


# x=np.array(listX).reshape(-1,1)
# grd=6
# polyFt=PolynomialFeatures(degree=grd)
# x=polyFt.fit_transform(x)
# model=linear_model.LinearRegression()
# y=np.array(datos['Araucanía']).reshape(-1,1)
# model.fit(x,y)
# ajuste=model.score(x,y)
# ajusteP=round(ajuste*100,3)
# print('Porcentaje de Exactitud:'+ str(ajusteP)+'%')
# y0=model.predict(x)
# plt.plot(y,'-m')
#
# dias=10
# pred=round(int(model.predict(polyFt.fit_transform([[len(list_col_head)+dias]]))),2)
# print("prediccion: "+str(pred))
# xpred=np.array(list(range(1,len(list_col_head)+dias))).reshape(-1,1)
# ypred=model.predict(polyFt.fit_transform(xpred))
# plt.plot(ypred,'--r')
# plt.plot(y0,'-b')
# plt.show()
