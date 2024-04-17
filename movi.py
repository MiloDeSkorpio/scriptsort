import pandas as pd
import os


ruta_trabajo = 'Transacciones/Transacciones_Limpias_2Quin_Marzo_2024'
    
archivo = 'CB_2024-03-Q2.csv'
archivo_path = os.path.join(ruta_trabajo,archivo) 
df_cb = pd.read_csv(archivo_path,low_memory=False)
# Agregar encabezados estandarizados
df_cb.columns = ["organismo", "csdec", "fecha_hora", "operacion", "monto", "saldo_final", "loc_id"]

df_cb['fecha_hora'] = pd.to_datetime(df_cb['fecha_hora'])
df_cb['fecha_hora'] = df_cb['fecha_hora'].dt.strftime('%Y-%m-%d')
#
print(len(df_cb['loc_id']))
new_ids = []
for lid in df_cb['loc_id']:
    nid = str(lid)
    new_ids.append(nid[:-3])
# Print the DataFame with the new 'loc_id_modified' column (without index)
df_cb['loc_id_m'] = new_ids 
print(df_cb['loc_id_m'].value_counts())
d1 = '2024-03-19'
d2 = '2024-03-20'
d3 = '2024-03-21'
df_cb_d1 = df_cb[df_cb['fecha_hora'] == d1]
df_cb_d2 = df_cb[df_cb['fecha_hora'] == d2]
df_cb_d3 = df_cb[df_cb['fecha_hora'] == d3]
print(len(df_cb_d1))
print(len(df_cb_d2))
print(len(df_cb_d3))
print(sum(df_cb_d1['monto']))
print(sum(df_cb_d2['monto']))
print(sum(df_cb_d3['monto']))
# print(organismo)

# leer_csv('STC_2024-03-Q2.csv','Metro')
# leer_csv('MB_2024-03-Q2.csv','Metrobus')
# leer_csv('STE_2024-03-Q2.csv','Tren Ligero')


