import os
import pandas as pd

ruta_guardado = "Validadores/Noviembre"
validadores = "Validadores.csv"

documento = []
documento_linea = []
archivo = os.path.join(ruta_guardado, 'Validaciones del 27 de nov al 03 de dic 2023.csv')
df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')

# Convertir la columna FECHA_HORA_TRANSACCION a datetime
df['FECHA_HORA_TRANSACCION'] = df['FECHA_HORA_TRANSACCION'].str.split(' ', expand=True)[0]
df['FECHA_HORA_TRANSACCION'] = pd.to_datetime(df['FECHA_HORA_TRANSACCION'], format="%d/%m/%Y")

# Obtener fechas únicas

fechas_unicas = df['FECHA_HORA_TRANSACCION'].unique()


for fecha in fechas_unicas:
    # Filtrar el DataFrame por la fecha actual

    df_fecha = df[df['FECHA_HORA_TRANSACCION'] == fecha]

    # Filtrar por tipo de transacción
    df_ban = df_fecha[df_fecha['TIPO_TRANSACCION'] == 5]
    df_bus = df_fecha[df_fecha['TIPO_TRANSACCION'] == 3]
    df_gra = df_fecha[df_fecha['TIPO_TRANSACCION'] == 4]
    df_tra = df_fecha[df_fecha['TIPO_TRANSACCION'] == 7]
    df_sal = df_fecha[df_fecha['TIPO_TRANSACCION'] == 11]
    df_rfw = df_fecha[df_fecha['TIPO_TRANSACCION'] == 13]
    df_sss = df_fecha[df_fecha['TIPO_TRANSACCION'] == 51]
    df_asm = df_fecha[df_fecha['TIPO_TRANSACCION'] == 53]
    df_tai = df_fecha[df_fecha['TIPO_TRANSACCION'] == 55]
    df_tax = df_fecha[df_fecha['TIPO_TRANSACCION'] == 61]
    df_pgo = df_fecha[df_fecha['TIPO_TRANSACCION'] == 70]

    # Montos
    monto_cetrams = sum(df_ban['MONTO_TRANSACCION']) / 100
    monto_buses = sum(df_bus['MONTO_TRANSACCION']) / 100

    # Transacciones
    tr_cetrams = df_ban.shape[0]
    tr_buses = df_bus.shape[0]
 
    documento.append({
        'Fecha': fecha,
        'Débitos en autobús': df_bus.shape[0],
        'Débitos en baño': df_ban.shape[0],
        'Valor de Débitos en autobús': monto_buses,
        'Valor de Débitos en baños': monto_cetrams,
        'Gratuidad': df_gra.shape[0],
        'Transbordo': df_tra.shape[0],
        'Salida': df_sal.shape[0],
        'Rechazo de tarjeta por recarga fuera de lista blanca': df_rfw.shape[0],
        'Sin saldo suficiente': df_sss.shape[0],
        'Transacción abortada por saldo mayor': df_asm.shape[0],
        #'Transacción abortada por contrato inválido (firma errónea)': df_tai.shape[0],
        'Transacción abortada (cualquier otro caso)': df_tax.shape[0],
        'Pase gratuito por operación': df_pgo.shape[0],
    })
# Create a DataFrame from the list of dictionaries
resultados = pd.DataFrame(documento)
# Sort the DataFrame by the 'Fecha' column in ascending order
resultados = resultados.sort_values(by='Fecha')

# Calculate and append the row for the sum of all values
sum_row = {
    'Fecha': 'Total',
    'Débitos en autobús': resultados['Débitos en autobús'].sum(),
    'Débitos en baño': resultados['Débitos en baño'].sum(),
    'Valor de Débitos en autobús': resultados['Valor de Débitos en autobús'].sum(),
    'Valor de Débitos en baños': resultados['Valor de Débitos en baños'].sum(),
    'Gratuidad': resultados['Gratuidad'].sum(),
    'Transbordo': resultados['Transbordo'].sum(),
    'Salida': resultados['Salida'].sum(),
    'Rechazo de tarjeta por recarga fuera de lista blanca': resultados['Rechazo de tarjeta por recarga fuera de lista blanca'].sum(),
    'Sin saldo suficiente': resultados['Sin saldo suficiente'].sum(),
    'Transacción abortada por saldo mayor': resultados['Transacción abortada por saldo mayor'].sum(),
    #'Transacción abortada por contrato inválido (firma errónea)': resultados['Transacción abortada por contrato inválido (firma errónea)'].sum(),
    'Transacción abortada (cualquier otro caso)': resultados['Transacción abortada (cualquier otro caso)'].sum(),
    'Pase gratuito por operación': resultados['Pase gratuito por operación'].sum(),
}

