import pandas as pd
import psycopg2
import os

##
## nombre de la tabla
mes_nombre = "Marzo"
m = "03"
y = "2022"
tabla = f"datos_{y}"
root = 'Transacciones'
ruta_trabajo = f'{root}/{y}/{m} {mes_nombre}'
name_file = "Marzo_crudo.csv"
# Parámetros de conexion
connection_string = {
    "host": "localhost",
    "database": "ORT",
    "user": "postgres",
    "password": "Hj2c#y8",
    "port": 5432,
}

# Función para manejar la conexión a la base de datos
def connect_to_db(connection_string):
    try:
        return psycopg2.connect(**connection_string)
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para cargar los datos del DataFrame a la tabla sin conversiones
def load_data_to_table_direct(df, table_name, connection):
    try:
        # Handling missing values (example: fill with 0)
        default_date = '2000-01-01'
        df['CONTRACT_VALIDITY_START_DATE'] = df['CONTRACT_VALIDITY_START_DATE'].fillna(default_date)
        df = df.fillna(0)  # Adjust as neede
        # Obtener nombres de las columnas
        columns = list(df.columns)
        
        lowercase_columns = [name.lower() for name in columns]
        # print(lowercase_columns)
        # Ejecutar la consulta INSERT
        cursor = connection.cursor()
        ##
        datos = df.values
        ##
        querry = f"""
            INSERT INTO {table_name} ({", ".join(lowercase_columns)})
            VALUES ({", ".join(["%s"] * len(lowercase_columns))})
             
            ;
        """
        # print(querry)
        cursor.executemany(querry,datos.tolist())
        connection.commit()
        cursor.close()
        print(f"Se han cargado {df.shape[0]} filas a la tabla {table_name}")
    except Exception as e:
        print(e.__class__.__name__, ":", e)


# Leer archivo CSV

ruta_archivo = os.path.join(ruta_trabajo,name_file)
df = pd.read_csv(ruta_archivo)
# print(df.columns)
# Conectar a la base de datos
connection = connect_to_db(connection_string)
print(df['FECHA_HORA_TRANSACCION'])
# Cargar datos a la tabla sin conversiones
if connection:
    print("Conexión exitosa")
    print("Llenando tabla de Recargas ...")
    load_data_to_table_direct(df, tabla, connection)

