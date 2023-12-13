# imporatr las librerias necesarias para le funcionamiento
import os
import pandas as pd
# Directorio donde se encuentran los archivos CSV y la cual sera la base de trabajo del Script
ruta_guardado = "Transacciones/hexids"

# Definir el nombre del archivo que contendra la union de todos
validadores = "Recargas_ORT_2023.csv"
# Definir los nombres de los archivos que se van a leer
archivos_a_leer = [
    "Hex_ID_Enero.csv",
    "Hex_ID_Febrero.csv",
    "Hex_ID_Marzo.csv",
    "Hex_ID_Abril.csv",
    "Hex_ID_Mayo.csv",
    "Hex_ID_Junio.csv",
    "Hex_ID_Julio.csv",
    "Hex_ID_Agosto.csv",
    "Hex_ID_Septiembre.csv",
    "Hex_ID_Octubre.csv",
    "Hex_ID_Noviembre.csv",
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