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
    # '71240815536',
    # '71286149582',
    # '73560261598',
    # '73342702841',
    # '73342452031',
    # '73562116348',
    # '73562158196',
    # '73687404494',
    # '73773899904',
    # '73626794601',
    # '74094674978',
    # '74113509366',
    # '74166610154',
    # '74309426730',
    # '74309255510',
    # '74084925121',
    # '74084501933',
    # '74350684860',
    # '74154494067',
    # '74330547938',
    # '74166417929',
    # '74192924975',
    # '74489296152',
    # '74485340568',
    # '74272965467',
    # '74324332019',
    # '74565604300',
    # '74376657983',
    # '74697782238',
    # '74441629877',
    # '74539270099',
    # '74513382933',
    # '74699030086',
    # '74787640644',
    # '74848965826',
    # '75019459736',
    # '74878411295',
    # '74867924439',
    # '75153284936',
    # '75197573383',
    # '75172211945',
    # '75521109196',
    # '75554425108',
    # '75398257881',
    # '75400296343',
    # '75563922894',
    # '75386490981',
    # '75554010037',
    # '75774792296',
    # '75944095248',
    # '75737235731',
    # '75723081623',
    # '75771976741',
    # '76004002886',
    # '76066321250',
    # '76112018340',
    # '76139221958',
    # '75956430945',
    # '75956280629',
    # '76271150182',
    # '76059425385',
'72983586385',
'72735475247',
'72950793418',
'73183353472',
'72966784115',
'73179644716'
] ## Actualizado hasta 23 de Abril



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
# print(cards_unique)
cards_fixed = []
# print(len(cards_unique))
for card in cards_unique:
    if len(card) <= 16:
        card_padded = card.zfill(16)  # Agrega ceros a la izquierda para completar 16 caracteres
        # Imprime la longitud de la tarjeta con relleno
        ma_card = card_padded.upper()
        cards_fixed.append(ma_card)


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
        card_users[card_number] = set()  
    card_users[card_number].add(user_id)  

for card_number,user_id in card_users.items():
    card_users[card_number] = list(user_id)

with open(f'{ruta_trabajo}/tarjeta-usuarios-{mes_nombre}.json', 'w') as archivo:
    json.dump(card_users, archivo,indent=4)

trs['fecha_recarga_segundos'] = pd.to_datetime(trs['fecha_recarga'], format='%d/%m/%Y %H:%M').astype(np.int64) // 10**9
trs['fecha_recarga_segundos_mas_hora'] = trs['fecha_recarga_segundos'] + 3600

adip = trs[['id_transacion', 'user_id', 'monto_recarga', 'fecha_recarga', 'email', 'fecha_recarga_segundos_mas_hora']]


transa_mp = []

for card in cards_fixed:
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
                if monto_fsg == monto_fmp:
                    if diferencia_actual < minima_diferencia:
                        lista_diferencias= (id_tr,tr_org,fecha_fsg,fecha_fmp,diferencia_actual,monto_fsg,monto_fmp)
                        minima_diferencia = diferencia_actual
                        indice_minimo = i
                        t_card = card_hex.zfill(16)
                        id_user = adip['user_id'].iloc[i] 
                        email = adip['email'].iloc[i] 
                        fecha_adp = adip['fecha_recarga'].iloc[i] 
                        resultados.append( {
                                    'id_transacion':id_tr,
                                    'id_transacion_org': tr_org,
                                    'card': t_card,
                                    'fecha_adp': fecha_adp,
                                    'fecha_mp': fecha_mp,
                                    'fecha_fsg': fecha_fsg,
                                    'fecha_fmp': fecha_fmp,
                                    'monto_fsg': monto_fsg,
                                    'monto_fmp': monto_fmp,
                                    'user_id':id_usuario_fsg,
                                    'email':email,
                                    }) 
                        
    relacion_fechas[fecha_fsg] = lista_diferencias
# print(relacion_fechas)
resumen = pd.DataFrame(resultados)
# print(resumen)
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
