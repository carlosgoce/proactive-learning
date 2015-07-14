AJAX
====

.. role:: php(code)
   :language: php

.. role:: shell(code)
   :language: shell

Para realizar las llamadas ajax debemos proceder de la siguiente forma.

Crear dentro de nuestro módulo un fichero php que recibirá la llamada ajax,
por ejemplo, :shell:`mi_modulo/ajax/millamada.php`

El fichero simplemente debe escribir la respuesta que deseemos:


.. code-block:: php

   echo "hello world";


Finalmente desde JS lo único que debemos hacer es llamar a la URL de esta forma:


.. code-block:: js

    var query = $.ajax({
      type: 'post',
      url: 'mi_modulo/ajax/millamada.php',
      data: {id: val},
      dataType: 'json',
      success: function(json) {
        alert(json);
      }
    });


O la configuración ajax que deseemos.


Para utilizar código de Prestashop, modelos, etc, debemos cargar el núcleo de prestashop de esta forma:


.. code-block:: php

    require_once(dirname(__FILE__).'../../../../config/config.inc.php');
    require_once(dirname(__FILE__).'../../../../init.php');


Hecho esto podemos acceder helpers y otras herramientas de Prestashop, por ejemplo,
podríamos imprimir un array como json así: :php:`echo Tools::jsonEncode($result);`

Si queremos utilizar modelos de Prestashop simplemente debemos requerirlos.
