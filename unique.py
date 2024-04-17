import pandas as pd

# Suponiendo que las fechas están en columnas separadas ('fecha1' y 'fecha2') en DataFrames 'df1' y 'df2'

# Convertir fechas a segundos
uno = 1707672290
dos = 1707672120
res = uno - dos  
print(res)