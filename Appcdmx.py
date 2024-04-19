import os
import pandas as pd
import json
import datetime
import numpy as np
## Asignar el nombre del mes con texto
mes_nombre = "Febrero"
## Modificar el contenido de m = "mes" * Para los meses que anteriores a octubre ocupar la sintaxis 09 = Septiembre 08 = Agosto
## Modificar el contenido de Y = "Año" 2023 / 2024 / 2025 
m = "02"
y = "2024"
## La ruta de trabaajo es la ruta donde se leen y se generan los archivos
ruta_trabajo = f"Transacciones/ADIP/2024-03-03 BD AppCDMX"
ruta_mp = f"Transacciones/{y}/{m} {mes_nombre}"
## Es el periodo en el que se realiza el analisis
periodo = "04 al 10"
## metodo para asignar la ruta al archivo de las tarjetas
archivo_tarjetas = 'card_numbers_feb_24.csv'
file_card = os.path.join(ruta_trabajo, archivo_tarjetas)
df_cards = pd.read_csv(file_card, low_memory=False, encoding='latin-1')
## metodo para asignar la ruta al archivo de las transacciones
archivo_datos = 'mp_info_01-29_02_2024.csv'
file_info = os.path.join(ruta_trabajo, archivo_datos)
df_tra = pd.read_csv(file_info, low_memory=False, encoding='latin-1')
## 
archivo_mp = f"Full_{mes_nombre}.csv"
file_mp = os.path.join(ruta_mp, archivo_mp)
df_mp = pd.read_csv(file_mp, low_memory=False, encoding='latin-1')
# Lista de identificadores de transacción
ctc = [
    '71286149582',
    '71240815536',
    '71671444315',
    '71879428944',
    '71718770714',
    '72845562353',
    '72934003383',
    '73181128594',
    '73242073804',
    '72964485679',
    '73047625195',
    '73266562608',
    '73182767240',
    '72734745019',
    '72950286322',
    '72983315459',
    '72966122041',
    '72734935031',
    '72734827039',
    '72983265303',
    '72966275549',
    '72950086928',
    '73687404494',
    '73560261598',
    '72937867930',
    '73342702841',
    '73342452031',
    '73081827700',
    '74094674978',
    '73562116348',
    '73562158196',
    '74350684860',
    '74154494067',
    '74166417929',
    '74324332019',
    '73626794601',
    '74539270099',
    '74513382933',
    '72065580619',
    '74699030086',
    '74697782238',
    '74192924975',
    '74878411295',
    '73773899904',
    '74441629877',
    '74166610154',
    '75521109196',
    '75554010037',
    '75398257881',
    '75400296343',
    '75554425108',
    '72641837853',
    '74309426730',
    '74309255510',
    '75153284936',
    '74084925121',
    '74084501933',
    '74848965826',
    '74113509366',
    '74787640644',
    '75197573383',
    '75774792296',
    '74489296152',
    '74485340568',
    '74330547938',
    '74376657983',
] ## Actualizado hasta 16 de A bril
## Inicio de Analisis 
print("Iniciando Analisis")
print("Ajuste de datos...")
## Convertimos el id_transacion en tipo cadena y elimina los decimales en caso de generar
df_tra['id_transacion'] = df_tra['id_transacion'].astype(str)
df_tra['id_transacion'] = df_tra['id_transacion'].apply(lambda x: x[:-2]) 
## Lista para transacciones
transactions = []
## Obtener la lista de las transacciones que fueron identificadas como contracargo
for idtr in ctc:
  # Filtrar DataFrame por ID de transacción
  tr = df_tra[df_tra['id_transacion'] == idtr]
  # Agregar ID de usuario a la lista
  transactions.append(tr)
## Crear el dataframe de Transaciones de contracargo
trs = pd.concat(transactions, ignore_index=True)

## Obtener los id de usuarios de la lista de transacciones con contracargo
usuario_tra_uni = set(trs['user_id'])
##
user_c = []
##
for us in usuario_tra_uni:
    id_us = df_cards[df_cards['user_id'] == us]
    user_c.append(id_us)
