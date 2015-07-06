Context
=======

El objeto contexto es algo similar a un Service Container. Es un objeto que almacena otros objetos comunes,
como cookies, el lenguaje actual, el usuario que ha iniciado sesión, servicios (smarty), etc.


Obteniendo el objeto context
############################

En controladores y módulos podemos acceder a él de esta forma:

.. code-block:: php

  $this->context;


Si no estamos ni en un controlador ni módulo podemos obtener el context con:

.. code-block:: php

  $context = Context::getContext();


Objetos disponibles
###################

:cart: El objeto carrito del cliente en el front office. No disponible en back office
:customer: El cliente logueado actual. Sólo front office
:cookie: Es distinta en front office y en back office. Ej. el id de empleado sólo estará disponible en el back office
:link: Contiene métodos para crear enlaces para imágenes, productos, etc
:country: EL país definido por el carrito del cliente (en cuanto defina una dirección) o el por defecto de la tienda
:employee: Contiene el objeto Employee correspondiente al usuario iniciado en el Back Office
:controller: El controlador actual (FrontController o AdminController en back)
:language: El idioma actual según el seleccionado por el cliente
:currency: La moneda del carrito actual
:shop: El objeto Shop en la cual se encuentra el cliente
:smarty: Nos permitirá asignar variables a smarty para mostrar después en la plantilla
:mobile_detect: Nos dice si el visitante está en móvil o no. No es válido para la back office
