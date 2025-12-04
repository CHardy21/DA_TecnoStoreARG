import pandas as pd
import numpy as np
from datetime import date, timedelta
import random
from faker import Faker

fake = Faker('es_AR')

# --- 1. Tiempo y períodos ---
start_date = date(2018, 1, 1)
end_date = date(2024, 12, 31)
dates = pd.date_range(start=start_date, end=end_date, freq='D')

PANDEMIC_START_DATE = pd.to_datetime('2020-03-01')
POST_PANDEMIC_START_DATE = pd.to_datetime('2022-01-01')

# --- 2. Cargar IPC mensual oficial ---
ipc_df = pd.read_excel("data/Indice-FACPCE-Res.-JG-539-18-_2025-05.xlsx", header=None)
ipc_df.columns = ["fecha", "ipc"]
ipc_df['fecha'] = pd.to_datetime(ipc_df['fecha'], format='%b-%y', errors='coerce')
ipc_df = ipc_df.dropna(subset=['fecha', 'ipc'])
ipc_df['año'] = ipc_df['fecha'].dt.year
ipc_df['mes'] = ipc_df['fecha'].dt.month
ipc_df = ipc_df[(ipc_df['fecha'] >= "2018-01-01") & (ipc_df['fecha'] <= "2024-12-31")]

mask = (ipc_df['año'] == 2018) & (ipc_df['mes'] == 1)
ipc_base = ipc_df.loc[mask, 'ipc'].values[0] if mask.any() else ipc_df['ipc'].iloc[0]
print(f"✅ IPC base: {ipc_base}")
print(f"🧾 Filas IPC: {len(ipc_df)}")

# --- 3. Eventos promocionales ---
def hot_sale_dates(year):
    may = pd.date_range(f'{year}-05-01', f'{year}-05-31', freq='D')
    second_monday = may[may.weekday == 0][1] if len(may[may.weekday == 0]) >= 2 else may[0]
    return [second_monday, second_monday + timedelta(days=1), second_monday + timedelta(days=2)]

def cyber_black_dates(year):
    nov = pd.date_range(f'{year}-11-01', f'{year}-11-10', freq='D')
    # lunes de la primera semana de noviembre
    mondays = nov[nov.weekday == 0]
    monday = mondays[0] if len(mondays) >= 1 else nov[0]
    return [monday, monday + timedelta(days=1), monday + timedelta(days=2)]


events_by_date = set()
for y in range(2018, 2025):
    for d in hot_sale_dates(y) + cyber_black_dates(y):
        events_by_date.add(pd.to_datetime(d))

# --- 4. Dimensión Productos ---
productos = []
categorias = {
    'Tecnologia': {
        'Computo': ['Laptop Premium', 'Desktop Gamer', 'Monitor 27"', 'Teclado Mecánico', 'Mouse Gamer'],
        'Moviles': ['Smartphone Alta Gama', 'Smartphone Media Gama', 'Tablet Pro', 'Smartwatch', 'Auriculares'],
        'TV & Entretenimiento': ['Smart TV 55"', 'Smart TV 65"', 'Consola Gaming', 'Chromecast']
    },
    'Linea Blanca': {
        'Refrigeracion': ['Heladera No Frost', 'Freezer'],
        'Lavado': ['Lavadora', 'Secadora'],
        'Cocina': ['Cocina Vitrocerámica', 'Microondas'],
        'Climatizacion': ['Aire Acondicionado', 'Calefactor']
    },
    'Pequeños Electro': {
        'Cocina & Hogar': ['Cafetera', 'Licuadora', 'Aspiradora Robot', 'Plancha'],
        'Cuidado Personal': ['Corta Pelo', 'Secador']
    }
}

