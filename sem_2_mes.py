# imporatr las librerias necesarias para le funcionamiento
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Directorio donde se encuentran los archivos CSV y la cual sera la base de trabajo del Script
ruta_guardado = "Transacciones/2024/Semanas/Semana 5"
semana = '5'
# Definir el nombre del archivo que contendra la union de todos
validadores = "Validadores.csv"
# Definir los nombres de los archivos que se van a leer
archivos_a_leer = [
    "20240129-Transacciones.csv",
    "20240130-Transacciones.csv",
    "20240131-Transacciones.csv",
    "20240201-Transacciones.csv",
    "20240202-Transacciones.csv",
    "20240203-Transacciones.csv",
    "20240204-Transacciones.csv",
]

# Lista para almacenar los DataFrames de los archivos
transacciones = []

resumen =[]
# Leer los archivos y almacenarlos en la lista de DataFrames
for archivo in archivos_a_leer:
    archivo_path = os.path.join(ruta_guardado, archivo)
    df = pd.read_csv(archivo_path)
    transacciones.append(df)
    
for df in transacciones:
    ## Filtrar las transacciones de tipo 0
    df['TIPO_TRANSACCION'] = df['TIPO_TRANSACCION'].astype('str')
    df_filtro = df[df['TIPO_TRANSACCION'] == '0'].copy()

    ## Sacaremos el total de transacciones con el metodo count 
    tr_totales = df_filtro['TIPO_TRANSACCION'].count()

    ## Convertir la columna FECHA_HORA_TRANSACCION a datetime
    df_filtro['FECHA_HORA_TRANSACCION'] = pd.to_datetime(df_filtro['FECHA_HORA_TRANSACCION'])
    df_filtro['FECHA_HORA_TRANSACCION'] = df_filtro['FECHA_HORA_TRANSACCION'].dt.strftime('%Y-%m-%d')

    ## Separar las transacciones en base al método
    df_fisico = df_filtro[df_filtro['LOCATION_ID'] == '201A00']
    df_digital = df_filtro[df_filtro['LOCATION_ID'] == '101800']
    df_appcdmx = df_filtro[df_filtro['LOCATION_ID'] == '101801']

    ## Calcular el monto total por transacción física y agregar al DataFrame correspondiente
    monto_fisico = df_fisico['MONTO_TRANSACCION'].sum()

    ## Calcular el monto total por transacción digital y agregar al DataFrame correspondiente
    monto_digital = df_digital['MONTO_TRANSACCION'].sum()
    ## 
    monto_appcdmx = df_appcdmx['MONTO_TRANSACCION'].sum()

    ## Obtener los valores únicos de la fecha de transacción
    fechas_unicas = df_filtro['FECHA_HORA_TRANSACCION'].unique()

    ## Agregar los resultados a la lista de resumen 
    resumen.append({
        'FECHA': ', '.join(fechas_unicas),
        'TR Digitales': df_digital.shape[0],
        'TR Fisicas': df_fisico.shape[0],
        'TR AppCDMX': df_appcdmx.shape[0],
        'TR Totales': tr_totales,
        'Montos Digitales': monto_digital / 100,
        'Montos Fisicos': monto_fisico / 100,
        'Montos AppCDMX': monto_appcdmx / 100,
        'Monto Total': (monto_digital + monto_fisico + monto_appcdmx)/100,
    })
    
resultados = pd.DataFrame(resumen)
archivo_sem = f"RRE_semana_{semana}.csv"
ruta_res_sem = os.path.join(ruta_guardado, archivo_sem)
resultados.to_csv(ruta_res_sem, index=False)
print("Creando Grafico")
## Definir el nombre del grafico
nombre_grafico = f'RR_Grafico_Semana_{semana}.png'
## Definir el titulo del grafico
title = f'Montos recaudados por tipo de red semana {semana}'
## Definir el estilo del grafico
plt.style.use('seaborn-v0_8-paper')
## Definir el ancho de cada una de las barras
width = 0.8  
## Definimos el objeto grafico (ancho,alto)
fig,ax = plt.subplots(figsize=(18,8))
## Valores base para las barras apiladas
bottom = np.zeros(7)
## Colores para las barras
colors = ['#385723','#a50021'] 
# Define variables
fechas = resultados['FECHA']
tr_rrd = resultados['TR Digitales'] + resultados['TR AppCDMX']
tr_rrf = resultados['TR Fisicas']
mto_tt = resultados['Monto Total']
# Asigna nombres a las Series
tr_rrd.name = 'TR Digitales'
tr_rrf.name = 'TR Fisicas'
mto_tt.name = 'Monto Total'
# Crea un DataFrame
tr_counts = pd.DataFrame({
    'TR Digitales': np.array(tr_rrd),
    'TR Fisicas': np.array(tr_rrf),
})
# Crea el gráfico
fig, ax = plt.subplots(figsize=(12,8))
## Creamos la iteracion de los datos
for i, (tr, tr_count) in enumerate(tr_counts.items()):
    ## Creamos un grafico de barras
    p = ax.bar(fechas, tr_count, width, label=tr, bottom=bottom, color=colors[i])
    ## Generamos el apilamiento de barras
    bottom += tr_count
    ## Asignamos las etiwuetas a las barras
    ax.bar_label(p, label_type='center', color='#fff',fontsize=10,fontweight=600,**{'fmt': '{:,.0f}'})
## Creamos un segundo eje
ax2 = ax.twinx()
## Graficamos una linea con el nuevo eje
ax2.plot(fechas, mto_tt, label="Montos", color="#fe9c55", marker='o',linestyle="solid")
## Añadimos las etiquetas a la linea
for i, (fecha, monto) in enumerate(zip(fechas, mto_tt)):
    if monto >= min(mto_tt) :  
        ax2.annotate(f"${monto:,.0f}", (fecha, monto), xytext=(2,5), textcoords='offset points', fontsize=10,fontweight=600)

## Posicionamiento de la etiqueta del eje secundario
ax2.yaxis.set_label_position("right")
## Se asignan las etiqetas para los ejes
ax2.set_ylabel("Valor Monetario",fontsize=8,fontweight=600)
ax.set_ylabel("N° de Transacciones",fontsize=8,fontweight=600)
ax.set_xlabel(f'Semana {semana}',fontsize=8,fontweight=600)
## Creamos una legenda fuera del grafico
fig.legend(loc='outside upper left')
# Ajusta el formato de los valores en el eje Y
ax.yaxis.set_major_formatter(lambda x, pos: f'{x:,.0f}')
ax2.yaxis.set_major_formatter(lambda x, pos: f'{x:,.0f}')
# Ajusta el título del gráfico
ax.set_title(title,fontsize=12,fontweight=600)
# Guarda el gráfico en alta resolución
ruta_grafico = os.path.join(ruta_guardado, nombre_grafico)
plt.savefig(ruta_grafico,format='png',dpi=900,bbox_inches='tight')
print("Proceso realizado con Exito!!")