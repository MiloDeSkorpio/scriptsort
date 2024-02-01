import os
import pandas as pd

ruta_trabajo = "Validadores/2024/01 Enero"
periodo = "1ra_qna_enero"
file_to_upload = 'Validaciones de la 1ra qna de enero 2024.csv'
archivo = os.path.join(ruta_trabajo, file_to_upload)
df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')


# Convertir la columna FECHA_HORA_TRANSACCION a datetime
df['FECHA_HORA_TRANSACCION'] = pd.to_datetime(df['FECHA_HORA_TRANSACCION'])
df['FECHA_HORA_TRANSACCION'] = df['FECHA_HORA_TRANSACCION'].dt.strftime('%Y-%m-%d')
# Obtener fechas unicas
fechas_unicas = df['FECHA_HORA_TRANSACCION'].unique()

documento = []
for fecha in fechas_unicas:
    # Filtrar el DataFrame por la fecha actual
    df_fecha = df[df['FECHA_HORA_TRANSACCION'] == fecha]
    # Filtrar por tipo de transaccion
    df_ban = df_fecha[df_fecha['TIPO_TRANSACCION'] == '5']
    df_bus = df_fecha[df_fecha['TIPO_TRANSACCION'] == '3']
    df_gra = df_fecha[df_fecha['TIPO_TRANSACCION'] == '4']
    df_tra = df_fecha[df_fecha['TIPO_TRANSACCION'] == '7']
    df_sal = df_fecha[df_fecha['TIPO_TRANSACCION'] == '11']
    df_rfw = df_fecha[df_fecha['TIPO_TRANSACCION'] == '13']
    df_sss = df_fecha[df_fecha['TIPO_TRANSACCION'] == '51']
    df_asm = df_fecha[df_fecha['TIPO_TRANSACCION'] == '53']
    df_tai = df_fecha[df_fecha['TIPO_TRANSACCION'] == '55']
    df_tax = df_fecha[df_fecha['TIPO_TRANSACCION'] == '61']
    df_pgo = df_fecha[df_fecha['TIPO_TRANSACCION'] == '70']
    df_ff = df_fecha[df_fecha['TIPO_TRANSACCION'] == 'FF']

    # Montos
    monto_cetrams = sum(df_ban['MONTO_TRANSACCION']) / 100
    monto_buses = sum(df_bus['MONTO_TRANSACCION']) / 100

    # Transacciones
    tr_cetrams = df_ban.shape[0]
    tr_buses = df_bus.shape[0]
 
    documento.append({
        'Fecha': fecha,
        'Debitos en autobus': df_bus.shape[0],
        'Debitos en baño': df_ban.shape[0],
        'Valor de Debitos en autobus': monto_buses,
        'Valor de Debitos en baños': monto_cetrams,
        'Gratuidad': df_gra.shape[0],
        'Transbordo': df_tra.shape[0],
        'Salida': df_sal.shape[0],
        'Rechazo de tarjeta por recarga fuera de lista blanca': df_rfw.shape[0],
        'Sin saldo suficiente': df_sss.shape[0],
        'Transaccion abortada por saldo mayor': df_asm.shape[0],
        'Transaccion abortada por contrato invalido (firma erronea)': df_tai.shape[0],
        'Transaccion abortada (cualquier otro caso)': df_tax.shape[0],
        'Pase gratuito por operacion': df_pgo.shape[0],
        'FF': df_ff.shape[0],
    })
# Create a DataFrame from the list of dictionaries
resultados = pd.DataFrame(documento)
# orena el DataFrame por 'Fecha' en modo ascendente 
resultados = resultados.sort_values(by='Fecha')
# Calcula todos los totales
sum_row = {
    'Fecha': 'Total',
    'Debitos en autobus': resultados['Debitos en autobus'].sum(),
    'Debitos en baño': resultados['Debitos en baño'].sum(),
    'Valor de Debitos en autobus': resultados['Valor de Debitos en autobus'].sum(),
    'Valor de Debitos en baños': resultados['Valor de Debitos en baños'].sum(),
    'Gratuidad': resultados['Gratuidad'].sum(),
    'Transbordo': resultados['Transbordo'].sum(),
    'Salida': resultados['Salida'].sum(),
    'Rechazo de tarjeta por recarga fuera de lista blanca': resultados['Rechazo de tarjeta por recarga fuera de lista blanca'].sum(),
    'Sin saldo suficiente': resultados['Sin saldo suficiente'].sum(),
    'Transaccion abortada por saldo mayor': resultados['Transaccion abortada por saldo mayor'].sum(),
    'Transaccion abortada por contrato invalido (firma erronea)': resultados['Transaccion abortada por contrato invalido (firma erronea)'].sum(),
    'Transaccion abortada (cualquier otro caso)': resultados['Transaccion abortada (cualquier otro caso)'].sum(),
    'Pase gratuito por operacion': resultados['Pase gratuito por operacion'].sum(),
    'FF': resultados['FF'].sum(),
}