resultados = pd.concat([resultados, pd.DataFrame([sum_row])], ignore_index=True)



lineas = [ 1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 15, 'D', 'E', 34, 36]

for linea in lineas:
    # Filtrar el DataFrame por la línea actual
    df_linea = df[df['LINEA'] == str(linea)]

    lin_bus = df_linea[df_linea['TIPO_TRANSACCION'] == 3]
    lin_ban = df_linea[df_linea['TIPO_TRANSACCION'] == 5]
    lin_mbu = sum(lin_bus['MONTO_TRANSACCION']) / 100
    lin_mba = sum(lin_ban['MONTO_TRANSACCION']) / 100
    lin_gra = df_linea[df_linea['TIPO_TRANSACCION'] == 4]
    lin_tra = df_linea[df_linea['TIPO_TRANSACCION'] == 7]
    lin_sal = df_linea[df_linea['TIPO_TRANSACCION'] == 11]
    lin_rfw = df_linea[df_linea['TIPO_TRANSACCION'] == 13]
    lin_sss = df_linea[df_linea['TIPO_TRANSACCION'] == 51]
    lin_asm = df_linea[df_linea['TIPO_TRANSACCION'] == 53]
    lin_tai = df_linea[df_linea['TIPO_TRANSACCION'] == 55]
    lin_tax = df_linea[df_linea['TIPO_TRANSACCION'] == 61]
    lin_pgo = df_linea[df_linea['TIPO_TRANSACCION'] == 70]

    documento_linea.append({
        'Linea': linea,
        'Débitos en autobús': lin_bus.shape[0],
        'Débitos en baño': lin_ban.shape[0],
        'Valor de Débitos en autobús': lin_mbu,
        'Valor de Débitos en baños': lin_mba,
        'Gratuidad': lin_gra.shape[0],
        'Transbordo': lin_tra.shape[0],
        'Salida': lin_sal.shape[0],
        'Rechazo de tarjeta por recarga fuera de lista blanca': lin_rfw.shape[0],
        'Sin saldo suficiente': lin_sss.shape[0],
        'Transacción abortada por saldo mayor': lin_asm.shape[0],
        'Transacción abortada por contrato inválido (firma errónea)': lin_tai.shape[0],
        'Transacción abortada (cualquier otro caso)': lin_tax.shape[0],
        'Pase gratuito por operación': lin_pgo.shape[0],
    })

resultados_lin = pd.DataFrame(documento_linea)
#resultados_lin = resultados_lin.sort_values(by='Valor de Débitos en autobús', ascending=False)
# Calculate and append the row for the sum of all values
sum_rows = {
    'Linea': 'Total',
    'Débitos en autobús': resultados_lin['Débitos en autobús'].sum(),
    'Débitos en baño': resultados_lin['Débitos en baño'].sum(),
    'Valor de Débitos en autobús': resultados_lin['Valor de Débitos en autobús'].sum(),
    'Valor de Débitos en baños': resultados_lin['Valor de Débitos en baños'].sum(),
    'Gratuidad': resultados_lin['Gratuidad'].sum(),
    'Transbordo': resultados_lin['Transbordo'].sum(),
    'Salida': resultados_lin['Salida'].sum(),
    'Rechazo de tarjeta por recarga fuera de lista blanca': resultados_lin['Rechazo de tarjeta por recarga fuera de lista blanca'].sum(),
    'Sin saldo suficiente': resultados_lin['Sin saldo suficiente'].sum(),
    'Transacción abortada por saldo mayor': resultados_lin['Transacción abortada por saldo mayor'].sum(),
    'Transacción abortada por contrato inválido (firma errónea)': resultados_lin['Transacción abortada por contrato inválido (firma errónea)'].sum(),
    'Transacción abortada (cualquier otro caso)': resultados_lin['Transacción abortada (cualquier otro caso)'].sum(),
    'Pase gratuito por operación': resultados_lin['Pase gratuito por operación'].sum(),
}

resultados_lin = pd.concat([resultados_lin, pd.DataFrame([sum_rows])], ignore_index=True)


# Save the DataFrame to a CSV file
archivo_val = "Resumen_Val_Nov_27_Dic_03.csv"
ruta_resultados = os.path.join(ruta_guardado, archivo_val)
resultados.to_csv(ruta_resultados, index=False)

# Save the DataFrame to a CSV file
archivo_lin = "Resumen_Lin_Nov_27_Dic_03.csv"
ruta_res_lin = os.path.join(ruta_guardado, archivo_lin)
resultados_lin.to_csv(ruta_res_lin, index=False)
