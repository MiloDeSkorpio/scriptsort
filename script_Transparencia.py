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
##
hex_recargas = [] 
## 
hex_valids = []
# Leer los archivos y almacenarlos en la lista de DataFrames
for archivo in archivos_a_leer:
    archivo_path = os.path.join(ruta_guardado, archivo)
    df = pd.read_csv(archivo_path)
    dataframes.append(df)
## 
df_all = pd.concat(dataframes,ignore_index=True)
## 
df_recargas = df_all[df_all['TIPO_TRANSACCION'] == '3']
##
tarjetas_unicas = pd.DataFrame({'NUMERO_SERIE_HEX': df_recargas['NUMERO_SERIE_HEX'].unique()})
df_hex = pd.merge(df_all, pd.DataFrame(tarjetas_unicas, columns=['NUMERO_SERIE_HEX']), on='NUMERO_SERIE_HEX', how='inner')

# Creamos una DataFrame con los datos de las tarjetas únicas
df_tarjetas_unicas = pd.DataFrame(tarjetas_unicas)

# Obtenemos los datos de cada tarjeta
for tarjeta in df_tarjetas_unicas['NUMERO_SERIE_HEX']:
    origen = df_hex.loc[df_hex['NUMERO_SERIE_HEX'] == tarjeta, 'ENVIRONMENT_ISSUER_ID'].iloc[0]
    pto_vta = df_hex.loc[df_hex['NUMERO_SERIE_HEX'] == tarjeta, 'CONTRACT_SALE_SAM'].iloc[0]
    fecha = df_hex.loc[df_hex['NUMERO_SERIE_HEX'] == tarjeta, 'FECHA_HORA_TRANSACCION'].iloc[0]
    mto = df_hex.loc[df_hex['NUMERO_SERIE_HEX'] == tarjeta, 'MONTO_TRANSACCION'].iloc[0]

    # Agregamos los datos a las DataFrames de recargas y validaciones
    hex_recargas.append({
        'NUMERO_SERIE_HEX': tarjeta,
        'ENVIRONMENT_ISSUER_ID': origen,
        'CONTRACT_SALE_SAM': pto_vta,
    })
    hex_valids.append({
        'NUMERO_SERIE_HEX': tarjeta,
        'MONTO_TRANSACCION': mto,
        'FECHA_HORA_TRANSACCION': fecha,
    })

    
df_hex_fin = pd.DataFrame(hex_recargas)
archivo_hex = f"Hex_val_Octubre.csv"
ruta_hex = os.path.join(ruta_guardado, archivo_hex)
df_hex_fin.to_csv(ruta_hex, index=False)

df_valid_fin = pd.DataFrame(hex_valids)
archivo_valid = f"Hex_deb_Octubre.csv"
ruta_valid = os.path.join(ruta_guardado,archivo_valid)
df_valid_fin.to_csv(ruta_valid, index=False)

print("Proceso Finalizado con Exito!!")