##
usuarios_ctc = pd.concat(user_c, ignore_index=True)
# print(usuarios_ctc)
##
cards_unique = set(usuarios_ctc['card_number'])
# print(len(cards_unique))
for card in cards_unique:
  id_us = usuarios_ctc[usuarios_ctc['card_number'] == str(card.upper())]
##
cards_users = pd.concat(user_c, ignore_index=True)

# Create a dictionary to store user IDs and their associated card numbers
print("Creando JSON usuario-tarjetas...")
user_cards = {}
##
for user_id, card_number in zip(usuarios_ctc['user_id'], usuarios_ctc['card_number']):
    if user_id not in user_cards:
        user_cards[user_id] = set()  # Inicializa un conjunto vacío
    user_cards[user_id].add(card_number)
# Convierte los conjuntos a listas antes de la serialización
for user_id, card_numbers in user_cards.items():
    user_cards[user_id] = list(card_numbers)
#
with open(f'{ruta_trabajo}/usuario-tarjetas-{mes_nombre}.json', 'w') as archivo:
    json.dump(user_cards, archivo,indent=4)
##
print("Creando JSON tarjeta-usuarios...")
card_users = {}
##
for user_id, card_number in zip(df_cards['user_id'], usuarios_ctc['card_number']):
    if card_number not in card_users:
        card_users[card_number] = set()  # Initialize an empty set for unique card numbers
    card_users[card_number].add(user_id)  # Add card number to the set (duplicates won't be added)
# Convierte los conjuntos a listas antes de la serialización
for card_number,user_id in card_users.items():
    card_users[card_number] = list(user_id)
# Crea el JSON
with open(f'{ruta_trabajo}/tarjeta-usuarios-{mes_nombre}.json', 'w') as archivo:
    json.dump(card_users, archivo,indent=4)

trs['fecha_recarga_segundos'] = pd.to_datetime(trs['fecha_recarga'], format='%d/%m/%Y %H:%M').astype(np.int64) // 10**9
trs['fecha_recarga_segundos_mas_hora'] = trs['fecha_recarga_segundos'] + 3600

adip = trs[['id_transacion', 'user_id', 'monto_recarga', 'fecha_recarga', 'email', 'fecha_recarga_segundos_mas_hora']]


transa_mp = []

for card in cards_unique:
    df_mp['TIPO_TRANSACCION'] = df_mp['TIPO_TRANSACCION'].astype('str')
    df_filtro = df_mp[df_mp['TIPO_TRANSACCION'] == '0'].copy()
    df_appcdmx = df_filtro[df_filtro['LOCATION_ID'] == '101801']
    tra_mp = df_appcdmx[df_appcdmx['NUMERO_SERIE_HEX'] == str(card.upper())]
    transa_mp.append(tra_mp)
        
fnal = pd.concat(transa_mp,ignore_index=True)
# print(fnal)
fnal['FECHA_HORA_TRANSACCION_SEG'] = pd.to_datetime(fnal['FECHA_HORA_TRANSACCION']).astype(np.int64) // 10**9
mp = fnal[['ID_TRANSACCION_ORGANISMO', 'NUMERO_SERIE_HEX', 'FECHA_HORA_TRANSACCION', 'MONTO_TRANSACCION', 'FECHA_HORA_TRANSACCION_SEG']]
mp['MONTO_TRANSACCION'] = mp['MONTO_TRANSACCION'] / 100
# Initialize empty dictionary for results
resultados = []

