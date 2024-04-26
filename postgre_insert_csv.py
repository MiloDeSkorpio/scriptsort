import pandas as pd
import psycopg2
import os

##
## nombre de la tabla
mes_nombre = "Abril"
m = "04"
y = "2024"
tabla = f"datos_{y}"
root = 'Validadores'
ruta_trabajo = f'{root}/{y}/{m} {mes_nombre}'
name_file = f"Mpeso_1ra qna Abril.csv"
# Parámetros de conexion
connection_string = {
    "host": "localhost",
    "database": "ORT",
    "user": "postgres",
    "password": "Hj2c#y8",
    "port": 5432,
}

connection = psycopg2.connect(**connection_string)

# Función para cargar los datos del DataFrame a la tabla sin conversiones
def load_data_to_table_direct(df, table_name, connection):
    try:
        default_date = '2000-01-01'
        df['CONTRACT_VALIDITY_START_DATE'] = df['CONTRACT_VALIDITY_START_DATE'].fillna(default_date)
        # Replace 'Invalid date' with '2000-01-01' where the value is 'Invalid date'
        df.loc[df['CONTRACT_VALIDITY_START_DATE'] == 'Invalid date', 'CONTRACT_VALIDITY_START_DATE'] = default_date

        df['FECHA_HORA_TRANSACCION'] = df['FECHA_HORA_TRANSACCION'].fillna(default_date)
        df = df.fillna(0) 
        # Obtener nombres de las columnas
        columns = list(df.columns)
        
        lowercase_columns = [name.lower() for name in columns]
        cursor = connection.cursor()
        datos = df.values

        querry = f"""
            INSERT INTO {table_name} ({", ".join(lowercase_columns)})
            VALUES ({", ".join(["%s"] * len(lowercase_columns))})
        """
        cursor.executemany(querry,datos.tolist())
        connection.commit()
        cursor.close()
        print(f"Se han cargado {df.shape[0]} filas a la tabla {table_name} del {mes_nombre}")
    except Exception as e:
        print(e.__class__.__name__, ":", e)

ruta_archivo = os.path.join(ruta_trabajo,name_file)
df = pd.read_csv(ruta_archivo,encoding='latin-1',low_memory=False)

if connection:
    print("Conexión exitosa")
    print(f"Llenando tabla {tabla} ...")
    load_data_to_table_direct(df, tabla, connection)

