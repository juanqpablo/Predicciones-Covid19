# # -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import math
#from pymongo import MongoClient
import numpy as np
# import matplotlib
# matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

#import time


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


options=["Arica y Parinacota", "Tarapacá", "Antofagasta",
             "Atacama", "Coquimbo", "Valparaíso", "Metropolitana", "O’Higgins", "Maule",
             "Ñuble", "Biobío", "Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes"]

plot_y = st.sidebar.selectbox('Eliga Region a Graficar:', options)

x=np.array(listX).reshape(-1,1)
#y=np.array(datos['Atacama']).reshape(-1,1)
y=np.array(datos[plot_y]).reshape(-1,1)

fig = plt.figure()
# ax = fig.add_subplot(111)
# line, = ax.plot(x, y)

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
#plt.show()

#Codigo StreamLit
st.write("""
# Cagaste JP!, a presentar se ha dicho xD
""")

# region = st.sidebar.selectbox(
#     label="Elegir region",
#     options=["Arica y Parinacota,", "Tarapacá", "Antofagasta",
#              "Atacama", "Coquimbo", "Valparaíso", "Metropolitana", "O’Higgins", "Maule"
#              "Ñuble", "Biobío", "Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes"],
#     index=0,
# )



the_plot = st.pyplot(fig)

# def init():  # give a clean slate to start
#     line.set_ydata([np.nan] * len(x))
    

# def animate(i):  # update the y values (every 1000ms)
#     #line.set_ydata(np.array(datos['Los Ríos']).reshape(-1,1))
    
#     the_plot.pyplot(plt)

# init()
# for i in range(100):
#     animate(i)
#     time.sleep(0.1)
    




