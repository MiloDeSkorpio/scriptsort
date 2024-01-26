import os
import pandas as pd
import glob

# Directorio donde se encuentran los archivos CSV y la cual sera la base de trabajo del Script
c = 'Validadores'
c2 = 'Mpeso'
periodo = '15-21'
archivo_f = f'Mpeso_{periodo}.csv'
ruta_guardado = f'{c}/{c2}'
archivos = glob.glob(os.path.join(ruta_guardado, '*.csv'))

df = pd.DataFrame()
for archivo in archivos:
  with open(archivo, 'r') as f:
    df = df._append(pd.read_csv(f), ignore_index=True)

# Escribe el archivo CSV
ruta_mpeso = os.path.join(ruta_guardado,archivo_f)
df.to_csv(ruta_mpeso, index=False)
