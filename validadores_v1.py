import os
import pandas as pd

##
mes = "Enero"
##
m = "01"
##
y = "2024"

##
ruta_trabajo = f"Validadores/{y}/{m} {mes}"

##
periodo = "15_al_21_enero"

## Arcchivo a subir 
file_to_upload = 'Validaciones del 15 al 21 de enero 2024.csv'

## metodo para asignar la ruta al archivo
archivo = os.path.join(ruta_trabajo, file_to_upload)
df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')

df['FECHA_HORA_TRANSACCION'] = pd.to_datetime(df['FECHA_HORA_TRANSACCION'])
df['FECHA_HORA_TRANSACCION'] = df['FECHA_HORA_TRANSACCION'].dt.strftime('%Y-%m-%d')
# Obtener fechas unicas
fechas_unicas = df['FECHA_HORA_TRANSACCION'].unique()

documento = []
for fecha in fechas_unicas:
    # Filtrar el DataFrame por la fecha actual
    df['TIPO_TRANSACCION'] = df['TIPO_TRANSACCION'].astype('str')
    df_fecha = df[df['FECHA_HORA_TRANSACCION'] == fecha]
    # Filtrar por tipo de transaccion
    df_bus = df_fecha[df_fecha['TIPO_TRANSACCION'] == '3'] # Debito en Bus
    df_ban = df_fecha[df_fecha['TIPO_TRANSACCION'] == '5'] # debito en baño
    df_pgo = df_fecha[df_fecha['TIPO_TRANSACCION'] == '70'] # Gratuidad de operacion
    df_tra = df_fecha[df_fecha['TIPO_TRANSACCION'] == '7'] # Transbordo
    df_sal = df_fecha[df_fecha['TIPO_TRANSACCION'] == '11'] # Salida
    ## transacciones no exitosas, no permiten acceso
    df_gra = df_fecha[df_fecha['TIPO_TRANSACCION'] == '0D'] # rechazo de tarjeta en lista negra 
    df_rfw = df_fecha[df_fecha['TIPO_TRANSACCION'] == '13'] # rechazo de tarjeta fuera de la lista blanca
    df_sss = df_fecha[df_fecha['TIPO_TRANSACCION'] == '51'] # transaccio abortada por saldo insuficiente
    df_asm = df_fecha[df_fecha['TIPO_TRANSACCION'] == '53'] # Transaccion abortada por saldo mayor al maximo permitido
    df_ati = df_fecha[df_fecha['TIPO_TRANSACCION'] == '54'] # transaccion abortada por aplicacion de transporte invalido
    df_tai = df_fecha[df_fecha['TIPO_TRANSACCION'] == '55'] # Transaccion abortada por contrato invalido
    df_tax = df_fecha[df_fecha['TIPO_TRANSACCION'] == '61'] # Transaccion abortada por cualquier otro caso
    df_tve = df_fecha[df_fecha['TIPO_TRANSACCION'] == '60'] # Transaccion abortada por vigencia expirada
    df_ff = df_fecha[df_fecha['TIPO_TRANSACCION'] == 'FF'] # Transaccion sin descripcion

    # Montos
    monto_cetrams = sum(df_ban['MONTO_TRANSACCION']) / 100
    monto_buses = sum(df_bus['MONTO_TRANSACCION']) / 100

    # Transacciones
    tr_cetrams = df_ban.shape[0]
    tr_buses = df_bus.shape[0]
 
    documento.append({
        'Fecha': fecha,
        'Debitos en autobus (E)': df_bus.shape[0],
        'Debitos en baño (E)': df_ban.shape[0],
        'Valor de Debitos en autobus': monto_buses,
        'Valor de Debitos en baños': monto_cetrams,
        'Gratuidad (E)': df_pgo.shape[0],
        'Transbordo (E)': df_tra.shape[0],
        'Salida (E)': df_sal.shape[0],
        'Rechazo de tarjeta por lista negra': df_gra.shape[0],
        'Rechazo de tarjeta por recarga fuera de lista blanca': df_rfw.shape[0],
        'Sin saldo suficiente': df_sss.shape[0],
        'Transaccion abortada por saldo mayor': df_asm.shape[0],
        'Transaccion abortada por aplicacion de transporte invalido': df_ati.shape[0],
        'Transaccion abortada (cualquier otro caso)': df_tax.shape[0],
        'Transaccion abortada por vigencia expirada': df_tve.shape[0],
        'FF': df_ff.shape[0],
    })
