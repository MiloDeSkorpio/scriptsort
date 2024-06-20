import pandas as pd
import os
## Define: mes ="Febrero" --- Nombre del mes
mes = "Mayo"
## Define: m ="02"  ---- Numero del mes
m = "05"
## Define: y ="2024" --- Año a tomar en cuenta en el analisis
y = "2024"
## Rango de dias semanales L - V Agregando + 1 al viernes ** Leer documentacion metodo range

## ------- Definir datos de Entrada --------
ruta_trabajo = f"Transacciones/{y}/{m} {mes}/"
# archivo = f'{mes}_crudo_2023.csv'
archivo = f'Full_{mes}.csv'
archivo = os.path.join(ruta_trabajo, archivo)
# Lectura del archivo de Entrada
df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')

print(df[df['TIPO_TRANSACCION'] == '50'])