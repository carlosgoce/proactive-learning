Smarty
=======

Variables
#########

Disponemos de smarty en la variable $this->context.
Sabiendo esto podemos definir valores a pasar a la plantilla así:


.. code-block:: php

                                                         $this->context->smarty->assign('clave', 'valor');

Después en la plantilla podremos utilizarlo, por ejemplo, de esta forma:


.. code-block:: smarty

    {if isset($clave)}
        <div class="alert alert-success">Configuración actualizada</div>
    {/if}


Manualmente
###########

Para generar una cadena a partir de una plantilla smarty manualmente

.. code-block:: php

    $helper = new HelperList($context);
    $helper->base_folder = dirname(__FILE__).'/directorio/base/plantillas/';
    $tpl = $helper->createTemplate('template.tpl');
    $tpl->assign(array('var1' => $value, 'var2' => $value2));
	$templateString = $tpl->fetch();
