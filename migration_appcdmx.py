import os
import pandas as pd

ruta_trabajo = 'Transacciones/migration'

pe1 = [
    "Full_Noviembre.csv",
    "Full_Diciembre.csv",
    "Full_Enero.csv",
]
pe2 = [
    "Full_21-29_Febrero.csv",
    "Full_Marzo.csv",
    "Full_Abril.csv",
]

per1 = []
per2 = []

def lectura_archivos(array_l,array_s):
    for archivo in array_l:
        archivo_path = os.path.join(ruta_trabajo,archivo)
        df = pd.read_csv(archivo_path)
        array_s.append(df)
##  
lectura_archivos(pe1,per1)
lectura_archivos(pe2,per2)
##
df_dc = pd.concat(per1)
df_ac = pd.concat(per2)
##
df_dc['TIPO_TRANSACCION'] = df_dc['TIPO_TRANSACCION'].astype('str')
df_fil_dc = df_dc[df_dc['TIPO_TRANSACCION'] == '0']
df_com = df_fil_dc[df_fil_dc['LOCATION_ID'] == '201A00'] 
df_dig = df_fil_dc[df_fil_dc['LOCATION_ID'] == '101800']    
##
df_ac['TIPO_TRANSACCION'] = df_ac['TIPO_TRANSACCION'].astype('str')
df_fil_ac = df_ac[df_ac['TIPO_TRANSACCION'] == '0']
df_app = df_fil_ac[df_fil_ac['LOCATION_ID'] == '101801']    
##
list_com = df_com['NUMERO_SERIE_HEX'].unique()
list_dig = df_dig['NUMERO_SERIE_HEX'].unique()
list_app = df_app['NUMERO_SERIE_HEX'].unique()
print(len(list_com))
print(len(list_dig))
print(len(list_app))
##
# res_com = []
# for card in list_com:
#     cardInfo = df_com[df_com['NUMERO_SERIE_HEX'] == card]
#     monto = cardInfo['MONTO_TRANSACCION'].sum()
    
#     res_com.append({
#         'cshex': card,
#         'tipoRed':'201A800',
#         '# Recargas': cardInfo.shape[0],
#         '$ Recargas': monto / 100
#     })
# resultados_comercios = pd.DataFrame(res_com)
# print(resultados_comercios)



