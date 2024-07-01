import os
import pandas as pd

## Definimos el mes con nombre
mes = "Junio"
## Definimos el mes con número
m = "06"
## Definimos el año
y = "2024"

## La ruta de trabaajo es la ruta donde se leen y se generan los archivos
ruta_trabajo = f"Transacciones/{y}/{m} {mes}"

## Archivo a subir 
file_to_upload = '20240604-Transacciones.csv'

## metodo para asignar la ruta al archivo
archivo = os.path.join(ruta_trabajo, file_to_upload)
df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')

df_duplicados = df[df[['NUMERO_SERIE_HEX','FECHA_HORA_TRANSACCION','SALDO_ANTES_TRANSACCION','MONTO_TRANSACCION']].duplicated()]
print(df_duplicados)
# print(df[df[['FECHA_HORA_TRANSACCION']].duplicated()])
# # df_dup = df[df[['NUMERO_SERIE_HEX','FECHA_HORA_TRANSACCION','LOCATION_ID','TIPO_TRANSACCION','SALDO_ANTES_TRANSACCION','MONTO_TRANSACCION']].duplicated()]
# df_dup = df[df[['FECHA_HORA_TRANSACCION']].duplicated()]
df_dup_short = df_duplicados[['ID_TRANSACCION_ORGANISMO','NUMERO_SERIE_HEX','FECHA_HORA_TRANSACCION','LOCATION_ID','TIPO_TRANSACCION','SALDO_ANTES_TRANSACCION','MONTO_TRANSACCION']]
card = '000000007C899CC8'
df_hex = df[df['NUMERO_SERIE_HEX'] == card] 
print(df_dup_short)
# print(df_hex[['ID_TRANSACCION_ORGANISMO','NUMERO_SERIE_HEX','FECHA_HORA_TRANSACCION','LOCATION_ID','TIPO_TRANSACCION','SALDO_ANTES_TRANSACCION','MONTO_TRANSACCION']])