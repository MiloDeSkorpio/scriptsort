# import os
# import pandas as pd

# ## Definimos el mes con nombre
# mes = "Febrero"
# ## Definimos el mes con número
# m = "02"
# ## Definimos el año
# y = "2024"

# c = 'Conduent'
# c2 = '2da qna febrero'
# ## La ruta de trabaajo es la ruta donde se leen y se generan los archivos
# ruta_trabajo = f"Validadores/{y}/{c2}"

# ## Es el periodo en el que se realiza el analisis
# periodo = "2da qna febrero"

# ## Archivo a subir 
# file_to_upload = 'Validaciones 2da qna febrero 2024.csv'

# ## metodo para asignar la ruta al archivo
# archivo = os.path.join(ruta_trabajo, file_to_upload)
# df = pd.read_csv(archivo, low_memory=False, encoding='latin-1')
# df['ID_TRANSACCION_ORGANISMO'] = df['ID_TRANSACCION_ORGANISMO'].str.replace('.', '')

# archivo_mp = f"{c}_{periodo}.csv"
# ruta_mp = os.path.join(ruta_trabajo,archivo_mp)
# df.to_csv(ruta_mp, index=False)
# print(df)
import plotly.graph_objects as go

# Ejemplo de uso
fig = go.Figure()
fig.add_trace(go.Bar(x=[1, 2, 3], y=[4, 5, 6]))
fig.update_layout(xaxis=dict(title='Eje X'))

# Agregar una tabla debajo del label del eje X
table = go.Table(header=dict(values=['Columna 1', 'Columna 2']),
                  cells=dict(values=[[1, 2], [3, 4]]))
fig.add_layout_image(table, xref='x', yref='paper', x=0, y=1.05, sizex=1, sizey=1)

fig.show()



