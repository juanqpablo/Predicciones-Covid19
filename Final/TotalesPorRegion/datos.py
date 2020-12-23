# -*- coding: utf-8 -*-
import pandas as pd

"""
RANGOS de datos :
    - 0-16 TotalAcumulado = Confirmados
    - 17-33 Totales nuevos por dia
    - 34-50 Casos nuevos con sintomas
    - 51-67 Casos nuevos sin sintomas
    - 68-84 Casos nuevos sin notificar
    - 85-101 Fallecidos totales
    - 102-118 Casos confirmados recuperados
    - 119-135 Casos activos confirmados
"""
"""
Confirmados por Región: Corresponden a los datos acomulados del archivo que recibe
Muertos por Región: Corresponden a los datos de las personas Fallecidas por región
"""
class Datos_Region:

    def __init__(self, file):
        #-------------------------------------------------------------------------------
        # Dataset
        #-------------------------------------------------------------------------------
        self.data_frame_original = file
        self.data_frame_original.head(10)

        #-------------------------------------------------------------------------------
        #Obtengo la Traspuesta del dataframe
        #-------------------------------------------------------------------------------
        self.data_trasposed = self.data_frame_original.T
        self.largo = len(self.data_trasposed[0])
        #print(largo)

        #Obtenemos los datos necesarios: de Casos Confirmados, Casos Muertos y casos Recuperados
        self.df_confirmados = self.data_trasposed.iloc[2:self.largo, 0:16]
        self.df_muertos = self.data_trasposed.iloc[2:self.largo, 85:101]
        self.df_recuperados = self.data_trasposed.iloc[2:self.largo, 102:118]
        self.df_array = [self.df_confirmados, self.df_muertos, self.df_recuperados]
        #-------------------------------------------------------------------------------
        # Se agregan los nombres de columnas a los Data Frame creados
        #-------------------------------------------------------------------------------
        for i in range(len(self.df_array)):
            self.df_array[i].columns = [ "Arica y Parinacota",
                                    "Tarapacá",
                                    "Antofagasta",
                                    "Atacama",
                                    "Coquimbo",
                                    "Valparaíso",
                                    "Metropolitana",
                                    "O’Higgins",
                                    "Ñuble",
                                    "Maule",
                                    "Biobío",
                                    "Araucanía", #
                                    "Los Ríos",
                                    "Los Lagos",
                                    "Aysén",
                                    "Magallanes"]
    def get_columns_df(self,df):
        list_col = list(df.columns.values)# Se obtiene la lista de clumnas correspondientes regiones
        list_col_head = df.columns.values[0:len(list_col)] #Filtramos solo desde el indice 2
        return (list_col_head)

    def confirmados_region(self, name_region):
        columna = self.df_confirmados[name_region].reset_index(drop=True)
        return (columna)

    def muertos_region(self, name_region):
        columna = self.df_muertos[name_region].reset_index(drop=True)
        return (columna)

    def recuperados_region(self, name_region):
        columna = self.df_recuperados[name_region].reset_index(drop=True)
        return (columna)

    def get_fechas(self):
        data_top = self.data_trasposed.head(self.largo)
        fechas_array = []
        # iterating the columns
        for row in data_top.index:
            fechas_array.append(row)
        return (fechas_array[2:self.largo])

    def all_region(self):
        regiones = [
                    "Arica y Parinacota",
                    "Tarapacá",
                    "Antofagasta",
                    "Atacama",
                    "Coquimbo",
                    "Valparaíso",
                    "Metropolitana",
                    "Ohiggins",
                    "Ñuble",
                    "Maule",
                    "Bio Bío",
                    "Araucanía", #
                    "Los Ríos",
                    "Los Lagos",
                    "Aysén",
                    "Magallanes"
                    ]
        return regiones
    def generate_dataframe(self, name_region, activos = False):
        #-------------------------------------------------------------------------------
        #Se obtienen los datos necesarios
        #-------------------------------------------------------------------------------
        confirmados = self.confirmados_region(name_region)
        muertos = self.muertos_region(name_region)
        recuperados = self.recuperados_region(name_region)
        fechas = self.get_fechas()

        #-------------------------------------------------------------------------------
        # Armando Data Frame
        #-------------------------------------------------------------------------------
        region = {
            "Fecha": fechas,
            "Casos_Confirmados": confirmados,
            "Casos_Fallecidos" : muertos,
            "Casos_Recuperados": recuperados,
        }
        df = pd.DataFrame(region, columns = ["Fecha", "Casos_Confirmados", "Casos_Fallecidos","Casos_Recuperados"] )
        df = df.fillna(0) #Se camian todos los valores NaN por 0
        df['Casos_Confirmados'][df["Casos_Confirmados"] == 0] = 0
        df["Fecha"] = pd.to_datetime(df['Fecha'], infer_datetime_format=True)
        if activos == True:
            df["Casos_Activos"] = df.Casos_Confirmados - df.Casos_Fallecidos - df.Casos_Recuperados
        df = df.assign(Dias=[i for i in range(len(fechas))]) # Se genera el campo Dias
        return df
