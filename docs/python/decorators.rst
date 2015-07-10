Decorators
==========

.. todo::  Falta añadir explicación y decorators básicos


El wraps es para estandarizar el decorator

Ejemplo:

.. code-block:: python

    def searchable_view(*attrs):
        def decorator(func):
            @wraps(func)
            def wrapper(*arg, **kwargs):
                rv = func(*arg, **kwargs)
                return rv

            return wrapper

        return decorator
