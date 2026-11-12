select
    id_venta,
    fecha_venta,
    cantidad,
    precio_unitario,
    _loaded_at
from {{ source('ventas_raw', 'ventas') }}
