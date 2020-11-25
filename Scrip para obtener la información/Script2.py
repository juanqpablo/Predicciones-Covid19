import pandas as pd
#from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
#from sklearn.preprocessing import PolynomialFeatures
#from sklearn import linear_model
#-------------------------------------------------------------------------------
# VAriables
#-------------------------------------------------------------------------------
url = "./data/producto3/TotalesPorRegion.csv"
file = pd.read_csv(url, sep=',')

def get_data(file, list_days):
    list_data = []
    array_data = {}
    for row in range(0,16):
        region = file.iloc[row][0]
        data = []
        for col in list_days:
            if(file.iloc[row][col]==0):
                data.append(0.01)
            else:
                data.append(file.iloc[row][col])
        array_data[region] = data
    return array_data

list_col = list(file.columns.values)
list_col_head = file.columns.values[2:len(list_col)]

datos = get_data(file, list_col_head)
listX = []

for i in range(0,len(list_col_head)):
    listX.append(i+1)

x=np.array(listX).reshape(-1,1)#[1,2,3,4,5,6,7]
y=np.array(datos['Arica y Parinacota']).reshape(-1,1)#datos confirmados
plt.plot(y,'-m')
#---------------------------#
# preparando datos de tabla #
#---------------------------#
ylogn=np.log(y)#arreglo datos y aplicado ln(y)--> [0.2344,0.1234,]
sumylogn=np.sum(ylogn)#suma total datos ln(y)-->valor
xlogn=np.log(x)#arreglo datos x aplicado log->[0,0,0]
sumxlogn=np.sum(xlogn)#suma total datos ln(x)->valor
ylogn2=np.power(ylogn,2)#arreglo datos ln(y) al cuadrado-->[0.0.0]
sumylogn2=np.sum(ylogn2)#suma-->valor
xlogn2=np.power(xlogn,2)#arreglo datos lnx al cuadrado
sumxlogn2=np.sum(xlogn2)#suma
multlnxy=xlogn*ylogn#arreglo datos lnx*lny-->[0,0,0,0]
smultlnxy=np.sum(multlnxy)#suma

coefb=(smultlnxy-((sumxlogn*sumylogn)/len(list_col_head)))/(sumxlogn2-((np.power(sumxlogn,2)/len(list_col_head))))
coeflna=((sumylogn-coefb*sumxlogn)/len(list_col_head))#resultado de logaritmo del coeficiente a
coefa=np.power(np.e,coeflna)#coeficiente _a_ final

#y=ax**b
print(coefb,coefa,)
y0=coefa*np.power(x,coefb)
plt.plot(y0,'-b')
#----------------------------#
# grado de ajuste del modelo #
#----------------------------#
r2=(coefb*(smultlnxy-((sumxlogn*sumylogn)/len(list_col_head))))/(sumylogn2-(np.power(sumylogn,2)/len(list_col_head)))
print(r2)



#Atacama=16 ; Arica y Parinacota=8; Araucanía=7;Metropolitana=8
# polyFt=PolynomialFeatures(degree=7)
# x=polyFt.fit_transform(x)
#
# model=linear_model.LinearRegression()
# model.fit(x,y)
# ajuste=model.score(x,y)
# ajusteP=round(ajuste*100,3)
# print('Porcentaje de Exactitud:'+ str(ajusteP)+'%')
# y0=model.predict(x)
# plt.plot(y0,'-b')

plt.show()
