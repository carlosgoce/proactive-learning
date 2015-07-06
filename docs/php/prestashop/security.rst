Security
========

Consultas SQL
#############

- Para proteger los string de las consultas los pasamos por la función pSQL($string)
- Los enteros los parseamos con int($numero)


Smarty
######

Escapar las cadenas de los usuarios


.. code-block:: smarty

    {if $smarty.get.selection}
        {$smarty.get.selection|escape:'htmlall'}
    {/if}
