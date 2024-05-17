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
df_bth = df_fil_dc[df_fil_dc['LOCATION_ID'] != '101801']    
# df_bth = df_fil_dc[(df_fil_dc['LOCATION_ID'] == '201A00') & (df_fil_dc['LOCATION_ID'] == '201A00') ]   
##
df_ac['TIPO_TRANSACCION'] = df_ac['TIPO_TRANSACCION'].astype('str')
df_fil_ac = df_ac[df_ac['TIPO_TRANSACCION'] == '0']
df_app = df_fil_ac[df_fil_ac['LOCATION_ID'] == '101801']
df_rre = df_fil_ac[df_fil_ac['LOCATION_ID'] != '101801']    
##
list_com = df_com['NUMERO_SERIE_HEX'].unique()
list_bth = df_bth['NUMERO_SERIE_HEX'].unique()
list_dig = df_dig['NUMERO_SERIE_HEX'].unique()
list_app = df_app['NUMERO_SERIE_HEX'].unique()

print( 'Suma x Sep',(len(list_com) + len(list_dig) ) )
print('Sin AppCDMX',len(list_bth))
print('AppCDMX',len(list_app))


lista_sin_coincidencias = [e for e in list_bth if e  in list_app]
print('Coinci',len(lista_sin_coincidencias)) 
#
res_com = []
for card in list_bth:
   
    cardInfo = df_bth[df_bth['NUMERO_SERIE_HEX'] == card]
    tipo = cardInfo['LOCATION_ID'].values
    fnt = set(tipo)
    monto = cardInfo['MONTO_TRANSACCION'].sum()
    
    res_com.append({
        'cshex': card,
        'tipoRed':fnt,
        '# Recargas': cardInfo.shape[0],
        '$ Recargas': monto / 100
    })
    
resultados_comercios = pd.DataFrame(res_com)
print(resultados_comercios)
res_app = []
for card in list_app:
    
    cardInfo = df_app[df_app['NUMERO_SERIE_HEX'] == card]
    tipo = cardInfo['LOCATION_ID'].values
    fnt = set(tipo)
    monto = cardInfo['MONTO_TRANSACCION'].sum()
    
    res_app.append({
        'cshex': card,
        'tipoRed':fnt,
        '# Recargas': cardInfo.shape[0],
        '$ Recargas': monto / 100
    })
   
resultados_appcdmx = pd.DataFrame(res_app)
print(resultados_appcdmx)
res_fna = []
for card in lista_sin_coincidencias:
    
    cardInfo = df_app[df_app['NUMERO_SERIE_HEX'] == card]
    tipo = cardInfo['LOCATION_ID'].values
    fnt = set(tipo)
    monto = cardInfo['MONTO_TRANSACCION'].sum()
    
    res_fna.append({
        'cshex': card,
        'tipoRed':fnt,
        '# Recargas': cardInfo.shape[0],
        '$ Recargas': monto / 100
    })
    
resultados_finales = pd.DataFrame(res_fna)
print(resultados_finales)

rre_fix = []
for card in lista_sin_coincidencias:
    cardInfo = df_rre[df_rre['NUMERO_SERIE_HEX'] == card]
    tipo = cardInfo['LOCATION_ID'].values
    fnt = set(tipo)
    monto = cardInfo['MONTO_TRANSACCION'].sum()
    rre_fix.append({
        'cshex': card,
        'tipoRed':fnt,
        '# Recargas': cardInfo.shape[0],
        '$ Recargas': monto / 100
    })
    
rre_res_act = pd.DataFrame(rre_fix)
print(rre_res_act)
print('Creando Documento Final')
doc_fna = f'Migracion_RRF_RRD_TO_APPCDMX.xlsx'
ruta_doc_fna = os.path.join(ruta_trabajo,doc_fna)
with pd.ExcelWriter(ruta_doc_fna, mode='a') as writer:
    resultados_comercios.to_excel(writer,index=False,sheetname='RE_Nov-Ene_RRD-RRF')
    resultados_appcdmx.to_excel(writer,index=False,sheetname='RE_Feb-Abril-App')
    resultados_finales.to_excel(writer,index=False,sheetname='Resumen-Migracion')
    rre_res_act.to_excel(writer,index=False,sheetname='Resumen-Migracion-RRE')

print('Proceso Finalizado con Exito!! Wenas Noches :v')