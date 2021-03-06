Admin Controller
================

Nos permite administrar una clase ObjectModel para realizar un CRUD sobre este y también crear
nuestras propias acciones o vistas personalizadas.


Instalación
###########

La convención es crear el controlador principal en la ruta controllers/admin del módulo
incluyendo el nombre del mismo.


.. code-block:: php

    class AdminMyModCommentsController extends ModuleAdminController
    {

    }


Es decir, el nombre debe ser Admin[NombreControlador]Controller y el fichero debe llamarse igual.


.. code-block:: txt

    Atención
    Para poder acceder al controlador se necesita crear la pestaña en la administración
    Se puede desactivar su visualización desde la administración misma, pero debe estar definido
    para poder acceder


Ahora debemos crear una nueva pestaña en el backoffice, desde Administración -> Pestaña. O realizarlo programáticamente
creando un nuevo método *installTab* en la clase principal de nuestro módulo.

Prestashop contiene una lista de objetos tipo ObjectModel para sus propias tablas, para crear el nuevo Tab utilizaremos
el objeto ObjectModel Tab. El método nos quedaría así:


.. code-block:: php

    public function installTab($parent, $class_name, $name)
    {
        $tab = new Tab();

        # Método que nos permite obtener el id a partir del nombre de la clase
        $tab->id_parent = (int)Tab::getIdFromClassName($parent)
        $tab->name = array();

        # Lista de idiomas disponibles y activados
        foreach (Language::getLanguages(true) as $lang) {
            $tab->name[$lang['id_lang']] = $name;
        }

        $tab->class_name = $class_name;
        $tab->module = $this->name;
        $tab->active = 1;
        return $tab->add();
    }


Ahora llamaremos a este método desde el método install


.. code-block:: php

    public function install()
    {
        # otro código

        if ( ! $this->installTab('AdminCatalog', 'AdminMyModule', 'MyModule') ) {
            return false;
        }
    }


Si todo a ido bien ya podremos ver el nuevo *Tab* en el back office, tras reinstalar el módulo.
Nota: Los métodos tab requieren el nombre del controlador admin sin el sufijo Controller. Por eso los parámetros
de install tab no los llevan.

Ahora si accedes a este nuevo tab verás una página vacía con el header y footer.

La ruta del controlador será así:
http://[host]/adminweb/index.php?controller=Admin[NombreControlador]&token=[eltoken]
Sin incluir Controller en el nombre


Desinstalación
##############

Al desinstalar el módulo deberíamos eliminar las tablas y configuraciones. Además de la Tab que hemos creado.
Para desinstalar el tab crearemos un nuevo método.


.. code-block:: php

    public function uninstallTab($class_name)
    {
        # Obtener el id del tab
        $id_tab = Tab::getIdFromClassName($class_name)

        # Obtener la instancia
        $tab = new Tab($id_tab);

        # Eliminarla
        return $tab->delete();
    }


Tras esto en el método uninstall del módulo lo llamaremos de esta manera:

.. code-block:: php

    if ( ! $this->uninstallTab('AdminNombreModulo'))
    {
        return false;
    }


Listando recursos
#################

El controlador Admin extiende de ModuleAdminController, que a su vez extiende de AdminController.
Esto nos da varias funcionalidades automáticamente gracias a la herencia. Como mostrar unl istado de ObjectModel.

Para utilizar la acción de listado de ObjectModel debes definir en el constructor de tu AdminController las
siguientes variables:

:table: El nombre de la tabla asociada al ObjectModel
:className: El nombre de la clase del ObjectModel
:fields_list: Un array asociativo con la lista de campos que queremos mostrar en la lista.
              La clave debe corresponder al campo en la base de datos.
              El valor puede tener varios parámetros como title, width, align, etc.
              Uno de ellos es obligatorio, title, que será el label del input asociado.
:bootstrap: Activa el uso de plantillas bootstrap

Recuerda crear el :doc:`objectmodels` que utilizará el controlador si es necesario.

