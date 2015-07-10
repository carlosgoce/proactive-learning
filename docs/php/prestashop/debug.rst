Depuración
==========

Modo desarrollo
###############

- Activa display_errors de PHP para que se vean los errores en lugar de una página en blanco
- Activa la constante _PS_DEBUG_SQL para que muestre potenciales problemas con las consultas
- Activa _PS_DISPLAY_COMPATIBILITY_WARNING que nos avisará si utlizamos código *deprecated* (obsoleto)

Para activarlo poner a true la variable **_PS_MODE_DEV** en el fichero */config/defines.inc.php*


Funciones
#########

:p(): Devuelve el contenido de una variable utilizando print_r()
:d(): Finaliza la ejecución con die()

Ambos tienen alias, ppp y ddd, para permitir encontrarlos más fácilmente en el código al realizar una búsqueda
en el editor.


Perfilador
##########

Para activarlo configura la constante :code:`_PS_DEBUG_PROFILING_true` en el fichero :code:`config/defines.inc.php`

Nos permitirá obtener esta información en las páginas:

- Tiempo de carga
- Hooks procesados
- Uso de memoria
- Número de consultas a la base de datos y duración de las mismas
- "Estrés" de las tablas de la base de datos
- Instancias de ObjectModel utilizados
- Ficheros incluídos
