import pandas as pd
import os

# Define month names and codes
mes = "Mayo"
m = "05"
y = "2024"

parque_vehicular = {
  'MIIT': 142, 
  'SAUSA': 66, 
  'ATROLSA': 57, 
  'CEUSA': 65, 
  'AULSA': 62,
  'CODIVERSA': 54, 
  'COTAXOMIL': 129, 
  'ABC': 76, 
  'MOVIN': 86
    }
# Set of days to process
l = 23
# Viernes + 1
v = 18
dias_es = l
# dias_ord = sorted(dias_es)
s = 25
d = 26

# Valid bus lines
lineas_valid = {
    'MIIT',
    'SAUSA',
    'ATROLSA',
    'CEUSA',
    'AULSA',
    'CODIVERSA',
    'COTAXOMIL',
    'ABC',
    'MOVIN',
}
lin_ord = sorted(lineas_valid)
rango = '20 al 26'
# Define company and file path
empresa = 'ORT'
ruta_trabajo = f"Validadores/{y}/{m} {mes}/"
archivo = 'Validaciones del 20 al 26 de mayo 2024.csv'
archivo = os.path.join(ruta_trabajo, archivo)

# Read data from CSV
df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')

# Filter transactions of type '3' and replace line codes
df['TIPO_TRANSACCION'] = df['TIPO_TRANSACCION'].astype(str)
df_bus_val = df[df['TIPO_TRANSACCION'] == '3']
reemplazos = {
    '1': 'MIIT',
    '2': 'SAUSA',
    '3': 'ATROLSA',
    '4': 'CEUSA',
    '7': 'AULSA',
    '11': 'CODIVERSA',
    '14':'COTAXOMIL',
    '15': 'ABC',
    '16': 'MOVIN',
 }# Assuming '...' represents remaining replacements
for codigo, reemplazo in reemplazos.items():
    df_bus_val.replace({'LINEA': codigo}, reemplazo, inplace=True)

# Final result structure
re_lv = []

# Loop through valid lines
for linea in lin_ord:
    df_corr = df_bus_val[df_bus_val['LINEA'] == linea]
    data = {'Concesionario': linea, 'Parque Vehicular Total': parque_vehicular[linea]}  # Dictionary to store data for current line

    # Loop through days and hours, counting active buses per time slot
    # for dia in dias_es:
    for hora in range(0, 24):
        inicio = f"{l}/{m}/{y} {hora:02d}:00:00"
        fin = f"{l}/{m}/{y} {(hora+1):02d}:00:00"
        df_hora = df_corr[(df_corr['FECHA_HORA_TRANSACCION'] >= inicio) & (df_corr['FECHA_HORA_TRANSACCION'] < fin)]
        data[f"{hora:02d}:00"] = len(df_hora['AUTOBUS'].unique())

    # Append data for current line to the results
    re_lv.append(data)

# Create Pandas DataFrame from results
resumen_lv = pd.DataFrame(re_lv)



res = []

# Loop through valid lines
for linea in lin_ord:
    df_corr = df_bus_val[df_bus_val['LINEA'] == linea]
    data = {'Concesionario': linea, 'Parque Vehicular Total': parque_vehicular[linea]}  # Dictionary to store data for current line

    # Loop through days and hours, counting active buses per time slot

    for hora in range(0, 24):
        inicio = f"{s}/{m}/{y} {hora:02d}:00:00"
        fin = f"{s}/{m}/{y} {(hora+1):02d}:00:00"
        df_hora = df_corr[(df_corr['FECHA_HORA_TRANSACCION'] >= inicio) & (df_corr['FECHA_HORA_TRANSACCION'] < fin)]
        data[f"{hora:02d}:00"] = len(df_hora['AUTOBUS'].unique())

    # Append data for current line to the results
    res.append(data)

# Create Pandas DataFrame from results
resumen_s = pd.DataFrame(res)

red = []

# Loop through valid lines
for linea in lin_ord:
    df_corr = df_bus_val[df_bus_val['LINEA'] == linea]
    data = {'Concesionario': linea, 'Parque Vehicular Total': parque_vehicular[linea]}  # Dictionary to store data for current line

    # Loop through days and hours, counting active buses per time slot

    for hora in range(0, 24):
        inicio = f"{d}/{m}/{y} {hora:02d}:00:00"
        fin = f"{d}/{m}/{y} {(hora+1):02d}:00:00"
        df_hora = df_corr[(df_corr['FECHA_HORA_TRANSACCION'] >= inicio) & (df_corr['FECHA_HORA_TRANSACCION'] < fin)]
        data[f"{hora:02d}:00"] = len(df_hora['AUTOBUS'].unique())

    # Append data for current line to the results
    red.append(data)

# Create Pandas DataFrame from results
resumen_d = pd.DataFrame(red)

# Define output filename and path
fn = f'RE_BUS_{empresa}_{mes}_{rango}.xlsx'
ruta_doc = os.path.join(ruta_trabajo, fn)

# Write DataFrame to Excel file
with pd.ExcelWriter(ruta_doc) as writer:
    resumen_lv.to_excel(writer, index=False, sheet_name=f'AUTOBUS_L-V')
    resumen_s.to_excel(writer, index=False, sheet_name=f'AUTOBUS_S')
    resumen_d.to_excel(writer, index=False, sheet_name=f'AUTOBUS_D')


