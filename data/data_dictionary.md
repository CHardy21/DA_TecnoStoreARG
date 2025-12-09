# Data Dictionary – Modelo Estrella
## *Tabla de Hechos: fact_ventas.csv*

| Columna	| Tipo	| Descripción |
| --- | --- | --- |
| transaction_id |	int	 | Identificador único de la transacción.
|fecha	|date	|Fecha de la transacción. Llave foránea hacia dim_fecha.
|año	|int	|Año de la transacción.
|mes	|int	|Mes de la transacción.
|cliente_id	|int	|Llave foránea hacia dim_clientes.
|segmento_cliente	|string	|Segmento asignado dinámicamente según año (Premium, Frecuente, Ocasional, Nuevo).
|producto_id	|int	|Llave foránea hacia dim_productos.
|canal_id	|int	|Llave foránea hacia dim_canales.
|sucursal_id	|int/NaN	|Llave foránea hacia dim_sucursales. NaN si la venta fue online.
|cantidad	|int	|Cantidad de unidades vendidas.
|precio_unitario_ars_nominal	|float	|Precio unitario en USD corrientes (ajustado por inflación y variaciones).
|monto_venta_ars_nominal	|float	|Monto total de la transacción en USD corrientes.
|monto_venta_ars_real_2018	|float	|Monto deflactado a precios constantes de 2018 (usando IPC).
|es_evento	|int (0/1)	|Flag que indica si la transacción ocurrió en un evento promocional (Hot Sale, Cyber/Black).

## *Dimensión Productos: dim_productos.csv*

|Columna	|Tipo	|Descripción |
| --- | --- | --- |
|producto_id	|int	|Identificador único del producto.
|nombre_producto	|string	|Nombre comercial del producto.
|categoria	|string	|Categoría principal (Tecnología, Línea Blanca, Pequeños Electro).
|subcategoria	|string	|Subcategoría (ej. Computo, Moviles, Refrigeración, Cocina, etc.).
|precio_base_ars_2018	|float	|Precio base en USD a valores de 2018 (para deflactar).

## *Dimensión Clientes: dim_clientes.csv*
  
|Columna	|Tipo	|Descripción |
| --- | --- | --- |
|cliente_id	|int	|Identificador único del cliente.
|nombre_cliente	|string	|Nombre ficticio generado con Faker.
|email_cliente	|string	|Email ficticio.
|ciudad_cliente	|string	|Ciudad ficticia.
|segmento_base	|string	|Segmento inicial asignado aleatoriamente (Premium, Frecuente, Ocasional, Nuevo).

## *Dimensión Sucursales: dim_sucursales.csv*
  
|Columna	|Tipo	|Descripción |
| --- | --- | --- |
|sucursal_id	|int	|Identificador único de la sucursal.
|nombre_sucursal	|string	|Nombre ficticio de la sucursal.
|direccion_sucursal	|string	|Dirección ficticia. Incluye errores intencionales para ETL.
|provincia_sucursal	|string	|Provincia de la sucursal. Incluye errores intencionales (mal escritos, espacios, NaN).

## *Dimensión Canales: dim_canales.csv*

|Columna	|Tipo	|Descripción |
| --- | --- | --- |
|canal_id	|int	|Identificador único del canal.
|nombre_canal	|string	|Nombre del canal (Online, Sucursal Física).

## *Dimensión Fecha: dim_fecha.csv*

|Columna	|Tipo	|Descripción |
| --- | --- | --- |
|fecha	|date	|Fecha calendario.
|año	|int	|Año.
|mes	|int	|Mes numérico.
|dia	|int	|Día del mes.
|nombre_mes	|string	|Nombre del mes.
|nombre_dia_semana	|string	|Nombre del día de la semana.
|trimestre	|int	|Trimestre (1–4).
|semana_del_año	|int	|Semana ISO del año.
|es_evento	|int (0/1)	|Flag de evento promocional.