Ejemplo:

.. code-block:: php

    class AdminMyModuleController extends ModuleAdminController
    {
        public function __construct()
        {
            $this->table = 'mymoduletable';
            $this->className = 'MyObjectModelClass';
            $this>-fields_list = array(
                'name' => array('title' => $this->l('name'), 'align' => 'center'),
                'date' => array('title' => $this->l('date'), 'align' => 'left'),
            );

            # Usar la plantilla de bootstrap
            $this->bootstrap = true;

            # No olvidar llamar al constructor que generará cookies y otras cosas esenciales
            parent::__construct();

            # Opcional
            $this->meta_title = $this->l('Título para este tab');
            $this->toolbar_title[] = $this->meta_title;
        }
    }


Modificando la consulta
-----------------------

Probablemente tengas que desinstalar e instalar el módulo. Esto nos activará paginación y filtros por defecto.
Y también activará las búsquedas en el listado.

Si necesitas cambiar la consulta que se realiza para obtener el listado puedes sobreescribir las propiedades
_select, _join o _where.

Por defecto la consulta que se realiza es así:


.. code-block:: php

    "                                                                                                SELECT a.* FROM `'._DB_PREFIX_.$this->table.'` a"


Es decir, se utiliza el alias *"a"* para el nombre de la tabla. Si quisiéramos modificar la parte SELECT por ejemplo
podríamos hacer esto:

.. code-block:: php

    $this->select = "CONCAT(a.firstname, a.lastname) fullname, a.date"


Estos cambios deben añadirse después de llamar al constructor padre o las sobreescribirá.
Todas estas variables serán concatenadas al final realizando la consulta completa.


Filtros
-------
En la lista de campos, debemos especificar los filtros de esta forma.

.. code-block:: php

    'fullname' => array('title' => $this->l('Nombre completo'), 'filter_key' => 'a!grade')


Como estamos utilizando un alias en la tabla, debemos especificar el alias y el nombre del campo.
Es decir, en este caso *"a"* es el alias de la tabla y *"fullname"* el nombre del campo
Sin especificarlo, si intentas filtrar por estos campos Prestashop lanzará un error.



Acciones
--------

Sino especificamos ninguna, por defecto no se mostrará ninguna acción en la lista de recursos.
Para añadir acciones como ver, editar y eliminar llamaremos al método addRowAction en el constructor.

.. code-block:: php

    $this->addRowAction('view');
    $this->addRowAction('edit');
    $this->addRowAction('delete');


El orden de los botones se puede cambiar simplemente cambiando el orden de las llamadas.


**Acciones en masa**

También es posible aplicar acciones en masa como la eliminación masiva de entidades.
Para ello definimos la variable bulk_actions en el constructor.

.. code-block:: php

    $this->bulk_actions = array(
        'delete' => array(
            'text' => $this->l('Eliminar seleccionados'),
            'confirm' => $this->l('¿Seguro que quieres eliminar los items seleccionados?'),
        )
    );


Los bulk actions nativos sólamente son *delete*, *enable*, *disable*. Para que estos 2 últimos funcionen se necesita
que el ObjectModel contenga un campo booleano llamado *active*.

Para crear tu propio bulk action simplemente crea la acción que desees:

.. code-block:: php

    $this->bulk_actions = array(
        'mail' => array(
            'text' => $this->l('Notificar por e-mail'),
            'confirm' => $this->l('¿Estás seguro?')
        )
    )


Y además añade el método que se ejecutará cuando se lance esa bulk action:

.. code-block:: php

    protected function processBulkMailAction()
    {
        Tools::dieObject($this->boxes);
    }


El método $this->boxes devuelve los elementos seleccionados. Además, la llamada dieObject es un método
de debug de Prestashop, la página se detendrá y nos mostrará el contenido de esa variable.


