Object Models
=============

.. role:: php(code)
   :language: php


Definición de un nuevo Object Model
###################################


Un object model de prestashop viene a ser algo así como un pequeño ORM. Lo ideal es guardarlos en una carpeta
de nuestro módulo llamada classess o models.

La convención de Prestashop para llamar al fichero y clase son las siguientes:
    - El mismo nombre para el archivo y la clase
    - Utilizar CamelCase para el nombre
    - Definir el nombre en singular
    - El nombre debe coincidir con el nombre de la tabla en la base de datos

La clase debe extender de ObjectModel y debes crear una variable pública por cada campo en la base de datos.
Además hay que crear un array de definiciones realizando los siguientes pasos:

    1. Definir el nombre de la tabla relacionada con el objeto, sin el prefijo (se añadirá automáticamente)
    2. Definir la clave primaria de la tabla
    3. Definir el campo multilang en caso de que el objeto necesite traducirse a varios idiomas
    4. Definir el array *fields* que contiene el *type*, el método de validación que se llamará
       al actualizar o insertar un objeto, el tamaño del campo (*size*) y la bandera *required*.
       Además también tenemos el campo *copy_post* que indicar si se debe obtener el valor de valores POST o no
       (normalmente se desactiva para campos tipo fecha como updated_at).

Ejemplo:

.. code-block:: php

    class MiModuloComentario extends ObjectModel
    {
        public $id_comentario;
        public $id_producto;
        public $nombre;
        public $apellidos;
        public $comentario;

        /**
        * @see ObjectModel::$definition
        */
        public static $definition = array(
            'table'     => 'mimodulo_comentario',
            'primary'   => 'id_comentario',
            'multilang' => false,
            'fields'    => array(
                'id_producto' => array('type' => self::TYPE_INT, 'validate' => 'isUnsignedId', 'required' => true),
                'nombre'      => array('type' => self::TYPE_STRING, 'validate' => 'isName', 'size' => 20),

                // Y así con el resto de campos
            ),
        );
    }


Guardando en la base de datos con un ObjectModel
################################################

$comentario = new MiModuloComentario();
$comentario->nombre = 'Carlos';
$comentario->producto = 25;
$comentario->comentario = 'texto del comentario'
$comentario->add();


.. warning:: Valores null serán convertidos a ":php:`0`" a no ser que se indique
    lo contrario. Para ello el atributo en el modelo debe declararse como tipo
    :php:`self::TYPE_NOTHING` y probablemente sea necesario sobreescribir el método
    add del modelo por:

    .. code-block:: php

        public function add($autodate = true, $null_values = true)
        {
            return parent::add($autodate, $null_values);
        }

    es decir, forzando $null_values=true para permitir valores null.


Validación
----------

La lista completa de validaciones se puede consultar en el propio
código fuente:
https://github.com/pal/prestashop/blob/master/classes/Validate.php

Cuidado. El comentario será validado antes de guardarse en cuyo caso lanzará excepciones que deberás capturar
para mostrar el error correspondiente al usuario.

Podríamos guardar así el error:

.. code-block:: php

    $this->context->smarty->assign('nuevo_comentario_posted', 'error');


Para mostrar la alerta al usuario el código prestashop en la plantilla sería:

.. code-block:: smarty

    {if isset($nuevo_comentario) && $nuevo_comentario_posted eq 'error'}
        <div class="alert alert-danger">
            <p>
                {l s='Algunos campos del formulario no son correctos, corrígelos y vuelve a intentarlo'}
            </p>
        </div>
    {/if}


**No olvides incluír el fichero .php del ObjectModel en todos los lugares donde quieras utilizarlo.**
