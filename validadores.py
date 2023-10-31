# imporatr las librerias necesarias para le funcionamiento
import os
import pandas as pd
# Directorio donde se encuentran los archivos CSV y la cual sera la base de trabajo del Script
ruta_guardado = "Validadores/Octubre"

# Definir el nombre del archivo que contendra la union de todos
validadores = "Validadores.csv"
# Definir los nombres de los archivos que se van a leer
archivos_a_leer = [
    "Acasa.csv",
    "Informe 1.2.csv",
    "Informe 1.3.csv",
    "Informe 1.4.csv",
    "Informe 1.5.csv",  
    "Microsafe.csv"
]

# Lista para almacenar los DataFrames de los archivos
dataframes = []

# Leer los archivos y almacenarlos en la lista de DataFrames
for archivo in archivos_a_leer:
    archivo_path = os.path.join(ruta_guardado, archivo)
    df = pd.read_csv(archivo_path)
    dataframes.append(df)

df_valid = pd.concat(dataframes,ignore_index=True)

ruta_validadores = os.path.join(ruta_guardado,validadores)
df_valid.to_csv(ruta_validadores,index=False)
'''# conteo de resultados por cada archivo y al final
# conteo de todos los resultados del DataFrame que contiene todos los archivos unidos
print(dataframes[0].shape)
print(dataframes[1].shape)
print(dataframes[2].shape)
print(dataframes[3].shape)
print(dataframes[4].shape)
print(dataframes[5].shape)
print(df_valid.shape)'''
df_filter = df_valid[df_valid['TIPO_TRANSACCION'] == "3"]
df_rechazo = df_valid[df_valid['TIPO_TRANSACCION'] == "51"] 
df_invalid = df_valid[df_valid['TIPO_TRANSACCION'].isnull() | (df_valid['TIPO_TRANSACCION'] == '')]
print("Transaccion = a 3",df_filter.shape)
print("Transaccion = a 51",df_rechazo.shape)
print("Transaccion = a null",df_invalid.shape)

linea1 = df_valid[df_valid['LINEA'] == "1"]
print(df_valid['LOCATION_ID'].head(10))
print(linea1.shape)
# En esta linea conocemos todas las transacciones por linea
print(df_valid['LINEA'].value_counts())
# Suma de montos
montos_centavos = df_filter['MONTO_TRANSACCION'].sum()

print(montos_centavos)

# Fechas
for df in dataframes:
    df_filtro = df[df['TIPO_TRANSACCION'] == '3'].copy()
    df_filtro['FECHA_HORA_TRANSACCION'] = pd.to_datetime(df_filtro['FECHA_HORA_TRANSACCION'])
    df_filtro['FECHA_HORA_TRANSACCION'] = df_filtro['FECHA_HORA_TRANSACCION'].dt.strftime('%Y-%m-%d')
    #
    df_fisico = df_filtro[df_filtro['LOCATION_ID'] == '201A00']
    df_digital = df_filtro[df_filtro['LOCATION_ID'] == '101800']
print(df_filtro['FECHA_HORA_TRANSACCION'].unique())
print(df_fisico)
print(df_digital)