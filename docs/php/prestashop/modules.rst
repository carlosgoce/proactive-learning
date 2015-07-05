Módulos
=======

Creando el módulo
#################

El nombre técnico debe ser en minúsculas, conteniendo sólo letras y números,
y debe comenzar con una letra.

Una vez seleccionado el nombre del módulo se crea una carpeta con ese nombre
dentro de la carpeta **modules** y dentro de esta un fichero php
con el nombre del módulo.

Podemos añadir un logo al módulo
poniendo una imagen .gif de 16x16 y un png de 32x32 px
en la raíz del módulo .

Por tanto, suponiendo que el módulo se llame
mymodcomments, nos crearemos una estructura como esta:


.. code-block:: shell

   modules
     - mymodcomments
       - mymodcomments.php
       - logo.gif
       - logo.png


El contenido del fichero debe ser:


.. code-block:: php

    <?php
    class MyModComments extends Module
    {
        public function __construct()
        {
            // Estos 3 primeros parámetros son obligatorios

            # Este lo utiliza prestashop como nombre del módulo
            # Al instalar, configurar enlaces, etc.
            $this->name = 'mymodcomments';

            # El nombre que saldrá en la tienda
            $this->displayName = 'Mi modulo de comentarios';

            # Finalmente debemos llamar al método padre obligatoriamente
            # para que se inicialice correctamente
            parent::construct();

            # Tambien podemos definir mas configuraciones
            # pero son totalmente opcionales

            # El nombre de la categoria (ver lista en prestashop)
            # Sirve para que encuentren el modulo facilmente en la tienda
            $this->tab = 'front_office_features';

            # Útil para indicar al módulo que está desactualizado
            $this->version = '0.0.1';
            $this->author = 'Carlos Goce';
            $this->description = 'Descripción del módulo';
        }
    }


Una vez en su sitio ya nos saldrá en prestashop para instalar, desinstalar,
actualizar, eliminar, etc...