price_map = {
    'Laptop Premium': 30000, 'Desktop Gamer': 40000, 'Monitor 27"': 8000, 'Teclado Mecánico': 2500, 'Mouse Gamer': 1500,
    'Smartphone Alta Gama': 25000, 'Smartphone Media Gama': 12000, 'Tablet Pro': 15000, 'Smartwatch': 6000, 'Auriculares': 3500,
    'Smart TV 55"': 20000, 'Smart TV 65"': 28000, 'Consola Gaming': 15000, 'Chromecast': 2000,
    'Heladera No Frost': 22000, 'Freezer': 18000, 'Lavadora': 19000, 'Secadora': 17000,
    'Cocina Vitrocerámica': 15000, 'Microondas': 4500, 'Aire Acondicionado': 27000, 'Calefactor': 4000,
    'Cafetera': 4500, 'Licuadora': 3000, 'Aspiradora Robot': 8000, 'Plancha': 2000,
    'Corta Pelo': 1500, 'Secador': 2000
}

producto_id = 1
for cat, subs in categorias.items():
    for subcat, nombres in subs.items():
        for nombre in nombres:
            productos.append({
                'producto_id': producto_id,
                'nombre_producto': nombre,
                'categoria': cat,
                'subcategoria': subcat,
                'precio_base_ars_2018': price_map[nombre]
            })
            producto_id += 1

df_productos = pd.DataFrame(productos)
df_productos.to_csv('data/raw/productos.csv', index=False)

# --- 5. Dimensión Clientes ---
n_clientes = 15000
segmentos = ['Premium', 'Frecuente', 'Ocasional', 'Nuevo']
df_clientes = pd.DataFrame({
    'cliente_id': range(1, n_clientes + 1),
    'nombre_cliente': [fake.name() for _ in range(n_clientes)],
    'email_cliente': [fake.email() for _ in range(n_clientes)],
    'ciudad_cliente': [fake.city() for _ in range(n_clientes)],
    'segmento_base': np.random.choice(segmentos, size=n_clientes, p=[0.12,0.36,0.32,0.20])
})
df_clientes.to_csv('data/raw/clientes.csv', index=False)

# --- 6. Dimensión Sucursales ---
provincias_argentinas = ['Buenos Aires','Chaco','Córdoba','Mendoza','Santa Fe','Tucumán','Salta','Misiones','Neuquén','Río Negro']
n_sucursales = 25
df_sucursales = pd.DataFrame({
    'sucursal_id': range(1, n_sucursales + 1),
    'nombre_sucursal': [f'Sucursal {i+1}' for i in range(n_sucursales)],
    'direccion_sucursal': [fake.address().replace('\n', ', ') for _ in range(n_sucursales)],
    'provincia_sucursal': random.choices(provincias_argentinas, k=n_sucursales)
})
df_sucursales.to_csv('data/raw/sucursales.csv', index=False)

# --- 7. Dimensión Canales ---
df_canales = pd.DataFrame({'canal_id':[1,2],'nombre_canal':['Online','Sucursal Fisica']})
df_canales.to_csv('data/raw/canales.csv', index=False)

# --- 8. Dimensión Fecha ---
df_fecha = pd.DataFrame({'fecha': dates})
df_fecha['año'] = df_fecha['fecha'].dt.year
df_fecha['mes'] = df_fecha['fecha'].dt.month
df_fecha['dia'] = df_fecha['fecha'].dt.day
df_fecha['nombre_mes'] = df_fecha['fecha'].dt.strftime('%B')
df_fecha['nombre_dia_semana'] = df_fecha['fecha'].dt.strftime('%A')
df_fecha['trimestre'] = df_fecha['fecha'].dt.quarter
df_fecha['semana_del_año'] = df_fecha['fecha'].dt.isocalendar().week.astype(int)
df_fecha['es_evento'] = df_fecha['fecha'].isin(events_by_date).astype(int)
df_fecha.to_csv('data/raw/fecha.csv', index=False)

