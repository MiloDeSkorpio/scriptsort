import os
import pandas as pd
import glob

# Directorio donde se encuentran los archivos CSV y la cual sera la base de trabajo del Script
c = 'Validadores'
c2 = 'Validaciones'
periodo = '2da qna Mayo'
archivo_f = f'{c2}_{periodo}.csv'
ruta_guardado = f'{c}/{c2}/Mayo/2da qna'
archivos = glob.glob(os.path.join(ruta_guardado, '*.csv'))

df = pd.concat((pd.read_csv(archivo, dtype={'LOCATION_ID': str}, encoding='latin-1') for archivo in archivos), ignore_index=True)
df['LOCATION_ID'] = df['LOCATION_ID'].astype(str).str.zfill(width=1)

ruta_mpeso = os.path.join(ruta_guardado,archivo_f)
df.to_csv(ruta_mpeso, index=False)