Consultas
=========


Encontrar duplicados y sacar listado de ambos, sin repetidos
############################################################


.. code-block:: sql


    SELECT DISTINCT a.id, a.campo_duplicado, a.nombre
    FROM tabla_con_duplicados AS a JOIN tabla_con_duplicados AS b USING(campo_duplicado)
    WHERE a.id <> b.id AND a.campo_duplicado > 0 AND a.campo_duplicado=b.campo_duplicado
