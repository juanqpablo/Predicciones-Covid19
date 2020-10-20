import pandas as pd
from pymongo import MongoClient
#-------------------------------------------------------------------------------
# Declaración de variables
#-------------------------------------------------------------------------------
regiones = []; casosNuevos = []; casosTotales = []; casosRecuperados =[]

conn = MongoClient()
try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.datos_covid
collection = db.casosXRegion

def get_dataxFields(file, name_data):
    array_data = []
    for d in file[name_data]:
        array_data.append(d)
    return (array_data[1:len(array_data)])

for mes in range(3, 10):
    location = ""
    if mes == 3 or mes == 5 or mes==7 or mes == 8:
        for dia in range(3,32)
            if mes == 3 and dia <=21:
                location = "./data/producto4/"+"2020-0"+mes+"-0"+dia+"-CasosConfirmados-totalRegional.csv"
                file = pd.read_csv(location,
                                sep=',',
                                names=["Region","CasosNuevos","CasosTotales","CasosRecuperados"])
            if mes == 3 and dia >=21 and dia <26:
                location = "./data/producto4/"+"2020-0"+mes+"-0"+dia+"-CasosConfirmados-totalRegional.csv"
                file = pd.read_csv(location,
                                sep=',',
                                names=["Region","CasosNuevos","CasosTotales","Fallecidos"])
            if mes == 3 and dia >=26:
                location = "./data/producto4/"+"2020-0"+mes+"-0"+dia+"-CasosConfirmados-totalRegional.csv"
                file = pd.read_csv(location,
                                sep=',',
                                names=["Region","CasosNuevos","CasosTotales","CasosRecuperados","Fallecidos"])

    if mes == 4 or mes == 6 or mes == 9:
        for dia in range(3,31)
            if mes == 4 and dia <= 4:
                location = "./data/producto4/"+"2020-0"+mes+"-0"+dia+"-CasosConfirmados-totalRegional.csv"
                file = pd.read_csv(location,
                                sep=',',
                                names=["Region","CasosNuevos","CasosTotales","Fallecidos"])
            if mes == 4 and dia >= 4 and dia <= 28:
                location = "./data/producto4/"+"2020-0"+mes+"-0"+dia+"-CasosConfirmados-totalRegional.csv"
                file = pd.read_csv(location,
                                sep=',',
                                names=["Region","CasosNuevos","CasosTotales","%CasosTotales","Fallecidos"])
            if mes == 4 and dia >28  and dia <=30:
                location = "./data/producto4/"+"2020-0"+mes+"-0"+dia+"-CasosConfirmados-totalRegional.csv"
                file = pd.read_csv(location,
                        sep=',',
                        names=["Region","CasosNuevosConSintomas","CasosNuevosSinSintomas","CasosTotalesAcomulados","%Total","Fallecidos","Tasa100000","Inc-diario","CasosTotales"])


    if mes == 10:
        location = "./data/producto4/"+"2020-0"+mes+"-0"+dia+"-CasosConfirmados-totalRegional.csv"
        for dia in range(3,20)
            file = pd.read_csv(location,
                            sep=',',
                            names=["Region","CasosNuevosConSintomas","CasosNuevosSinSintomas","CasosTotalesAcomulados","%Total","Fallecidos","Tasa100000","Inc-diario","CasosTotales"])

regiones = get_dataxFields(file, "Region")
casosNuevos = get_dataxFields(file, "CasosNuevos")
casosTotales = get_dataxFields(file, "CasosTotales")
casosRecuperados = get_dataxFields(file,"CasosRecuperados")

for c in range(len(regiones)):
    data = {
        "Fecha" :
        "Region": regiones[c],
        "CasosNuevos":casosNuevos[c],
        "CasosTotales":casosTotales[c],
        "CasosRecurepados": casosRecuperados
        }
    # Insert Data
    collection.insert_one(data)
print("Datos insertados correctamente: ")
