##importar librearias necesarias para el funcionamiento del script
import os
import pandas as pd

## Nombre del mes con texto, se ocupara para leer la carpeta del mes y asignar el nombre a los archivos generados
mes_nombre = "Enero"

## Modificar el contenido de m = "mes" * Para los meses que anteriores a octubre ocupar la sintaxis 09 = Septiembre 08 = Agosto
## Modificar el contenido de Y = "Año" 2023 / 2024 / 2025 
m = "01"
y = "2023"

## Nombre de las extenciones de los archivos que ocupara el script para realizar 
a = "-Transacciones.csv"
ae = "-Transacciones-extension.csv"
at = "-Test-Transacciones.csv"

## Ruta de la cual se extraeran todos los archivos y en la misma se guardaran los archivos
ruta_guardado = f"Transacciones/{y}/{m} {mes_nombre}"

## Quincena a trabajar
first = "1ra"
second = "2da"

## Este es el rango de dias en el que se trabajara, para el tema del ultimo dia siempre se le sumara 1
## Ejemplo primera quincena dia_fn = 16 el metodo range trabaja de esa forma
dia_in = 5
dia_fn = 8
rango = dia_fn - dia_in

## Listado de los archvios -Transacciones.csv
## Listado de los archivo a leer segun el rango especificado 
archivo_tr = [os.path.join(ruta_guardado, f"{y}{m}{d:02d}{a}") for d in range(dia_in, dia_fn)]

## Areglo que se llenara con los archivos -Transacciones-extension.csv
transacciones = []

## Leer Archivos de Extencion para obtener la duracion de las transacciones
## Lista de nombres de archivo
archivo_ex = [os.path.join(ruta_guardado, f"{y}{m}{d:02d}{ae}") for d in range(dia_in, dia_fn)]

## Arreglo que se llenara con los archivos -Transacciones.csv
extenciones = []

## Bucle para insertar todos los archivos en el DataFrame transacciones
for transaccion in archivo_tr:
    df = pd.read_csv(transaccion)
    transacciones.append(df)

## Concatenación de documentos extraídos del arreglo transacciones y creando un solo DataFrame con información de toda la quincena
#df_transacciones = pd.concat(transacciones, ignore_index=True)

## Bucle para insertar todos los archivos en el DataFrame extenciones
for extencion in archivo_ex:
    df = pd.read_csv(extencion)
    extenciones.append(df)  
     
## Concatenación de documentos extraídos del arreglo extenciones y creando un solo DataFrame con información de todo el mes
df_extenciones = pd.concat(extenciones, ignore_index=True)

## Arreglo para almacenar el RRE
resumen = []

## Inicia el condicional para los dias sueltos
if rango < 13 :
    ## Bucle para el analisis de todas las transacciones
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

    ## Convertir el arreglo resumen en DataFrame
    resultados = pd.DataFrame(resumen)
    
    ## Definir el nombre de los archivos que seran guardados en la carpeta al finalizar el analisis
    archivo_sem = f"RRE_{mes_nombre}_{dia_in}-{dia_fn}.csv"
    ruta_res_sem = os.path.join(ruta_guardado, archivo_sem)
    resultados.to_csv(ruta_res_sem, index=False)
        
                
## Inicia el condicional para las Quincenas        
elif rango >= 13 and rango <= 16:
    print('Es quincena')
## Inicia el Condicional para los meses    
elif rango > 16:
    print('Es Mes')