# --- 9. Funciones de generación ---
def daily_base_transactions(current_date):
    y = current_date.year
    if y < 2020:
        base = 200
    elif y < 2022:
        base = 400
    else:
        base = 340

    # Estacionalidad semanal
    wd = current_date.weekday()
    if wd in [4, 5]:      # viernes, sábado
        base *= 1.15
    elif wd == 6:         # domingo
        base *= 0.9

    # Primeros 90 días de pandemia: efecto cierre físico
    if PANDEMIC_START_DATE <= current_date < PANDEMIC_START_DATE + timedelta(days=90):
        base *= 0.85

    # Eventos: Hot Sale / Cyber
    if current_date in events_by_date:
        base *= random.uniform(1.8, 2.2)

    # Ruido aleatorio
    base = int(np.random.normal(base, base * 0.15))
    return max(1, base)


def online_share(current_date):
    if current_date < PANDEMIC_START_DATE:
        share = 0.15
    elif current_date < POST_PANDEMIC_START_DATE:
        delta_days = (current_date - PANDEMIC_START_DATE).days
        total_pandemic_days = (POST_PANDEMIC_START_DATE - PANDEMIC_START_DATE).days
        share = 0.15 + (0.55 * (delta_days / total_pandemic_days))
    else:
        share = 0.58 + np.random.uniform(-0.05, 0.05)

    # Eventos: mayor peso online
    if current_date in events_by_date:
        share += 0.12

    # Limitar entre 0.05 y 0.95
    return min(max(share, 0.05), 0.95)


# --- 10. Generación de tabla de hechos (año por año) ---
transaction_id = 1

for year in range(2018, 2025):
    ventas_list = []
    dates_year = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
    print(f"➡️ Generando {year} ({len(dates_year)} días)")

    for i, current_date in enumerate(dates_year):
        n_trx = daily_base_transactions(current_date)
        o_share = online_share(current_date)
        month = current_date.month

        if i % 30 == 0:
            print(f"   Día {current_date.date()} ({i}/{len(dates_year)}), {n_trx} transacciones previstas")

        for _ in range(n_trx):
            cliente_id = random.randint(1, n_clientes)
            producto_id = random.choice(df_productos['producto_id'].tolist())

            # Canal y sucursal
            if random.random() < o_share:
                canal_id = 1  # Online
                sucursal_id = np.nan
            else:
                canal_id = 2  # Físico
                sucursal_id = random.randint(1, n_sucursales)

            # Cantidad
            cantidad = np.random.choice([1, 1, 1, 2, 2, 3])

            # Precio nominal en ARS
            precio_base_2018 = df_productos.loc[df_productos['producto_id']==producto_id,'precio_base_ars_2018'].iloc[0]
            mask = (ipc_df['año']==year) & (ipc_df['mes']==month)
            ipc_mes = ipc_df.loc[mask,'ipc'].values[0] if mask.any() else ipc_base

            precio_nominal = precio_base_2018 * (ipc_mes / ipc_base)
            if current_date in events_by_date:
                precio_nominal *= random.uniform(0.85, 0.95)
            precio_nominal *= random.uniform(0.97, 1.03)

            monto_nominal = round(precio_nominal * cantidad, 2)
            monto_real = round(monto_nominal * (ipc_base / ipc_mes), 2)

            ventas_list.append({
                'transaction_id': transaction_id,
                'fecha': current_date,
                'año': year,
                'mes': month,
                'cliente_id': cliente_id,
                'producto_id': producto_id,
                'canal_id': canal_id,
                'sucursal_id': sucursal_id,
                'cantidad': int(cantidad),
                'precio_unitario_ars_nominal': round(precio_nominal, 2),
                'monto_venta_ars_nominal': monto_nominal,
                'monto_venta_ars_real_2018': monto_real,
                'es_evento': int(current_date in events_by_date)
            })
            transaction_id += 1

    # Guardar chunk por año
    df_fact_ventas_year = pd.DataFrame(ventas_list)
    df_fact_ventas_year.to_csv(f"data/raw/fact_ventas_{year}.csv", index=False)
    print(f"✅ {year} generado con {len(df_fact_ventas_year)} transacciones")