# Define a threshold for considering a match
max_diferencia_permitida = 2400  # Adjust this value as needed
relacion_fechas = {}
# Main loop to iterate through 'fsg' dates
for i, fecha_fsg in enumerate(adip['fecha_recarga_segundos_mas_hora']):
    # Reset variables for each 'fsg' date
    minima_diferencia = float('inf')
    indice_minimo = None
    monto_fsg = adip['monto_recarga'].iloc[i]  # Get 'monto_recarga' for 'fecha_fsg'
    id_usuario_fsg = adip['user_id'].iloc[i]  # Get 'user_id' for 'fecha_fsg'
    id_tr = adip['id_transacion'].iloc[i] 
    lista_diferencias = {}
    # Nested loop to compare with 'fmp' dates
    for tr_org,fecha_fmp, monto_fmp,card_hex,fecha_mp in zip(mp['ID_TRANSACCION_ORGANISMO'],mp['FECHA_HORA_TRANSACCION_SEG'], mp['MONTO_TRANSACCION'],mp['NUMERO_SERIE_HEX'], mp['FECHA_HORA_TRANSACCION']):
        diferencia_actual = fecha_fmp - fecha_fsg
        if(diferencia_actual > 0):
            if(diferencia_actual <= max_diferencia_permitida):
                # lista_diferencias= (id_tr,tr_org,fecha_fsg,fecha_fmp,diferencia_actual,monto_fsg,monto_fmp)
                # print(lista_diferencias)
                if monto_fsg == monto_fmp:
                    # print(lista_diferencias)
                    if diferencia_actual < minima_diferencia:
                        lista_diferencias= (id_tr,tr_org,fecha_fsg,fecha_fmp,diferencia_actual,monto_fsg,monto_fmp)
                        # lista_diferencias= (fecha_fsg,fecha_fmp,diferencia_actual)
 
                        minima_diferencia = diferencia_actual

                        indice_minimo = i
                                  
                        id_user = adip['user_id'].iloc[i] 
                        email = adip['email'].iloc[i] 
                        fecha_adp = adip['fecha_recarga'].iloc[i] 
                        resultados.append( {
                                    'id_transacion':id_tr,
                                    'id_transacion_org': tr_org,
                                    'card': card_hex,
                                    'fecha_adp': fecha_adp,
                                    'fecha_mp': fecha_mp,
                                    'fecha_fsg': fecha_fsg,
                                    'fecha_fmp': fecha_fmp,
                                    'monto_fsg': monto_fsg,
                                    'monto_fmp': monto_fmp,
                                    'user_id':id_usuario_fsg,
                                    'email':email,
                                    }) 
                        print(f"{id_tr}-{monto_fsg}-{monto_fmp}-{tr_org}-{card_hex}-{diferencia_actual}")
    relacion_fechas[fecha_fsg] = lista_diferencias
# print(relacion_fechas)
resumen = pd.DataFrame(resultados)
print(resumen)
# ## Extenciones    
print("Generando datos extenciones")
archivo_tr_adip = f"Adip_CTC_{mes_nombre}.csv"
ruta_adip = os.path.join(ruta_trabajo, archivo_tr_adip)
trs.to_csv(ruta_adip, index=False)
# ## Extenciones    
print("Creando Relacion con MP")
archivo_tr_mp = f"MP_CTC_{mes_nombre}.csv"
ruta_mp = os.path.join(ruta_trabajo, archivo_tr_mp)
fnal.to_csv(ruta_mp, index=False)
##
print("Creando Resumen General")
archivo_tr_ctc = f"Resumen_CTC_{mes_nombre}.csv"
ruta_re = os.path.join(ruta_trabajo, archivo_tr_ctc)
resumen.to_csv(ruta_re, index=False)


print("Proceso Realizado con Exito!!")


## Paso 1 Realizar una resta para obtener una diferencia
## 1.1 - Descartar todas las diferencias que sean negativas
## 1.2 - Las diferencias positivas pasaran a ser revisadas al campo de monto, donde todas tienen que se iguales
## Paso 2 Realizar comparacion con montos
## 2.1 - Todas las que no sean iguales se descartan automaticamente
## 2.2 - Las Cantidades que sean iguales pasaran a revisar la diferencia minima o cercana a 0 
## Paso 3 matchear id_usuario  con card
## 3.1 - Tomar el id de usuario del dataframe de adip correspondiente a la fecha en segundos
## 3.2 - comparar el id_usuario con el diccionario y buscar su galeria de tarjetas con la minima comparada para ver si la tarjeta de esa recarga esta asignada a ese usuario
## Paso 4 Obtener la  minima y matchear
## 4.1 - Obtener la minima de las transacciones filtradas
## 4.2 - La diferencia minima matchearla por los campos de cada dataframe original.