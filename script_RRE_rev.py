##importar librearias necesarias para el funcionamiento del script
import os
import pandas as pd

## Nombre del mes con texto, se ocupara para leer la carpeta del mes y asignar el nombre a los archivos generados
mes_nombre = "Noviembre"

## Modificar el contenido de m = "mes" * Para los meses que anteriores a octubre ocupar la sintaxis 09 = Septiembre 08 = Agosto
## Modificar el contenido de Y = "Año" 2023 / 2024 / 2025 
m = "11"
y = "2023"

## Nombre de las extenciones de los archivos que ocupara el script para realizar 
a = "-Transacciones.csv"
ae = "-Transacciones-extension.csv"
at = "-Test-Transacciones.csv"

## Ruta de la cual se extraeran todos los archivos y en la misma se guardaran los archivos
ruta_guardado = f"Transacciones/{m} {mes_nombre}"

## Quincena a trabajar
first = "1ra"
second = "2da"

## Definir el nombre de los archivos que seran guardados en la carpeta al finalizar el analisis
mes_completo = f"{mes_nombre}_completo.csv"

## Archivos quincenales agregar # al inicio cuando se desea trabajar por mes el script
archivo_mp = f"Reporte_MP_{second}_qna_{mes_nombre}.xlsx"
quincena = f"{second}_qna_{mes_nombre}"

## Archivos mensuales eliminar # cuando se trabaje el script por mes
#archivo_mp = f"Reporte_MP_{mes_nombre}.xlsx"## Desactivar cuando se requiera el Reporte_MP_mensual
#quincena = f"{mes_nombre}" ## Desactivar cuando se requiera el Resumen_RRE_mensual

## Este es el rango de dias en el que se trabajara, para el tema del ultimo dia siempre se le sumara 1
## Ejemplo primera quincena dia_fn = 16 el metodo range trabaja de esa forma
dia_in =  1
dia_fn = 31

## Listado de los archvios -Transacciones.csv
## Listado de los archivo a leer segun el rango especificado 
archivo_tr = [os.path.join(ruta_guardado, f"{y}{m}{d:02d}{a}") for d in range(dia_in, dia_fn)]

## Leer Archivos de Extencion para obtener la duracion de las transacciones
## Lista de nombres de archivo
archivo_ex = [os.path.join(ruta_guardado, f"{y}{m}{d:02d}{ae}") for d in range(dia_in, dia_fn)]

## Areglo que se llenara con los archivos -Transacciones-extension.csv
extenciones = []

## Arreglo que se llenara con los archivos -Transacciones.csv
transacciones = []

## Arreglo que recopilara los datos Resumidos del filtro y se ocupara para realizar el RRE
resumen = []
##
hex_recargas = []
## Bucle para insertar todos los archivos en el DataFrame transacciones

for transaccion in archivo_tr:
    df = pd.read_csv(transaccion)
    transacciones.append(df)

## Bucle para insertar todos los archivos en el DataFrame extenciones
for extencion in archivo_ex:
    df = pd.read_csv(extencion)
    extenciones.append(df)   
    
## Concatenación de documentos extraídos del arreglo transacciones y creando un solo DataFrame con información de toda la quincena
df_transacciones = pd.concat(transacciones, ignore_index=True)
ruta_transacciones = os.path.join(ruta_guardado, mes_completo)
df_transacciones.to_csv(ruta_transacciones)

## Concatenación de documentos extraídos del arreglo extenciones y creando un solo DataFrame con información de todo el mes
df_extenciones = pd.concat(extenciones, ignore_index=True)

## Imprime el tipo de transacciones
print(df_transacciones["TIPO_TRANSACCION"].value_counts())

#df_recargas = df_transacciones[df_transacciones['TIPO_TRANSACCION'] == '0'].copy()
## Documento Resumen recarga externa

for day in transacciones:
    df_recargas = day[day['TIPO_TRANSACCION'] == '0'].copy()
    ## Separar Transacciones fisicas y digitales
    #df_mix = df_recargas.apply(lambda x: 'Comercios' if x['LOCATION_ID'] == '201A00' else 'Digitales', axis=1)
    df_m_fisico = df_recargas[df_recargas['LOCATION_ID'] == '201A00']
    df_m_digital = df_recargas[df_recargas['LOCATION_ID'] == '101800']
    ## Crear filtro para las transacciones de recarga
    md = sum(df_m_digital['MONTO_TRANSACCION'] / 100)
    mf = sum(df_m_fisico['MONTO_TRANSACCION'] / 100)
    ## Convertir fecha
    df_recargas['FECHA_HORA_TRANSACCION'] = pd.to_datetime(df_recargas['FECHA_HORA_TRANSACCION'])
    df_recargas['FECHA_HORA_TRANSACCION'] = df_recargas['FECHA_HORA_TRANSACCION'].dt.strftime('%Y-%m-%d')
    ## Obtener los valores únicos de la fecha de transacción  
    fechas_unicas = df_recargas['FECHA_HORA_TRANSACCION'].unique()
    ## Conteo de Transacciones
    ttd = df_m_digital.shape[0]
    ttf = df_m_fisico.shape[0]

    resumen.append({
        'FECHA': ', '.join(fechas_unicas),
        'Montos RRD': md ,
        'Montos RRF': mf,
        'Total Montos': md + mf,
        'Transacciones RRD': ttd,
        'Transacciones RRF': ttf,
        'Total Transacciones': ttd + ttf,
    })

df_resumen = pd.DataFrame(resumen)
archivo_rre = f"Resumen_RRE_new_{quincena}.csv"
ruta_resumen = os.path.join(ruta_guardado, archivo_rre)
df_resumen.to_csv(ruta_resumen, index=False)
## 
df_transacciones.LOCATION_ID.replace('101800', 'Digitales', inplace=True)
df_transacciones.LOCATION_ID.replace('201A00', 'Comercios', inplace=True)
df_transacciones = df_transacciones.drop(df_transacciones[df_transacciones.LOCATION_ID == 101801].index)
df_transacciones.MONTO_TRANSACCION = df_transacciones.MONTO_TRANSACCION.astype('float64') / 100
df_filtrado = df_transacciones.loc[:, ['NUMERO_SERIE_HEX', 'LOCATION_ID', 'MONTO_TRANSACCION','FECHA_HORA_TRANSACCION']]

# Imprimir el DataFrame filtrado
print(df_filtrado)

       
df_hex_fin = pd.DataFrame(df_filtrado)
archivo_hex = f"Hex_ID_{mes_nombre}.csv"
ruta_hex = os.path.join(ruta_guardado, archivo_hex)
df_hex_fin.to_csv(ruta_hex, index=False)




