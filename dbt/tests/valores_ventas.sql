select id_venta from {{ ref('stg_ventas') }}
where cantidad <= 0 or precio_unitario < 0