# Create a DataFrame from the list of dictionaries
resultados = pd.DataFrame(documento)
# orena el DataFrame por 'Fecha' en modo ascendente 
resultados = resultados.sort_values(by='Fecha')
# Calcula todos los totales
sum_row = {
    'Fecha': 'Total',
    'Debitos en autobus (E)': resultados['Debitos en autobus (E)'].sum(),
    'Debitos en baño (E)': resultados['Debitos en baño (E)'].sum(),
    'Valor de Debitos en autobus': resultados['Valor de Debitos en autobus'].sum(),
    'Valor de Debitos en baños': resultados['Valor de Debitos en baños'].sum(),
    'Gratuidad (E)': resultados['Gratuidad (E)'].sum(),
    'Transbordo (E)': resultados['Transbordo (E)'].sum(),
    'Salida (E)': resultados['Salida (E)'].sum(),
    'Rechazo de tarjeta por lista negra': resultados['Rechazo de tarjeta por lista negra'].sum(),
    'Rechazo de tarjeta por recarga fuera de lista blanca': resultados['Rechazo de tarjeta por recarga fuera de lista blanca'].sum(),
    'Sin saldo suficiente': resultados['Sin saldo suficiente'].sum(),
    'Transaccion abortada por saldo mayor': resultados['Transaccion abortada por saldo mayor'].sum(),
    'Transaccion abortada por aplicacion de transporte invalido': resultados['Transaccion abortada por aplicacion de transporte invalido'].sum(),
    'Transaccion abortada (cualquier otro caso)': resultados['Transaccion abortada (cualquier otro caso)'].sum(),
    'Transaccion abortada por vigencia expirada': resultados['Transaccion abortada por vigencia expirada'].sum(),
    'FF': resultados['FF'].sum(),
}

resultados = pd.concat([resultados, pd.DataFrame([sum_row])], ignore_index=True)

print(resultados)
# Guarda el DataFrame a CSV 
archivo_val = f"Resumen_Val_{periodo}.csv"
ruta_resultados = os.path.join(ruta_trabajo, archivo_val)
resultados.to_csv(ruta_resultados, index=False)

df.LINEA.replace('1', 'MIIT', inplace=True)
df.LINEA.replace('2', 'SAUSA', inplace=True)
df.LINEA.replace('3', 'ATROLSA', inplace=True)
df.LINEA.replace('4', 'CEUSA', inplace=True)
df.LINEA.replace('5', 'TRIOXA', inplace=True)
df.LINEA.replace('6', 'ACASA', inplace=True)
df.LINEA.replace('7', 'AULSA', inplace=True)
df.LINEA.replace('9', 'COPATTSA', inplace=True)
df.LINEA.replace('11', 'CODIVERSA', inplace=True)
df.LINEA.replace('12', 'COPESA', inplace=True)
df.LINEA.replace('13', 'TVO', inplace=True)
df.LINEA.replace('15', 'ABC', inplace=True)
df.LINEA.replace('D', 'AMOPSA', inplace=True)
df.LINEA.replace('E', 'CETRAM ZAPATA', inplace=True)
df.LINEA.replace('34', 'CETRAM BUENAVISTA', inplace=True)
df.LINEA.replace('36', 'CETRAM TACUBAYA', inplace=True)

lineas = [ 
          'MIIT', 
          'SAUSA', 
          'ATROLSA', 
          'CEUSA', 
          'TRIOXA', 
          'ACASA', 
          'AULSA', 
          'COPATTSA', 
          'CODIVERSA', 
          'COPESA', 
          'TVO', 
          'ABC',
          'AMOPSA',
          'CETRAM ZAPATA', 
          'CETRAM BUENAVISTA', 
          'CETRAM TACUBAYA'
        ]

