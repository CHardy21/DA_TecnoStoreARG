# Script para generación de datos con inflación, eventos y canales
A continuación el script completo y autocontenido que:

- Genera dimensiones más realistas (productos con categorías y subcategorías, clientes, sucursales, canales y fecha).

- Modela volúmenes y cuotas de canal acordes a 2018–2024 (pre, pandemia, post).

- Aplica inflación anual y construye un índice IPC sintético para calcular ventas nominales y reales.

- Introduce eventos promocionales (Hot Sale en mayo y Cyber/Black en noviembre), con picos de volumen y mayor cuota online.

- Mantiene un modelo estrella (sin copo de nieve), listo para ETL con errores controlados en sucursales.

## Supuestos y parámetros clave
- **Volumen diario target:**

  - Pre-pandemia 2018–2019: ~200 transacciones/día.

  - Pandemia 2020–2021: ~400 transacciones/día, con fuerte migración al canal online.

  - Post 2022–2024: ~320–360 transacciones/día (híbrido consolidado).

- **Cuota online:**

    - Pre: 15%.

    - Pandemia: evoluciona hasta 65–70%.

    - Post: estabiliza en 55–60%.

- **Inflación** (IPC sintético, base 2018=100): crecimiento anual acumulado, para ajustar precio nominal y calcular precio real.

- **Eventos:**

    - Hot Sale: 3 días en mayo.

    - Cyber/Black: 3 días entre fines de octubre y noviembre.

    - Efectos: +80–120% en transacciones y +10–20 p.p. de cuota online durante esos días.