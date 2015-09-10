Snippets
========

Ejecutar función en intervalos mientras se escribe
##################################################

.. code-block:: javascript

    var typingTimer;
    var doneTypingInterval = 5000;
    var $input = $('#myInput');

    // En keyup, comenzar la cuenta atrás
    $input.on('keyup', function () {
      clearTimeout(typingTimer);
      typingTimer = setTimeout(doneTyping, doneTypingInterval);
    });

    // En keydown, reiniciar la cuenta atrás
    $input.on('keydown', function () {
      clearTimeout(typingTimer);
    });

    // Ha terminado la cuenta atrás. Lanzar función
    function doneTyping () {
      //do something
    }
