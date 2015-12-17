PostgreSQL
==========

.. role:: sql(code)
   :language: sql


CLI
---

:sql:`\l`
   Listar bases de datos

:sql:`SET TIME ZONE 'UTC';`
   Cambia la zona horaria para la **sesión** actual

:sql:`\q`
   Cierra la sesión de psql



VARS
----

La timezone se puede cambiar sobreescribiendo PGTZ


.. code-block:: bash

   PGTZ=UTC psql -c "SHOW TIME ZONE;"
    TimeZone
   ----------
    UTC
   (1 row)

