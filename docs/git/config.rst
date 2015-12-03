Config
=======

Para no tener que hacer contínuamente --set-upstream mi_rama origin/mi_rama
y que lo haga por defecto.

Es decir, que siempre empuje por defecto al remoto a una rama con mismo nombre.

.. code-block:: shell

    git config --global push.default current
