import os
import pandas as pd
###############################################################################
#                           Carga de archivos                                 #
###############################################################################
## Definimos el mes con nombre
mes = "Febrero"
## Definimos el mes con número
m = "02"
## Definimos el año
y = "2024"
## La ruta de trabaajo es la ruta donde se leen y se generan los archivos
ruta_trabajo = f"Validadores/{y}/{m} {mes}"
## Archivo a subir 
file_to_upload = 'Validaciones 2da qna febrero 2024.csv'
archivo = os.path.join(ruta_trabajo, file_to_upload)
df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')
## Ruta de las Listas
ruta_listas = "Listas/"
## Cargar lista Blanca
white_list = '20240212_listaBlanca_v34.csv'
wl = os.path.join(ruta_listas, white_list)
df_wl = pd.read_csv(wl, low_memory=False, encoding='latin-1')
## Cargar lista Negra
black_list = '20240201_listaNegra_v39.csv'
bl = os.path.join(ruta_listas, black_list)
df_bl = pd.read_csv(bl, low_memory=False, encoding='latin-1')
## Cargar Validacion de la MAC
macverify = '20240220-MacVerify-conduent aulsa_1.csv'
mcv = os.path.join(ruta_listas, macverify)
df_mcv = pd.read_csv(mcv, low_memory=False, encoding='latin-1')
###############################################################################
#                           Inicio de Analisis                                #
###############################################################################
df['TIPO_TRANSACCION'] = df['TIPO_TRANSACCION'].astype('str')
buses = df[df['TIPO_TRANSACCION'] == '3']
baños = df[df['TIPO_TRANSACCION'] == '5']
transbordos =df[df['TIPO_TRANSACCION'] == '7']
validas =[buses,baños,transbordos]
df_validas = pd.concat(validas, ignore_index=True)
# print(df_validas['TIPO_TRANSACCION'].value_counts())
## Convertir el numero de la tarjeta a decimal
df_validas['NUMERO_SERIE_DECIMAL'] = df_validas['NUMERO_SERIE_HEX'].apply(lambda x: int(x, 16))
## Obtener la longitud del numero decimal 
df_validas['LONGITUD_DECIMAL'] = df_validas['NUMERO_SERIE_DECIMAL'].apply(lambda x: len(str(x)))
long = df_validas['LONGITUD_DECIMAL']
# print(df['LONGITUD_DECIMAL'].value_counts() )
# print(df_wl['serial_hex'])
# print(df_bl['card_serial_number'])
df_bl.rename(columns={'card_serial_number': 'NUMERO_SERIE_HEX'}, inplace=True)
df_wl.rename(columns={'serial_hex': 'SAM_SERIAL_HEX_ULTIMA_RECARGA'}, inplace=True)
# print(df_wl)
hex_bl = df_bl['NUMERO_SERIE_HEX']
hex_df = df_validas['NUMERO_SERIE_HEX']
# print(long)
hex_wl = df_wl['SAM_SERIAL_HEX_ULTIMA_RECARGA']
# print(hex_wl)
hex_sam_df = df_validas['SAM_SERIAL_HEX_ULTIMA_RECARGA']
# print(hex_sam_df)
df_match_bl = pd.merge(hex_bl, hex_df, on="NUMERO_SERIE_HEX", how="inner")
print(df_match_bl)
registros_no_encontrados = pd.merge(hex_sam_df, hex_wl, on="SAM_SERIAL_HEX_ULTIMA_RECARGA", how="left", indicator=True)
# archivo_mens = f"results_wl.csv"
# ruta_res = os.path.join(ruta_trabajo, archivo_mens)
# registros_no_encontrados.to_csv(ruta_res, index=False)
no_dentro = registros_no_encontrados[registros_no_encontrados['_merge'] == 'left_only']
print(no_dentro['SAM_SERIAL_HEX_ULTIMA_RECARGA'].value_counts())
# Mostrar las filas con valores fuera del rango de momento muestra 0
df_fuera_rango = df_validas.loc[df_validas["LONGITUD_DECIMAL"].isin([x for x in df_validas["LONGITUD_DECIMAL"] if x < 8 or x > 10])]
# print(len(df_fuera_rango))

