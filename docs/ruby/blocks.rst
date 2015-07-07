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


Hay dos tipos de delimitaciones porque a veces es más
natural utilizar uno u otro. Algo recurrente en ruby,
proveer diferentes formas para hacer lo mismo.

No obstante, la comunidad utiliza la siguiente convención:
utilizar las llaves para bloques de una sóla línea,
y do / end para bloques multilínea.

Ejemplo:

.. code-block:: ruby

    # Usamos llaves porque es un bloque de una sóla línea
    saludar { puts 'Hola' }

    # Si el método necesita parámetros se ponen antes del bloque
    saludar("Carlos", "cliente") { puts 'hola' }

Un método puede invocar el bloque una o más veces utilizando
el statement yield. Piensa que es algo como una llamada a un método que
invoca el bloque asociado con la llamada del método que contiene yield.

Ejemplo:

.. code-block:: ruby

    def llamar_al_bloque
      puts 'Comienza el método'
      yield
      yield
      puts 'Fin'
    end

    llamar_al_bloque { puts 'En el bloque' }

    # Imprime
    # Comienza el método
    # En el bloque
    # En el bloque
    # Fin


El código del bloque se ejecuta 2 veces, una por cada yield.
Si necesitas pasar argumentos al bloque la sintaxis es la siguiente:

.. code-block:: ruby

    def quien_dice_que
      yield('Carlos', 'hola')
      yield('Miguel', 'adios')
    end

    # Los argumentos van entre | al inicio del bloque
    quien_dice_que {|persona, frase| puts "#{persona} dice #{frase}"}

    # Imprime
    # Carlos dice hola
    # Miguel dice adios


Los *code blocks* se utilizan también para implementar iteradores,
que son métodos que devuelven sucesivamente elementos dealgún tipo
de colección, como un array:

.. code-block:: ruby

    # Definimos un array
    animales = ["gato", "perro"]

    # Ejecuta el bloque una vez por item en el array
    animales.each {|animal| puts animal}

    # Imprime
    # gato
    # perro

    # Más ejemplos

    5.times { print "yo "}
    # Imprime yo yo yo yo yo

    3.upto(6) {|i| print i}
    # Imprime 3456
