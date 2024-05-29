import pandas as pd
import os
## Define: mes ="Febrero" --- Nombre del mes
mes = "Marzo"
## Define: m ="02"  ---- Numero del mes
m = "03"
## Define: y ="2024" --- Año a tomar en cuenta en el analisis
y = "2024"
## Rango de dias semanales L - V Agregando + 1 al viernes ** Leer documentacion metodo range
dia_in = 1
dia_fn = 16
## Nombre de las extenciones de los archivos que ocupara el script para realizar 
a = "-Transacciones.csv"
## Ruta de la cual se extraeran todos los archivos y en la misma se guardaran los archivos
work_path = f"Transacciones/{y}/{m} {mes}"
archivo_tr = [os.path.join(work_path, f"{y}{m}{d:02d}{a}") for d in range(dia_in, dia_fn)]
## Areglo que se llenara con los archivos -Transacciones-extension.csv
transacciones = []
## Bucle para insertar todos los archivos en el DataFrame transacciones
for transaccion in archivo_tr:
  df = pd.read_csv(transaccion, low_memory=False)
  transacciones.append(df)


## Filtrar las transacciones de tipo 0
df['TIPO_TRANSACCION'] = df['TIPO_TRANSACCION'].astype('str')
df_filtro = df[df['TIPO_TRANSACCION'] == '0'].copy()
##
df_fisico = df_filtro[df_filtro['LOCATION_ID'] == '201A00']
df_digital = df_filtro[df_filtro['LOCATION_ID'] == '101800']
df_appcdmx = df_filtro[df_filtro['LOCATION_ID'] == '101801']


fileApp = f'APP_{dia_in}_{dia_fn}_{mes}.csv'
fileRRF = f'RRF_{dia_in}_{dia_fn}_{mes}.csv'
fileRRD = f'RRD_{dia_in}_{dia_fn}_{mes}.csv'

rutaApp = os.path.join(work_path,fileApp)
rutaRRF = os.path.join(work_path,fileRRF)
rutaRRD = os.path.join(work_path,fileRRD)
print('Generando Archivo RRF')
df_fisico.to_csv(rutaRRF,index=False)
print('Generando Archivo RRD')
df_digital.to_csv(rutaRRD,index=False)
print('Generando Archivo APP')
df_appcdmx.to_csv(rutaApp,index=False)
print('Proceso Finalizado con Exito!')
