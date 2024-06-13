import pandas as pd
from pandas import ExcelWriter
import os
## Define: mes ="Febrero" --- Nombre del mes
mes = "Abril"
## Define: m ="02"  ---- Numero del mes
m = "04"
## Define: y ="2024" --- Año a tomar en cuenta en el analisis
y = "2024"
## Rango de dias semanales L - V Agregando + 1 al viernes ** Leer documentacion metodo range

## ------- Definir datos de Entrada --------
ruta_trabajo = f"Transacciones/{y}/{m} {mes}/"
archivo = f'Full_{mes}.csv'
archivo = os.path.join(ruta_trabajo, archivo)
# Lectura del archivo de Entrada
df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')

# print(len(df['SAM_SERIAL_HEX'].unique().tolist()))
# print(df['SAM_SERIAL_HEX'].unique().tolist())
lista_sams = df['SAM_SERIAL_HEX'].unique().tolist()
lista_sams = sorted(lista_sams)

lista = f'Reporte_SAM´s_{mes}.xlsx'
ruta_lista = os.path.join(ruta_trabajo,lista)
with pd.ExcelWriter(ruta_lista) as writer:
  for sam in lista_sams:
      df_sam = df[df['SAM_SERIAL_HEX'] == sam]
      df_sam_ordenado = df_sam[['ID_TRANSACCION_ORGANISMO', 'CONTADOR_RECARGAS']].sort_values(by='CONTADOR_RECARGAS', ascending=True)
      df_sam_ordenado.to_excel(writer, index=False ,sheet_name=f'{sam}') 
          