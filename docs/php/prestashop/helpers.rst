Helpers
=======


.. role:: php(code)
   :language: php


Funciones
#########

:php:`Tools::dieObject($variable)`
    Muestra el contenido de una variable y detiene la página


:php:`Tools::getIsset($key)`
    Comprueba si una clave existe en $_POST o $_GET


:php:`Tools::isSubmit('nombre-del-campo')`
    Comprueba que el campo submit que indiquemos ha sido enviado


:php:`Tools::getValue('nombre-campo')`
    Obtiene el valor de un campo enviado POST, sino existe, lo intenta
    obtener por GET. De lo contrario devuelve null, a no ser que indiquemos
    un segundo valor para definir el valor por defecto


:php:`Tools::jsonEncode(array('clave' => 'valor'))`
    Convierte un array asociativo en un json


:php:`Configuration::updateValue('CLAVE', 'valor')`
    Guarda un valor en la configuración de prestashop. Si ya existe lo
    sobreescribirá.
    Otra práctica de prestashop es definir la clave en letras mayúsculas.
    Para evitar conflitos con configuraciones de otros
    paquetes mejor añadir el prefijo de nuestro paquete al valor.


:php:`Configuration::get('CLAVE')`
    Devuelve el valor de la clave de configuración indicada


Sólo modo desarrollo
--------------------

:php:`p()`
    Devuelve el contenido de una variable utilizando :php:`print_r()`

:php:`d()`
    Finaliza la ejecución con :php:`die()`


HelperForm
##########

Utilizarlo no es obligatorio pero trae varios beneficios, entre ellos, que sea compatible con las versiones de Prestashop
1.5/1.6 y probablemente, posteriores.

Similar a la definicion de campos de un ObjectModel, debes realizar estos pasos:

    1. Definir el título e icono del fieldset. Recuerda que los iconos de prestashop son de FontAwesome.
    2. Definir el array *fields*
    3. Definir el array *submit*


Por ejemplo:

.. code-block:: php

    $fields_form = array(

        # Si es para indicar en un controlador
        'form' => array(
            'legend' => array(
                'title' => $this->l('Mi formulario'),
                'icon' => 'icon-envelope'
            ),
            'input' => array(
                array(
                    'type'  => 'switch',
                    'label' => $this->l('Activar permisos'),
                    'name' => 'enable_permissions',
                    'desc' => $this->l('Activa los permisos'),
                    'values' => array(
                        array(
                            'id' => 'activar permisos_1',
                            'value' => 1,
                            'label' => $this->l('Activado'),
                        ),
                        array(
                            'id' => 'activar_permisos_0',
                            'value' => 0,
                            'label' => $this->l('Desactivado'),
                        )
                    )
                )
            ),
            'submit' => array(
                'title' => $this->('Guardar'),
            ),
        ),
    )

    # Para generar el HTML a partir de la definición de fields_form debemos realizar estos pasos

    $helper = new HelperForm();
    $helper->table = 'nombre de la tabla'
    $helper->default_form_language = (int)Configuration::get('PS_LANG_DEFAULT');
    $helper->allow_employee_form_lang = (int)Configuration::get('PS_BO_ALOW_EMPLOYEE_FORM_LANG');
    $helper->submit_action = 'miformulariodeprueba';
    $helper->token = Tools::getAdminTokenLite('AdminModules');
    $helper->tpl_vars = array(
        'fields_value' => array('enable_permissions' => Tools::getValue('enable_permissions', false)),
        'languages' => $this->context->controller->getLanguages(),
    );

    return $helper->generateForm(array($fields_form));


Cuidado! Cuando se definen el fields_form a nivel controlador, para utilizar el método renderForm
no se necesita la clave 'form'.


Las opciones que podemos indicar son las siguientes:

:table: Define el atributo id del formulario
:default_form_language: Si es un campo multilang, define que idioma se seleccionará por defecto
:allow_employee_form_lang: En caso de un campo multilang, define si el idioma del empleado deberá ser seleccionado por defecto
:submit_action: Define el nombre del botón submit
:current_index: Define la URL de la acción del formulario
:token: El token de seguridad del formulario. debe estar a la atura con el controlador seleccionado en current_index
:tpl_vars: Define los valores por defecto del formulario y la lista de idiomas disponibles (en caso de campos multilang)


Por último, por ejemplo para utilizar un formulario en la pantalla de configuración, podríamos definirlo así:


.. code-block:: php

    public function getContent()
    {
        $this->processConfiguration();
        $html_confirmation_message = $this->display(__FILE__, 'getContent.tpl');
        $html_form = $this->renderForm();
        return $html_confirmation_Message.$html_form;
    }

Es decir, concatenamos el HTML con la notificación de éxito o fallo y el formulario.
