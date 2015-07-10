Hooks
=====

Los hooks (ganchos) son fundamentales para crear módulos en Prestashop.

Son puntos donde podremos enganchar nuestro módulo con el comportamiento
habitual de una tienda Prestashop.

Los hay de dos tipos.

:Tipo display:
    Generalmente utilizados para añadir HTML y JS a páginas específicas
    Por ejemplo añadir un nuevo bloque a una columna, añadir enlaces,
    un nuevo campo en un formulario, etc...

:Tipo action:
    Se utilizan para cambiar el comportamiento añadiendo nuevas acciones
    cuando ciertos eventos ocurren.


Engancharnos a un hook
######################

Se debe crear un nuevo método install donde indicaremos todos los hooks
en los que nos engancharemos. Importante llamar al constructor padre.
Ejemplo para engancharnos al hook displayProductTabContent, el cual
nos permite añadir contenido a una página de producto:


.. code-block:: php

    public function install()
    {
        parent::install();
        $this->registerHook('displayProductTabContent');
        # Si se devuelve false Prestashop indicará que el módulo
        # no se ha instalado correctamente
        return true;
    }


Los hook necesitan el id del módulo, por eso debemos "instalarlo". Y por eso debemos ponerlo después de
la llamada al método padre install.

Además, debes añadir el método hook{nombreDelHook} que se ejecutará
cada vez que se lance el evento displayProductTabContent. Como es tipo
display, lo habitual es que el hook devuelva un html.
En este caso de ejemplo lo devolvemos a mano, pero recordar utilizar
mejor una plantilla smarty:


.. code-block:: php

    public function hookDisplayProductTabContent($params)
    {
        return '<b>Esto se verá en la página de productos</b>';
    }


Posición de los Hook
####################

Los módulos enganchados a un hook tienen asociada una posición.
Esta posición representa el orden en que será llamado el hook.
En caso de ser un hook tipo display será el orden en que se mostrarán.

Al añadir un módulo a un hook se le asignará la última posición.
Para cambiar el orden se puede hacer desde el back office en el
menú principal -> modulos -> posiciones.

Desde esa pantalla también podremos desenganchar un hook o engancharlo
nuevamente.


Crear nuestros propios hook
###########################

Sólo necesitas colocar el trigger en el archivo php o plantilla smarty con una llamada a registerHook.
Automáticamente añadirá el hook a la base de datos sino existe ya.

.. code-block:: php

    Hook::exec('displayLeftColumn');