resultados = pd.concat([resultados, pd.DataFrame([sum_row])], ignore_index=True)


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

    lin_bus = df_linea[df_linea['TIPO_TRANSACCION'] == '3']
    lin_ban = df_linea[df_linea['TIPO_TRANSACCION'] == '5']
    lin_mbu = sum(lin_bus['MONTO_TRANSACCION']) / 100
    lin_mba = sum(lin_ban['MONTO_TRANSACCION']) / 100
    lin_gra = df_linea[df_linea['TIPO_TRANSACCION'] == '4']
    lin_tra = df_linea[df_linea['TIPO_TRANSACCION'] == '7']
    lin_sal = df_linea[df_linea['TIPO_TRANSACCION'] == '11']
    lin_rfw = df_linea[df_linea['TIPO_TRANSACCION'] == '13']
    lin_sss = df_linea[df_linea['TIPO_TRANSACCION'] == '51']
    lin_asm = df_linea[df_linea['TIPO_TRANSACCION'] == '53']
    lin_tai = df_linea[df_linea['TIPO_TRANSACCION'] == '55']
    lin_tax = df_linea[df_linea['TIPO_TRANSACCION'] == '61']
    lin_pgo = df_linea[df_linea['TIPO_TRANSACCION'] == '70']
    lin_ff = df_linea[df_linea['TIPO_TRANSACCION'] == 'FF']

    documento_linea.append({
        'Linea': linea,
        'Debitos en autobus': lin_bus.shape[0],
        'Debitos en baño': lin_ban.shape[0],
        'Valor de Debitos en autobus': lin_mbu,
        'Valor de Debitos en baños': lin_mba,
        'Gratuidad': lin_gra.shape[0],
        'Transbordo': lin_tra.shape[0],
        'Salida': lin_sal.shape[0],
        'Rechazo de tarjeta por recarga fuera de lista blanca': lin_rfw.shape[0],
        'Sin saldo suficiente': lin_sss.shape[0],
        'Transaccion abortada por saldo mayor': lin_asm.shape[0],
        'Transaccion abortada por contrato invalido (firma erronea)': lin_tai.shape[0],
        'Transaccion abortada (cualquier otro caso)': lin_tax.shape[0],
        'Pase gratuito por operacion': lin_pgo.shape[0],
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
    'Rechazo de tarjeta por recarga fuera de lista blanca': resultados_lin['Rechazo de tarjeta por recarga fuera de lista blanca'].sum(),
    'Sin saldo suficiente': resultados_lin['Sin saldo suficiente'].sum(),
    'Transaccion abortada por saldo mayor': resultados_lin['Transaccion abortada por saldo mayor'].sum(),
    'Transaccion abortada por contrato invalido (firma erronea)': resultados_lin['Transaccion abortada por contrato invalido (firma erronea)'].sum(),
    'Transaccion abortada (cualquier otro caso)': resultados_lin['Transaccion abortada (cualquier otro caso)'].sum(),
    'Pase gratuito por operacion': resultados_lin['Pase gratuito por operacion'].sum(),
    'FF': resultados_lin['FF'].sum(),
}

resultados_lin = pd.concat([resultados_lin, pd.DataFrame([sum_rows])], ignore_index=True)

# Guarda el DataFrame a CSV 
archivo_val = f"Resumen_Val_{periodo}.csv"
ruta_resultados = os.path.join(ruta_trabajo, archivo_val)
resultados.to_csv(ruta_resultados, index=False)

# Guarda el DataFrame a CSV 
archivo_lin = f"Resumen_Lin_Enero_{periodo}.csv"
ruta_res_lin = os.path.join(ruta_trabajo, archivo_lin)
resultados_lin.to_csv(ruta_res_lin, index=False)

print('Proceso Finalizado!!')