select
    fecha_venta,
    count(*) as numero_ventas,
    sum(cantidad) as unidades_vendidas,
    sum(cantidad * precio_unitario) as ingreso_total
from {{ ref('stg_ventas') }}
group by fecha_venta