.. note::  Para que se muestre el botón además debes añadir el código que lo genera.

    .. code-block:: php

        public function displayMyActionLink($token, $id)
        {
            $tpl = $this->createTemplate('list_action_my_action.tpl');

            $tpl->assign(array(
                'href' => self::$currentIndex.'&token='.$this->token.'&
                    '.$this->identifier.'='.$id.'&myaction'.$this->table.'=1',
                    'action' => $this->l('My Action')
            ));

            return $tpl->fetch();
        }



Plantilla para el detalle de un objeto
--------------------------------------

Al hacer click en el icono de ver de una fila por defecto se mostrará una página blanca por defecto.

Para crear nuestra propia vista crearemos el fichero views/templates/admin/view.tpl dentro del directorio
del módulo y dentro ponemos cualquier texto.

Para poder mostrar nuestra propia plantilla debemos sobreescribir el método renderView y devolver
la plantilla.

.. code-block:: php

    public function renderView()
    {
        # Al estar en una vista de detalle o edición se puede acceder al objeto desde $this->object
        # Se lo pasamos a smarty

        $tpl = $this->context->smarty->createTemplate($this->_path.'/views/templates/admin/view.tpl');
        $tpl->assign('myobject', $this->object);
        return $tpl->fetch;
    }


En la plantilla podemos utilizar esa variable así

.. code-block:: smarty

    <p>{$myobject->propiedad}</p>


Creando un FormView
-------------------

Para añadir y editar entidades.

El form view funciona de forma similar al list view. Para configurarlo, hay que indicar la variable
$fields_form en el constructor. En este array deben indicarse 3 arrays:

:legend: Contiene 2 parámetros, el titulo del fieldset y la imagen del icono asociado
:input: Los campos editables, dependiendo del campo se definen de diferentes formas:

    - type
        - hidden
        - text
        - tags (requiere el plugin tagify.js)
        - textarea
        - select
        - radio
        - checkbox
        - file
        - password
        - birthday
        - group
        - shop
        - categories
        - color
        - date

    - label
    - desc
    - name
    - size
    - cols: El ancho (sólo textarea)
    - rows: El alto (sólo textarea)
    - required
    - default_value
    - options (para los input tipo select)
        - query: Un array que contiene la lista de opciones a mostrar
        - id: La clave de la query con que se define el valor de una option
        - name: La clave de la query con que se define el label de una option

:submit: Dos parámetros. El título del botón del formulario y el css que se le aplica


Ejemplo:

.. code-block:: php

       $this->context = Context::getContext();
       $this->context->controller = $this;
       $this->fields_form = array(
           'legend' => array(
               'name' => $this->l('Añadir/Editar comentario'),
               'image' => '../img/admin/contact.gif',
           ),
           'input' => array(
               array('type' => 'text', 'label' => $this->l('Comentario'), 'comment' => 'comment', 'required' => true)
           ),
           'submit' => array('title' => $this->l('Guardar'))
       );


Debe ir en el constructor y debemos inicializar a mano el contexto ya que en ese punto todavía no se ha inicializado.


Creando enlaces entre secciones
###############################

Para generar un enlace a otra sección utilizaremos el método link del *context*.
Éste contiene varios métodos según el tipo de enlace que querramos generar.

Por ejemplo, para generar un enlace a otro AdminController lo realizaremos de esta forma.

.. code-block:: php

    # Para un producto de Prestashop
    $product = new Product(1);
    $admin_product_link = $this->context->link->getAdminLink('AdminProducts'.'&updateproduct&id_product='.(int)$product->id_product;

    # Para un cliente
    $customer = new Customer(1);
    $admin_customer_link = $this->context->link->getAdminLink('AdminCustomers').'&viewcustomer&id_customer='.(int)$customer->id_customer;

    # Asignar las variables a Smarty
    $tpl->assign('admin_product_link', $admin_product_link);


.. code-block:: smarty

    {* Utilizar los enlaces en los tpl *}
    <a href="{$admin_product_link}">{$product->name}</a>