documento_linea = []
for linea in lineas:
    # Filtrar el DataFrame por la línea actual
    df_linea = df[df['LINEA'] == str(linea)]

    ## transacciones exitosas, permiten el acceso
    lin_bus = df_linea[df_linea['TIPO_TRANSACCION'] == '3'] # Debito en Bus
    lin_ban = df_linea[df_linea['TIPO_TRANSACCION'] == '5'] # debito en baño
    lin_pgo = df_linea[df_linea['TIPO_TRANSACCION'] == '70'] # Gratuidad de operacion
    lin_tra = df_linea[df_linea['TIPO_TRANSACCION'] == '7'] # Transbordo
    lin_sal = df_linea[df_linea['TIPO_TRANSACCION'] == '11'] # Salida
    ## transacciones no exitosas, no permiten acceso
    lin_gra = df_linea[df_linea['TIPO_TRANSACCION'] == '0D'] # rechazo de tarjeta en lista negra 
    lin_rfw = df_linea[df_linea['TIPO_TRANSACCION'] == '13'] # rechazo de tarjeta fuera de la lista blanca
    lin_sss = df_linea[df_linea['TIPO_TRANSACCION'] == '51'] # transaccio abortada por saldo insuficiente
    lin_asm = df_linea[df_linea['TIPO_TRANSACCION'] == '53'] # Transaccion abortada por saldo mayor al maximo permitido
    lin_ati = df_linea[df_linea['TIPO_TRANSACCION'] == '54'] # transaccion abortada por aplicacion de transporte invalido
    lin_tai = df_linea[df_linea['TIPO_TRANSACCION'] == '55'] # Transaccion abortada por contrato invalido
    lin_tax = df_linea[df_linea['TIPO_TRANSACCION'] == '61'] # Transaccion abortada por cualquier otro caso
    lin_tve = df_linea[df_linea['TIPO_TRANSACCION'] == '60'] # Transaccion abortada por vigencia expirada
    lin_ff = df_linea[df_linea['TIPO_TRANSACCION'] == 'FF'] # Tramsaccion sin descripcion
    ## montos
    lin_mbu = sum(lin_bus['MONTO_TRANSACCION']) / 100
    lin_mba = sum(lin_ban['MONTO_TRANSACCION']) / 100
    documento_linea.append({
        'Linea': linea,
        'Debitos en autobus': lin_bus.shape[0],
        'Debitos en baño': lin_ban.shape[0],
        'Valor de Debitos en autobus': lin_mbu,
        'Valor de Debitos en baños': lin_mba,
        'Gratuidad': lin_pgo.shape[0],
        'Transbordo': lin_tra.shape[0],
        'Salida': lin_sal.shape[0],
        'Rechazo de tarjeta en lista negra': lin_gra.shape[0],
        'Rechazo de tarjeta por recarga fuera de lista blanca': lin_rfw.shape[0],
        'Sin saldo suficiente': lin_sss.shape[0],
        'Transaccion abortada por saldo mayor': lin_asm.shape[0],
        'Transaccion abortada por aplicacion de transporte invalido': lin_ati.shape[0],
        'Transaccion abortada por contrato invalido (firma erronea)': lin_tai.shape[0],
        'Transaccion abortada (cualquier otro caso)': lin_tax.shape[0],
        'Transaccion abortada por vigencia expirada': lin_tve.shape[0],
        'FF': lin_ff.shape[0],
    })

resultados_lin = pd.DataFrame(documento_linea)
# Calcula los totales
sum_rows = {
    'Linea': 'Total',
    'Debitos en autobus': resultados_lin['Debitos en autobus'].sum(),
    'Debitos en baño': resultados_lin['Debitos en baño'].sum(),
    'Valor de Debitos en autobus': resultados_lin['Valor de Debitos en autobus'].sum(),
    'Valor de Debitos en baños': resultados_lin['Valor de Debitos en baños'].sum(),
    'Gratuidad': resultados_lin['Gratuidad'].sum(),
    'Transbordo': resultados_lin['Transbordo'].sum(),
    'Salida': resultados_lin['Salida'].sum(),
    'Rechazo de tarjeta en lista negra': resultados_lin['Rechazo de tarjeta en lista negra'].sum(),
    'Rechazo de tarjeta por recarga fuera de lista blanca': resultados_lin['Rechazo de tarjeta por recarga fuera de lista blanca'].sum(),
    'Sin saldo suficiente': resultados_lin['Sin saldo suficiente'].sum(),
    'Transaccion abortada por saldo mayor': resultados_lin['Transaccion abortada por saldo mayor'].sum(),
    'Transaccion abortada por aplicacion de transporte invalido': resultados_lin['Transaccion abortada por aplicacion de transporte invalido'].sum(),
    'Transaccion abortada por contrato invalido (firma erronea)': resultados_lin['Transaccion abortada por contrato invalido (firma erronea)'].sum(),
    'Transaccion abortada (cualquier otro caso)': resultados_lin['Transaccion abortada (cualquier otro caso)'].sum(),
    'Transaccion abortada por vigencia expirada': resultados_lin['Transaccion abortada por vigencia expirada'].sum(),
    'FF': resultados_lin['FF'].sum(),
}

resultados_lin = pd.concat([resultados_lin, pd.DataFrame([sum_rows])], ignore_index=True)

print(resultados_lin)
archivo_lin = f"Resumen_Lin_Enero_{periodo}.csv"
ruta_res_lin = os.path.join(ruta_trabajo, archivo_lin)
resultados_lin.to_csv(ruta_res_lin, index=False)

print('Proceso Finalizado!!')

# df_gra = df[df['TIPO_TRANSACCION'] == '51']
# df_lin_1 = df_gra[df_gra['LINEA'] == '1']
# df_bs = df_lin_1['AUTOBUS'].value_counts()
# print(df_gra)
# print(df_lin_1)
# print(df_bs)
# print(len(df_bs))