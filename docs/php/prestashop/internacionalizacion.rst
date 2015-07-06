Internacionalización
====================


Internacionalizando cadenas con el método "l".
Preferiblemente poner todos en inglés por defecto.


.. code-block:: php

    $this->l('texto a traducir');


En la plantilla smarty se utiliza de este modo:


.. code-block:: smarty

  {l s='Cadena a traducir'}


Hecho esto prestashop creará un directorio translations.php en la raíz del módulo con las cadenas a traducir.
