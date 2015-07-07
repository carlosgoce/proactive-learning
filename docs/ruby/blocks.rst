Blocks
======

Los *code blocks* son *trozos* de código que asociamos
a invocaciones de métodos, como si fuera un parámetro más.

Es una característica muy poderosa y muy importante de entender,
pues es un recurso muy utilizado en Ruby.

Se pueden utilizar *code blocks* para implementar *callbacks*,
para pasar trozos de código de un lado a otro, y para
implementar iteradores.

Un *code block* es un bloque de código entre llaves o entre
los keyword *do* y *end*.

.. code-block:: ruby

    # Esto es un code block
    { puts "Hola" }

    # Y esto también
    do
      club.asociar(persona)
      persona.socializar
    end
