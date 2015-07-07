Estructura
##########

Inicialización de las páginas
-----------------------------

Un controlador hereda de FrontController para páginas del Frontend
o bien de ModuleFrontController para páginas del backend.

El punto de entrada está en el fichero index.php en la raíz del proyecto.
Este fichero busca el controlador requerido lo instancia y le pasa
los parámetros que correspondan con una llamada al método dispatch
de la clase Dispatch.

.. code-block:: php

    # Instanciar controlador

    try {
        # Instanciar controlador
        $controller = Controller:getController($controller_class);

        # Lanzar hook del dispatcher
        if ( isset($params_hook_action_dispatcher) ) {
            Hook::exec('actionDispatcher', $params_hook_action_dispatcher);
        }

        # Ejecutar el controlador
        $controller->run();
    }
    catch(PrestashopException $e) {
        $e->displayMessage();
    }


Además en esta inicialización se cargan también los siguientes ficheros
que incializan configuraciones del servidor.

:defines.inc.php: Define constantes
:settings.inc.php: Información sobre la base de datos, fecha de instalación y claves
:autoload.php:
    :alias: especifica ciertos alias para funciones como la clase Tools y contiene
            la función pSQL que se utiliza para sanear datos para prevenir injecciones SQL
    :classes/Autoload.php: Implementa una función para cargar el controlador de la petición
:defines_uri_inc.php: Constantes para obtener URLS de varias carpetas (modulos, carpetas de js, css, etc)
:smarty.config.inc.php: Define variables de Smarty:


    - Smarty.class.php
    - smartyadmin.config.inc.php
    - smartyfront.config.inc.php


Context
-------

El objeto singleton *Context* también es inicializado en casi todas las clases y controladores
y contiene información importante sobre el usuario actual y almacena multitud de objetos:

    - Carrito del cliente
    - Customer
    - Cookie
    - Link
    - Country
    - Employee
    - Controller
    - Language
    - Currency
    - AdminTab
    - Shop
    - Smarty
    - mobile_detect


Autoload
--------

.. code-block:: php

    require_once(dirname(__FILE__).'/alias.php');
    require_once(dirname(__FILE__).'/../classes/Autoload.php');
    spl_autoload_register(array(Autoload::getInstance(), 'load'));


Las clases se cargan de los directorios en este orden:

    - classes/
    - override/classes/
    - controllers/
    - override/controllers/


Todos los ficheros de esas carpetas se autocargarán. Para mejorar el rendimiento se puede crear un fichero
de caché cache/class_index.php con un array asociativo clave => valor siendo clave el nombre de la clase
y valor la ruta al fichero.

.. code-block:: php

    array(
        'DbCore' => 'classes/db/Db.php',
    );


Para entender mejor como funciona ver la clase Autoload y su método Autoload::load().


Rutas
-----

La clase Dispatcher contiene un array con las rutas por defecto y reglas.
Para entender mejor como funciona ver la clase Dispatcher y los métodos loadRoutes y addRoute.

Desde la versión 1.5.3 es posible añadir URLs personalizadas. Por ejemplo, dado el módulo mimodulo
que contiene dos funciones principales:

    - Mostrar una página con una lista de comandos disponibles
    - Ver detalles de un pedido


Página de lista de comandos:
    - Sin URLs amigables: http://www.tutienda.com/index.php?fc=module&module=mimodulo&controller=orders&module_action=listing
    - Con URLs amigables: http://www.tutienda.com/module/mimodulo/orders?module_action=listing


Detalle de un pedido:
    - Sin URLs amigables: http://www.tutienda.com/index.php?fc=module&module=mimodulo&controller=orders&module_action=detail&id_order=42
    - Con URLs amigables: http://www.tutienda.com/module/mimodulo/orders?module_action=details&id_order=42


La idea de este tipo de URLs es que sean limpias y claras y SEO Friendly, pero aún así, las URLs se ven un poco raras.
Desde la mencionada versión 1.5.3 podemos reescribir las URL para que queden así:
    - http://www.tutienda.com/module/mimodulo/orders/listing
    - http://www.tutienda.com/module/mimodulo/orders/details/42


Nada que ver. Para personalizarlas debes ir a Preferencias -> SEO -> URLs -> Schema para ver las personalizaciones
que puedes realizar. Debes tener también las Friendly Url's activadas.
