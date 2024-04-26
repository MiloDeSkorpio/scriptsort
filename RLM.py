import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Generar datos aleatorios
np.random.seed(10)

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
transacciones_app = np.random.randint(100, 500, len(dias))
monto_app = np.random.randint(1000, 5000, len(dias))
transacciones_pasarela = np.random.randint(50, 250, len(dias))
monto_pasarela = np.random.randint(500, 2500, len(dias))
crecimiento = np.random.randint(5, 20, len(dias))

# Crear DataFrame
datos = pd.DataFrame({
    "Dia": dias,
    "Transacciones_App": transacciones_app,
    "Monto_App": monto_app,
    "Transacciones_Pasarela": transacciones_pasarela,
    "Monto_Pasarela": monto_pasarela,
    "Crecimiento": crecimiento
})

# Codificar variable categórica "Dia"
datos_dummy = pd.get_dummies(datos["Dia"])
datos = pd.concat([datos, datos_dummy], axis=1)
datos.drop("Dia", axis=1, inplace=True)

# Separar variables dependiente e independientes
X = datos[["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo", "Transacciones_App", "Monto_App", "Transacciones_Pasarela", "Monto_Pasarela"]]
y = datos["Crecimiento"]

# Ajustar modelo de regresión lineal múltiple
modelo = LinearRegression()
modelo.fit(X, y)

# Imprimir coeficientes
print("Coeficientes:")
print(modelo.coef_)

# Interpretar coeficientes
# ... (Interpretar la magnitud y significancia de cada coeficiente)

# Realizar predicciones
dia_nuevo = np.array([ 200, 3000, 100, 1500])
prediccion = modelo.predict([dia_nuevo])
print("Crecimiento predicho para el Sabado con 200 transacciones App, $3000 monto App, 100 transacciones Pasarela y $1500 monto Pasarela:", prediccion[0])