from TotalesPorRegion.datos import Datos_Region
import pandas as pd
from datetime import datetime
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
#Carga del archivo
#-------------------------------------------------------------------------------
file = pd.read_csv("./data/producto3/TotalesPorRegion.csv")
data = Datos_Region(file)

#-------------------------------------------------------------------------------
#Se obtienen los datos necesarios
#-------------------------------------------------------------------------------
confirmados = data.confirmados_region("Arica y Parinacota")
muertos = data.muertos_region("Arica y Parinacota")
recuperados = data.recuperados_region("Arica y Parinacota")
fechas = data.get_fechas()
#-------------------------------------------------------------------------------
# Armando Data Frame
#-------------------------------------------------------------------------------
arica = {
    "Fecha": fechas,
    "Casos_Confirmados": confirmados,
    "Casos_Fallecidos" : muertos,
    "Casos_Recuperados": recuperados,
}
df_arica = pd.DataFrame(arica, columns = ["Fecha", "Casos_Confirmados", "Casos_Fallecidos","Casos_Recuperados"] )
df_arica = df_arica.fillna(0.01) #Se camian todos los valores NaN por 0
df_arica['Casos_Confirmados'][df_arica["Casos_Confirmados"] == 0] = 0.01
df_arica["Fecha"] = pd.to_datetime(df_arica['Fecha'], infer_datetime_format=True)
df_arica["Casos_Activos"] = df_arica.Casos_Confirmados - df_arica.Casos_Fallecidos - df_arica.Casos_Recuperados

df_arica = df_arica.assign(Dias=[i for i in range(len(fechas))]) # Se genera el campo Dias
print (df_arica)

#-------------------------------------------------------------------------------
# Creamos el objeto de Regresión Linear
#-------------------------------------------------------------------------------
regr = linear_model.LinearRegression()
X_train = df_arica.Dias.values
y_train = np.log(df_arica.Casos_Confirmados.values)

X_train = X_train.reshape(-1, 1)
y_train = y_train.reshape(-1, 1)
# Entrenamos nuestro modelo
regr.fit(X_train, y_train )

#-------------------------------------------------------------------------------
# Hacemos las predicciones que en definitiva una línea (en este caso, al ser 2D)
#-------------------------------------------------------------------------------
y_pred = regr.predict(X_train)

# Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
print('Coefficients: \n', regr.coef_)
# Este es el valor donde corta el eje Y (en X=0)
print('Independent term: \n', regr.intercept_)
# Error Cuadrado Medio
print("Mean squared error: %.2f" % mean_squared_error(y_train, y_pred))
# Puntaje de Varianza. El mejor puntaje es un 1.0
print('Variance score: %.2f' % r2_score(y_train, y_pred))

#y0 =  regr.coef_ *  (regr.intercept_* X_train)
y0 = regr.intercept_ *  np.power(np.e,(regr.coef_  * X_train))
area = 2 * 2**2
plt.scatter(df_arica.Dias.values, df_arica.Casos_Confirmados.values, color="black", s= area, alpha=0.5)
plt.plot(y0, "-b")
plt.show()
