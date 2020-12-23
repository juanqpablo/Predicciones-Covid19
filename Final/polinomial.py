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

# metodo que crea el modelo, lo ajusta a los datos y genera una prediccion de 
# acuerdo a los dias ingresados.
def modeloPred(list_dias, casos, grd=6, dias=10):
    #creacion del modelo
    x=np.array(list_dias).reshape(-1,1)
    polyFt=PolynomialFeatures(degree=grd)
    x=polyFt.fit_transform(x) #variable independiente: dias
    model=linear_model.LinearRegression()
    y=np.array(casos).reshape(-1,1) #variable dependiente: casos
    model.fit(x,y)

    #se crea la prediccion
    pred=round(int(model.predict(polyFt.fit_transform([[len(list_dias) + dias]]))),2)
    xpred=np.array(list(range(1,len(list_dias) + dias))).reshape(-1,1)
    ypred=model.predict(polyFt.fit_transform(xpred)) # prediccion
    return model,x,y,ypred # se retorna el modelo, x original, y original y el Y predecido.

#Leemos el csv
url = "./data/TotalesPorRegion.csv"
file = pd.read_csv(url, sep=',')
data = Datos_Region(file)

#se define titulo del Dashboard
st.title("Dashboard de predicción de Covid-19 Chile")

#se define titulo del sidebar
st.sidebar.title('Configuracion')

#opciones del selectbox para elegir los casos a analizar
opciones_casos=["Casos Confirmados", "Casos Fallecidos", "Casos Recuperados"]

#opciones del selectbox para elegir region
opciones_region=["Arica y Parinacota", "Tarapacá", "Antofagasta",
        "Atacama", "Coquimbo", "Valparaíso", "Metropolitana", "O’Higgins", "Maule",
        "Ñuble", "Biobío", "Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes"]


#Se guarda el grado con el que se desea graficar
grado = st.sidebar.slider('Grado', 1, 20, 6, step=1)

#Se guardan los dias de prediccion que se desea graficar
diasPredecido = st.sidebar.slider('Prediccion de dias', 1, 30, 10, step=1)

#Se guarda la region que se desea graficar
region = st.sidebar.selectbox('Eliga Region a Graficar:', opciones_region)

#Generamos dataframe
df = data.generate_dataframe(region, activos = True) #aca
#df= df.query('Casos_Confirmados > 0')
#print (df)

#del dataframa se obtienen los dias analizados del csv
dias = df.Dias.values

#Se guarda el tipo de caso con el que se desea graficar
tipo_casos = st.sidebar.selectbox('Eliga los datos a utlizar:', opciones_casos)

#Se define el tipo de caso
if (tipo_casos == "Casos Confirmados"):
    casos = df.Casos_Confirmados.values 
if(tipo_casos == "Casos Fallecidos"): 
    casos = df.Casos_Fallecidos.values  
if(tipo_casos == "Casos Recuperados"): 
    casos = df.Casos_Recuperados.values  


fig = plt.figure()
p, xfit, yfit, y1=modeloPred(dias, casos, grado, diasPredecido)
print(p.score(xfit,yfit)*100) 
y0=p.predict(xfit)
plt.plot(yfit,'-m', label='Datos Reales') # Datos reales
plt.plot(y1,'--r', label='Prediccion') # Prediccion
plt.plot(y0,'-b', label='Funcion del Modelo') # Funcion del modelo

#se agrega titulo, labels y legendas al grafico
fig.suptitle(f'Evolucion de {tipo_casos} en {region }')
plt.xlabel('Dias Trasncurridos')
plt.ylabel('Cantidad de Casos')
plt.legend(framealpha=1, frameon=True)


#Se añade barra de progreso visual
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
  latest_iteration.text(f'En proceso de grafica {i+1}%')
  bar.progress(i + 1)
  time.sleep(0.01)

#Se imprime en el dashboard la
st.write("Precision del Modelo: " + str(round(p.score(xfit,yfit)*100, 2)) +  "%")

#Se grafica el grafico
the_plot = st.pyplot(fig)







