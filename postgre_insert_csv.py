import pandas as pd
import psycopg2

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
        unique_col = columns[0]
        # Ejecutar la consulta INSERT
        cursor = connection.cursor()
        ##
        datos = df.values
        ##
        querry = f"""
            INSERT INTO {table_name} ({", ".join(columns)})
            VALUES ({", ".join(["%s"] * len(columns))}) 
            ON CONFLICT ({unique_col}) DO NOTHING;
        """
        # print(querry)
        cursor.executemany(querry,datos.tolist())
        connection.commit()
        cursor.close()
        print(f"Se han cargado {df.shape[0]} filas a la tabla {table_name}")
    except Exception as e:
        print(f"Error al cargar los datos: {e}")


# Parámetros de conexion
connection_string = {
    "host": "localhost",
    "database": "ort_csv",
    "user": "postgres",
    "password": "Hj2c#y8",
    "port": 5432,
}
## nombre de la tabla
table_name_recargas = "recargas_csv_files_info"
table_name_validaciones = "validaciones_csv_files_info"

# Leer archivo CSV
dfv = pd.read_csv("Validaciones 2da qna enero 2024.csv",low_memory=False, encoding='latin-1')
df = pd.read_csv("Octubre_crudo_2023.csv")

# Conectar a la base de datos
connection = connect_to_db(connection_string)

# Cargar datos a la tabla sin conversiones
if connection:
    print("Conexión exitosa")
    print("Llenando tabla de Recargas ...")
    load_data_to_table_direct(df, table_name_recargas, connection)
    print("Llenando tabla de Validaciones ...")
    load_data_to_table_direct(dfv, table_name_validaciones, connection)
