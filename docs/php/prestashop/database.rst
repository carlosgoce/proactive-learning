Base de datos
=============

Es preferible utilizar los modelos de Prestashop para realizar
consultas, pero en ocasiones necesitamos realizar consultas manualmente.

Se puede obtener una instancia de la base de datos con DB::getInstance().

Los métodos que nos permite son los siguientes:


:insert($tabla, $datos):
  Nos permite realizar un insert indicando el nombre de la tabla y
  un array asociativo. Devuelve un booleano.


:update($tabla, $datos, $condicion):
  Igual que insert pero actualiza un registro existente.


:Insert_ID():
  Devuelve el ID del último registro insertado en la base de datos


:executeS($peticionSQL):
  Nos permite realizar una consulta SELECT. Devuelve un array con los
  resultados.

:getRow($peticionSQL):
  Realizar una consulta SELECT pero devuelve una única línea de resultados.
  Añade LIMIT 1 a la consulta automáticamente.

:getValue($peticionSQL):
  Devuelve un valor único con una petición SQL. Por ejemplo, un COUNT.

:execute($peticionSQL):
  Puedes realizar cualquier consulta pero devuelve un booleano por tanto
  no es válido para realizar SELECTS.

:query($peticionSQL):
  Este método lo utilizan los demás para realizar las consultas.
  Similar al método execute pero no realiza caché. Y devuelve el resultado
  SQL directamente. Así que mejor utilizar los demás métodos.


Para escapar cadenas de injección SQL podemos utilizar la función pSQL($string).
