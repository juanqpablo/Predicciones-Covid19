from TotalesPorRegion.datos import Datos_Region
import pandas as pd
from datetime import datetime
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
# -*- coding: utf-8 -*-

def regression(var_independiente, var_dependiente):
    #-------------------------------------------------------------------------------
    # Creamos el objeto de Regresión Linear
    #-------------------------------------------------------------------------------
    regr = linear_model.LinearRegression()
    X_train = var_independiente # Corresponden a los dias
    # Puede corresponder a (Casos Confirmados, Casos Fallecidos o Casos_Recuperados)
    y_train = np.log(var_dependiente)

    X_train = X_train.reshape(-1, 1)
    y_train = y_train.reshape(-1, 1)

    #---------------------------------------------------------------------------
    # Entrenamos nuestro modelo
    #---------------------------------------------------------------------------
    regr.fit(X_train, y_train )
    #---------------------------------------------------------------------------
    # Hacemos las predicciones
    #---------------------------------------------------------------------------
    y_pred = regr.predict(X_train)
    summary = summary_regression(regr, y_train, y_pred)
    return summary,X_train


def summary_regression(regresion, y_train, y_pred):
        summary = {}
        #-----------------------------------------------------------------------
        # Summary de la regresion exponencial
        #-----------------------------------------------------------------------
        # Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
        print('Coefficients: \n', regresion.coef_)
        # Este es el valor donde corta el eje Y (en X=0)
        print('Independent term: \n', regresion.intercept_)
        # Error Cuadrado Medio
        print("Mean squared error: %.2f" % mean_squared_error(y_train, y_pred))
        # Puntaje de Varianza. El mejor puntaje es un 1.0
        print('Variance score: %.2f' % r2_score(y_train, y_pred))
        summary = {
            "b": regresion.coef_,
            "a" : regresion.intercept_,
            "Mean_squared_error": mean_squared_error(y_train, y_pred),
            "Variance_score": r2_score(y_train, y_pred)
        }
        return summary

#-------------------------------------------------------------------------------
# Método que Grafica
#-------------------------------------------------------------------------------
def graficar(df, y0,name_region):
    area = 2 * 2**2
    datos_reales = plt.scatter(df.Dias.values,
                               df.Casos_Confirmados.values,
                               color="black", s= area, alpha=0.5,
                               label="Casos Confirmados Originales")

    #datos_predictivos = plt.plot(y0, "-g", label="Datos Predictivos")
    datos_predictivos2 = plt.plot(y0, "-r", label="Datos Predictivos")
    # Create another legend for the second line.
    plt.title("Análisis Predictivo")
    plt.suptitle(name_region)
    plt.xlabel('Días Transcurridos', size="16")
    plt.ylabel('Casos Confirmados',  size="16")
    plt.legend()
    plt.show()


#-------------------------------------------------------------------------------
#Carga del archivo
#-------------------------------------------------------------------------------
file = pd.read_csv("./data/producto3/TotalesPorRegion.csv")
data = Datos_Region(file)
regiones = data.all_region()
#Generamos dataframe
df = data.generate_dataframe(regiones[0], activos = True)

df= df.query('Casos_Confirmados > 0')
print(df)
# Se aplica la regresion llamando a la funcion regression_exp
json_summary, X_train = regression(df.Dias.values, df.Casos_Confirmados.values )
print (json_summary["a"] , json_summary["b"])

y0 = json_summary["a"] *  np.power(np.e,(json_summary["b"] * X_train))
graficar(df, y0, regiones[0])
