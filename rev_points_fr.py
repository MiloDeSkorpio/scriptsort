##importar librearias necesarias para el funcionamiento del script
import os
import pandas as pd

## 
smartpos_list = [
            'SMARTPOS1494242323',
            'SMARTPOS1494242822',
            'SMARTPOS1494243063',
            'SMARTPOS1494241112',
            'SMARTPOS1494575251',
            'SMARTPOS1494240999',
            'SMARTPOS1494576364',
            'SMARTPOS1494571594',
            'SMARTPOS1494240394',
            'SMARTPOS1494240425',
            'SMARTPOS1494574794',
            ]
smartpos_list_id = [
            '1494242323',
            '1494242822',
            '1494243063',
            '1494241112',
            '1494575251',
            '1494240999',
            '1494576364',
            '1494571594',
            '1494240394',
            '1494240425',
            '1494574794',
            ]
# Nombre del mes con texto, se ocupara para leer la carpeta del mes y asignar el nombre a los archivos generados
mes_nombre = "Febrero"

## Modificar el contenido de m = "mes" * Para los meses que anteriores a octubre ocupar la sintaxis 09 = Septiembre 08 = Agosto
## Modificar el contenido de Y = "Año" 2023 / 2024 / 2025 
m = "02"
y = "2024"

## Nombre de las extenciones de los archivos que ocupara el script para realizar 
a = "-Transacciones.csv"
ae = "-Transacciones-extension.csv"

## Ruta de la cual se extraeran todos los archivos y en la misma se guardaran los archivos
ruta_guardado = f"Transacciones/{y}/{m} {mes_nombre}"

## Este es el rango de dias en el que se trabajara, para el tema del ultimo dia siempre se le sumara 1
## Ejemplo primera quincena dia_fn = 16 el metodo range trabaja de esa forma
dia_in = 1
dia_fn = 30
rango = dia_fn - dia_in

## Listado de los archvios -Transacciones.csv
## Listado de los archivo a leer segun el rango especificado 
archivo_tr = [os.path.join(ruta_guardado, f"{y}{m}{d:02d}{a}") for d in range(dia_in, dia_fn)]

## Leer Archivos de Extencion para obtener la duracion de las transacciones
## Lista de nombres de archivo
archivo_ex = [os.path.join(ruta_guardado, f"{y}{m}{d:02d}{ae}") for d in range(dia_in, dia_fn)]

## Areglo que se llenara con los archivos -Transacciones-extension.csv
transacciones = []
## Bucle para insertar todos los archivos en el DataFrame transacciones
for transaccion in archivo_tr:
  df = pd.read_csv(transaccion, low_memory=False)
  transacciones.append(df)

## Concatenación de documentos extraídos del arreglo transacciones y creando un solo DataFrame con información de toda la quincena
## Arreglo que se llenara con los archivos -Transacciones.csv
extenciones = []
## Bucle para insertar todos los archivos en el DataFrame extenciones
for extencion in archivo_ex:
  df = pd.read_csv(extencion)
  extenciones.append(df)

df_smartpos = pd.concat(extenciones,ignore_index=True)
df_trmes = pd.concat(transacciones,ignore_index=True)

coincidencias = []
for smartpos in smartpos_list:
    smartpos_filtered = df_smartpos[df_smartpos['DEVICE_ID'] == smartpos]
    match = pd.merge(df_trmes, smartpos_filtered, on="ID_TRANSACCION_ORGANISMO", how="inner")
    coincidencias.append(match)
df_coincidencias = pd.concat(coincidencias,ignore_index=True)

# archivo_mens = f"FR_SMARTPOS_{mes_nombre}.csv"
# ruta_res_mens = os.path.join(ruta_guardado, archivo_mens)
# df_coincidencias.to_csv(ruta_res_mens, index=False)
###
## Convertir la columna FECHA_HORA_TRANSACCION a datetime
df_coincidencias['FECHA_HORA_TRANSACCION'] = pd.to_datetime(df_coincidencias['FECHA_HORA_TRANSACCION'])
df_coincidencias['FECHA_HORA_TRANSACCION'] = df_coincidencias['FECHA_HORA_TRANSACCION'].dt.strftime('%Y-%m-%d')
# Obtener los valores únicos de la fecha de transacción
fechas_unicas = df_coincidencias['FECHA_HORA_TRANSACCION'].unique()
resumen = []
post = []
for fecha in fechas_unicas:
  df_fil = df_coincidencias.loc[df_coincidencias['FECHA_HORA_TRANSACCION'] == fecha]
  monto = sum(df_fil['MONTO_TRANSACCION'] / 100)
  resumen.append({
      'FECHA': fecha,
      '# Transacciones': df_fil.shape[0],
      'Monto': monto,
  })

  s1 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[0]]
  s2 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[1]]
  s3 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[2]]
  s4 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[3]]
  s5 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[4]]
  s6 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[5]]
  s7 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[6]]
  s8 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[7]]
  s9 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[8]]
  s10 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[9]]
  s11 = df_fil[df_fil['DEVICE_ID'] == smartpos_list[10]]

  smpo1 = sum(s1['MONTO_TRANSACCION'] / 100)
  smpo2 = sum(s2['MONTO_TRANSACCION'] / 100)
  smpo3 = sum(s3['MONTO_TRANSACCION'] / 100)
  smpo4 = sum(s4['MONTO_TRANSACCION'] / 100)
  smpo5 = sum(s5['MONTO_TRANSACCION'] / 100)
  smpo6 = sum(s6['MONTO_TRANSACCION'] / 100)
  smpo7 = sum(s7['MONTO_TRANSACCION'] / 100)
  smpo8 = sum(s8['MONTO_TRANSACCION'] / 100)
  smpo9 = sum(s9['MONTO_TRANSACCION'] / 100)
  smpo10 = sum(s10['MONTO_TRANSACCION'] / 100)
  smpo11 = sum(s11['MONTO_TRANSACCION'] / 100)


  post.append(  {
      'FECHA':fecha,
      smartpos_list_id[0]: smpo1,
      smartpos_list_id[1]: smpo2,
      smartpos_list_id[2]: smpo3,
      smartpos_list_id[3]: smpo4,
      smartpos_list_id[4]: smpo5,
      smartpos_list_id[5]: smpo6,
      smartpos_list_id[6]: smpo7,
      smartpos_list_id[7]: smpo8,
      smartpos_list_id[8]: smpo9,
      smartpos_list_id[9]: smpo10,
      smartpos_list_id[10]: smpo11,
  })
res = pd.DataFrame(post)
res = res.sort_values(by='FECHA')
print(res)  
archivo_res = f"Disp_POST_{mes_nombre}.csv"
ruta_resultados = os.path.join(ruta_guardado,archivo_res )
res.to_csv(ruta_resultados, index=False)

print('Analisis Finalizado con Exito!!')



