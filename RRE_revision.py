import os
import pandas as pd

ruta_guardado = "Revision/Noviembre"
validadores = "Revisado.csv"

resumen = []
archivo = os.path.join(ruta_guardado, 'Noviembre_completo_2da_qna.csv')
doc = pd.read_csv(archivo, low_memory=False, encoding='latin-1')

fechas_unicas = doc['FECHA_HORA_TRANSACCION'].unique()

for fecha in fechas_unicas:
    df_filter = doc.loc[doc['FECHA_HORA_TRANSACCION'] == fecha].copy()

    df_filter['FECHA_HORA_TRANSACCION'] = pd.to_datetime(df_filter['FECHA_HORA_TRANSACCION'])
    df_filter['FECHA_TRANSACCION'] = df_filter['FECHA_HORA_TRANSACCION'].dt.date

    tra_dig = df_filter.loc[df_filter['LOCATION_ID'] == '101800']
    tra_fis = df_filter.loc[df_filter['LOCATION_ID'] == '201A00']

    mto_dig = sum(tra_dig['MONTO_TRANSACCION'] / 100)
    mto_fis = sum(tra_fis['MONTO_TRANSACCION'] / 100)

    resumen.append({
        'FECHA': fecha,
        'Montos Digitales': mto_dig,
        'Montos Fisicos': mto_fis,
        'Monto Total': mto_fis + mto_dig,
    })

resultados = pd.DataFrame(resumen)
ruta_resultados = os.path.join(ruta_guardado, validadores)
resultados.to_csv(ruta_resultados, index=False)
