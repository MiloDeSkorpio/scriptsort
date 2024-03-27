import os
import pandas as pd

## La ruta de trabaajo es la ruta donde se leen y se generan los archivos
ruta_trabajo = f"Transacciones/ADIP/2024-03-03 BD AppCDMX"

## Es el periodo en el que se realiza el analisis
periodo = "04 al 10"

## metodo para asignar la ruta al archivo
cards_numbers = 'card_numbers_feb_24.csv'
archivo_c = os.path.join(ruta_trabajo, cards_numbers)
df_cards = pd.read_csv(archivo_c, low_memory=False, encoding='latin-1')
## metodo para asignar la ruta al archivo
bd = 'mp_info_01-29_02_2024.csv'
archivo_bd = os.path.join(ruta_trabajo, bd)
df_tr = pd.read_csv(archivo_bd, low_memory=False, encoding='latin-1')

print(df_tr['id_transacion'])
df_tr['id_transacion'] = df_tr['id_transacion'].astype(str)
df_tr['id_transacion'] = df_tr['id_transacion'].apply(lambda x: x[:-2])
print(df_tr['id_transacion'])

unique_user = df_tr['user_id'].unique()
unique_card = df_cards['card_number'].unique()

print(len(unique_user))
print(len(unique_card))

# Lista de identificadores de transacción
ctc = [
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
'72937867930',
'73081827700']

# Lista para almacenar IDs de usuarios
usuarios = []
emails = []
# Recorrer cada ID de transacción
for idtr in ctc:

  # Filtrar DataFrame por ID de transacción
  tr = df_tr[df_tr['id_transacion'] == idtr]

  # Obtener ID de usuario
  id_user = tr['user_id']
  email_uer = tr['email']
  # Imprimir información para depuración (opcional)
  print(tr)
  print(id_user)

  # Agregar ID de usuario a la lista
  usuarios.append(id_user)
  emails.append(email_uer)


usuari = pd.concat(usuarios, ignore_index=True)
emas = pd.concat(emails, ignore_index=True)

usuarios_uniq = usuari.unique()
emas_uniq = emas.unique()
print(usuarios_uniq)
print(emas.value_counts())
print(emas_uniq)

# user_c = []
# for us in usuari:
#     id_us = df_cards[df_cards['user_id'] == us]
    
#     print(id_us)
    
#     user_c.append(id_us)
#     cards = pd.concat(user_c, ignore_index=True)

# usuari = pd.concat(usuarios, ignore_index=True)   
  
# print(usuari)








# print(cards_em.values_counts())
