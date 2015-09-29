Eventos
=======

Desde fuera de $rootScope

.. code-block:: javascript

  // Enviar evento hacia abajo
  $scope.$broadcast('miEvento', 'Algún dato u objeto');

  //Enviar evento hacia arriba
  $scope.$emit('miEvento', 'Algún dato u objeto');


En caso de querer enviar un evento a un $scope "hermano",
que nace de $rootScope, debemos enviar el evento a través
de $rootScope.

Desde $rootScope tenemos algunas diferencias.


.. code-block:: javascript

  // Enviar evento hacia abajo lo envía hacia todos los hijos de rootScope
  // Otros listener de $rootScope también recibirán el evento
  $scope.$broadcast('miEvento', 'Algún dato u objeto');

  //Enviar evento hacia arriba hará que sólo los listener de $rootScope reciban el evento
  $scope.$emit('miEvento', 'Algún dato u objeto');
