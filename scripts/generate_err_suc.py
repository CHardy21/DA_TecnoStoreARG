import pandas as pd
import numpy as np

# Cargar la dimensión sucursales limpia generada por tu script principal
df_sucursales = pd.read_csv("data/raw/sucursales.csv")

# Inyectar errores simulados
# 1. Duplicar una fila
df_sucursales_err = pd.concat([df_sucursales, df_sucursales.iloc[[0]]], ignore_index=True)

# 2. Introducir typos en provincia
df_sucursales_err.loc[1, "provincia_sucursal"] = "Bunoes Aires"
df_sucursales_err.loc[2, "provincia_sucursal"] = "Cordoba"

# 3. Espacios extra
df_sucursales_err.loc[3, "provincia_sucursal"] = "Santa Fe "

# 4. Nulo intencional
df_sucursales_err.loc[4, "provincia_sucursal"] = np.nan

print(">>> Sucursales con errores simulados:")
print(df_sucursales_err.head())

# Guardar CSV con errores
df_sucursales_err.to_csv("data/raw/sucursales_err.csv", index=False)
print("✅ Archivo sucursales_err.csv guardado en data/raw/")

