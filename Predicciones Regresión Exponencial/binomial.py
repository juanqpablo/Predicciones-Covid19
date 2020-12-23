# -*- coding: utf-8 -*-

from TotalesPorRegion.datos import Datos_Region
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import streamlit as st
import time


def modeloPred(list_dias, casos_Confirmados, grd=6, dias=10):
    x=np.array(list_dias).reshape(-1,1)
    polyFt=PolynomialFeatures(degree=grd)
    x=polyFt.fit_transform(x)
    model=linear_model.LinearRegression()

    y=np.array(casos_Confirmados).reshape(-1,1) #aca es

    model.fit(x,y)
    pred=round(int(model.predict(polyFt.fit_transform([[len(list_dias) + dias]]))),2)
    xpred=np.array(list(range(1,len(list_dias) + dias))).reshape(-1,1)
    ypred=model.predict(polyFt.fit_transform(xpred))
    return model,x,y,ypred

st.title("Dashboard de predicción de Covid-19 Chile")


url = "./data/producto3/TotalesPorRegion.csv"
file = pd.read_csv(url, sep=',')
data = Datos_Region(file)

regiones = data.all_region()

st.sidebar.title('Configuracion')

options2=["Casos Confirmados", "Casos Fallecidos", "Casos Recuperados"]


options=["Arica y Parinacota", "Tarapacá", "Antofagasta",
        "Atacama", "Coquimbo", "Valparaíso", "Metropolitana", "O’Higgins", "Maule",
        "Ñuble", "Biobío", "Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes"]



grado = st.sidebar.slider('Grado', 1, 20, step=1)
diasPredecido = st.sidebar.slider('Prediccion de dias', 1, 30, step=1)

plot_y = st.sidebar.selectbox('Eliga Region a Graficar:', options)


#Generamos dataframe
df = data.generate_dataframe(plot_y, activos = True) #aca
#df= df.query('Casos_Confirmados > 0')
print (df)
dias = df.Dias.values



tipo_casos = st.sidebar.selectbox('Eliga los datos a utlizar:', options2)

if (tipo_casos == "Casos Confirmados"):
    casos = df.Casos_Confirmados.values 

if(tipo_casos == "Casos Fallecidos"): 
    casos = df.Casos_Fallecidos.values  

if(tipo_casos == "Casos Recuperados"): 
    casos = df.Casos_Recuperados.values  



fig = plt.figure()

p, xfit, yfit, y1=modeloPred(dias, casos, grado, diasPredecido)
print(p.score(xfit,yfit)*100) #aca
y0=p.predict(xfit)
plt.plot(yfit,'-m', label='Datos Reales') # Datos reales
plt.plot(y1,'--r', label='Prediccion') # Prediccion
plt.plot(y0,'-b', label='Funcion del Modelo') # Funcion del modelo

fig.suptitle(f'Evolucion de {tipo_casos} en {plot_y }')
plt.xlabel('Dias Trasncurridos')
plt.ylabel('Cantidad de Casos')


plt.legend(framealpha=1, frameon=True)
#plt.show()

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'En proceso de grafica {i+1}%')
  bar.progress(i + 1)
  time.sleep(0.01)

st.write("Precision del Modelo: " + str(round(p.score(xfit,yfit)*100, 2)) +  "%")

the_plot = st.pyplot(fig)







