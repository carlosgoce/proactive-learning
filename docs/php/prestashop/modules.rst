Módulos
=======

Métodos y variables disponibles
###############################

:$this->_path: Contiene el path del módulo actual
:$this->context: :doc:`context`


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

            # Para definir la compatibilidad de nuestro módulo con versiones de prestashop
            $this->ps_versions_compliancy = array('min' => '1.5.0', 'max' => '1.6.0.1');

            # Forzar instalar módulos del que depende éste
            $this->dependencies = array('paypal', 'blockcart');
        }
    }


Una vez en su sitio ya nos saldrá en prestashop para instalar, desinstalar,
actualizar, eliminar, etc...


Añadiendo configuración
#######################

Para permitir configurar el módulo utilizaremos el método getContent.


.. code-block:: php

    public function getContent()
    {
        return 'Texto a mostrar';
    }


Ahora si accedemos al módulo y pinchamos en el botón configurar,
la vista que obtendremos contendrá ese texto. Por supuesto
escribir la vista directamente en php no es muy buena idea.
Crearemos una plantilla de smarty para devolver la vista de configuración
del módulo.

Crea el fichero /views/templates/hook/getContent.tpl
a partir de la raíz de tu módulo. Una práctica de Prestashop es poner
al nombre de la vista el nombre del método, en este caso getContent.

En la vista poner "Texto a mostrar desde plantilla" y en la función getContent cambiarla
por esta otra función para que devuelva la plantilla que acabamos de crear.


.. code-block:: php

    public function getContent()
    {
                                                                                                            return $this->display(__FILE__, 'getContent.tpl');
    }


Ahora en la pantalla de configuración del módulo veremos el texto que hemos
añadido a la plantilla.


Manteniendo los módulos actualizados automáticamente
####################################################

Crear tablas al instalar el módulo
----------------------------------

Primero, crea un directorio llamado install dentro del módulo. Aquí crearemos el fichero install.sql
donde pondremos la consulta a lanzar al instalar el módulo.

.. code-block:: sql

    CREATE TABLE IF NOT EXIST `PREFIX_mimodulo_comentario` (
        `id_mimodulo_comentario` int(11) NOT NULL AUTO_INCREMENT,
        `comentario` text NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

Es importante poner la palabra PREFIX o algo similar para poder después substituírlo por el de Prestashop.
Añadimos ahora este método para cargar el SQL del fichero y ejecutarlo:

.. code-block:: php

    public function loadSQLFile($sql_file)
    {
        $sql_content = file_get_contents($sql_file);
        $sql_content = str_replace('PREFIX_', _DB_PREFIX_, $sql_content);

        # Dividimos las sentencias sql en un array por si hubiese varias
        $sql_requests = preg_split("/;\s*[\r\n]+/]", $sql_content);

        $result = true;

        foreach ($sql_requests as $request) {
            if ( ! empty($request)) {
                $result &= Db::getInstance()->execute(trim($request));
            }
        }

        return $result;
    }


Sólo nos queda llamar a este método en el método install justo después de llamar al padre:

.. code-block:: php

    public function install()
    {
        # más código
        parent::install();
        $sql_file = dirname(__FILE__).'/install/install.sql';
        $this->loadSQLFile($sql_file);
    }


Configuración inicial
---------------------

Si lo deseamos podemos crear la configuración inicial que de seemos también en el método install, de esta forma:

.. code-block:: php

    Configuration::updateValue('MIMODULO_NIVEL_DE_DETALLE', 3);


Eliminando tablas tras la desinstalación
----------------------------------------

Podemos realizarlo de la misma forma que la instalación pero creando los SQL inversos, es decir, eliminando
los cambios que hemos realizado en la base de datos, eliminando las configuraciones, etc.

.. code-block:: php
    if ( ! parent::uninstall() ) {
        return false;
    }

    # Lanzar consultas de desinstalación
    $sql_file = dirname(__FILE__).'/install/uninstall.sql';

    if ( ! $this->loadSQLFile($sql_file)) {
        return false;
    }

    # Eliminar configuración
    Configuration::deleteByName('MIMODULO_NIVEL_DE_DETALLE');

    return true;


Los hooks se desinstalan automáticamente al desinstalar el módulo así que no necesitamos hacer nada al respecto.


Actualizando el módulo
----------------------

Si piensas distribir el módulo será mejor manejar las actualizaciones de forma correcta.
El funcionamiento es muy sencillo, de forma casi idéntica a los métodos install y uninstall tenemos el método
update que será llamado cuando se actualice el módulo.

Creamos un archivo install-{version-del-modulo}.sql en la misma carpeta que los otros. En este caso el método a
llamar será update_module_0_0_2 o el número de versión correspondiente, el cual debe ser definido en el
contructor como podemos ver en `Creando el módulo`_.

Prestashop guarda en la base de datos la versión instalada del módulo. Al acceder al back office comprueba
que la versión en la base de datos se corresponda con la del módulo, en caso de no coincidir, lanzará la
actualización o actualizaciones si hubiese más de una.

A veces verás el botón "actualízalo", que indica que hay una nueva versión del módulo en addons.prestashop.com.
Al pincharlo se descargará el módulo y después lanzará los script de actualización si hubiese alguno.
