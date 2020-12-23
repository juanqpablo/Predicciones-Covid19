from TotalesPorRegion.datos import Datos_Region
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import streamlit as st
import altair as alt

@st.cache
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

def modeloPred(list_dias, casos_Confirmados, grd=6, dias=10):
    x=np.array(list_dias).reshape(-1,1)
    polyFt=PolynomialFeatures(degree=grd)
    x=polyFt.fit_transform(x)
    model=linear_model.LinearRegression()
    y=np.array(casos_Confirmados).reshape(-1,1)
    model.fit(x,y)
    pred=round(int(model.predict(polyFt.fit_transform([[len(list_dias) + dias]]))),2)
    xpred=np.array(list(range(1,len(list_dias) + dias))).reshape(-1,1)
    ypred=model.predict(polyFt.fit_transform(xpred))
    return model,x,y,ypred



url = "./data/producto3/TotalesPorRegion.csv"
file = pd.read_csv(url, sep=',')
data = Datos_Region(file)

regiones = data.all_region()



#Generamos dataframe
df = data.generate_dataframe(regiones[0], activos = True)
#df= df.query('Casos_Confirmados > 0')
print (df)
dias = df.Dias.values
casos_Confirmados = df.Casos_Fallecidos.values

#print(df.Dias.values)

p, xfit, yfit, y1=modeloPred(dias, casos_Confirmados)
print(p.score(xfit,yfit)*100)
y0=p.predict(xfit)
plt.plot(yfit,'-m')
plt.plot(y1,'--r')
plt.plot(y0,'-b')
plt.show()
