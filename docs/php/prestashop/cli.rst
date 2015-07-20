Scripts
=======

En Prestashop 1.5 para ejecutar un script ya no es suficiente con lanzar

.. code-block:: php

    require dirname(__FILE__).'/../../config/config.inc.php';


Prestashop busca la tienda en que estamos, sino la encuentra lanza un redirige con headers
y luego nos finaliza el script con un exit.

Para solucionarlo sobreescribimos el siguiente fichero con estos cambios

.. code-block:: php

    // override/classes/shop/Shop.php
    class Shop extends ShopCore {

        /**
         * Find the shop from current domain / uri and get an instance of this shop
         * if INSTALL_VERSION is defined, will return an empty shop object
         *
         * @return Shop
         */
        public static function initialize()
        {
            // Find current shop from URL
            if (!($id_shop = Tools::getValue('id_shop')) || defined('_PS_ADMIN_DIR_'))
            {
                $host = pSQL(Tools::getHttpHost());
                $sql = 'SELECT s.id_shop, CONCAT(su.physical_uri, su.virtual_uri) AS uri, su.domain, su.main
                        FROM '._DB_PREFIX_.'shop_url su
                        LEFT JOIN '._DB_PREFIX_.'shop s ON (s.id_shop = su.id_shop)
                        WHERE (su.domain = \''.$host.'\' OR su.domain_ssl = \''.$host.'\')
                            AND s.active = 1
                            AND s.deleted = 0
                        ORDER BY LENGTH(uri) DESC';

                $id_shop = '';
                $found_uri = '';
                $request_uri = rawurldecode($_SERVER['REQUEST_URI']);
                $is_main_uri = false;
                if ($results = Db::getInstance()->executeS($sql))
                {
                    foreach ($results as $row)
                    {
                        // An URL matching current shop was found
                        if (preg_match('#^'.preg_quote($row['uri'], '#').'#i', $request_uri))
                        {
                            $id_shop = $row['id_shop'];
                            $found_uri = $row['uri'];
                            if ($row['main'])
                                $is_main_uri = true;
                            break;
                        }
                    }
                }

                // If an URL was found but is not the main URL, redirect to main URL
                if ($id_shop && !$is_main_uri)
                {
                    foreach ($results as $row)
                    {
                        if ($row['id_shop'] == $id_shop && $row['main'])
                        {
                            // extract url parameters
                            $request_uri = substr($request_uri, strlen($found_uri));
                            $url = str_replace('//', '/', $row['domain'].$row['uri'].$request_uri);
                            header('HTTP/1.1 301 Moved Permanently');
                            header('Cache-Control: no-cache');
                            header('location: http://'.$url);
                            exit;
                        }
                    }
                }
            }

            if (!$id_shop && defined('_PS_ADMIN_DIR_'))
            {
                // If in admin, we can access to the shop without right URL
                $shop = new Shop(Configuration::get('PS_SHOP_DEFAULT'));
                $shop->physical_uri = preg_replace('#/+#', '/', str_replace('\\', '/', dirname(dirname($_SERVER['SCRIPT_NAME']))).'/');
                $shop->virtual_uri = '';
            }
            elseif ( isset($_SERVER['argc'] )){
                // patch for console script support
                // console sript
                $shop = new Shop(Configuration::get('PS_SHOP_DEFAULT'));

                if (!Validate::isLoadedObject($shop) || !$shop->active || !$id_shop)
                {
                    // No shop found ... too bad, let's redirect to default shop
                    $default_shop = new Shop(Configuration::get('PS_SHOP_DEFAULT'));

                    // Hmm there is something really bad in your Prestashop !
                    if (!Validate::isLoadedObject($default_shop))
                        throw new PrestaShopException('Shop not found');
                }
                // patch for console script support
                // console sript

            }
            else
            {
                $shop = new Shop($id_shop);
                if (!Validate::isLoadedObject($shop) || !$shop->active || !$id_shop)
                {
                    // No shop found ... too bad, let's redirect to default shop
                    $default_shop = new Shop(Configuration::get('PS_SHOP_DEFAULT'));

                    // Hmm there is something really bad in your Prestashop !
                    if (!Validate::isLoadedObject($default_shop))
                        throw new PrestaShopException('Shop not found');

                    $params = $_GET;
                    unset($params['id_shop']);
                    if (!Configuration::get('PS_REWRITING_SETTINGS'))
                        $url = 'http://'.$default_shop->domain.$default_shop->getBaseURI().'index.php?'.http_build_query($params);
                    else
                    {
                        // Catch url with subdomain "www"
                        if (strpos($default_shop->domain, 'www.') === 0 && 'www.'.$_SERVER['HTTP_HOST'] === $default_shop->domain
                            || $_SERVER['HTTP_HOST'] === 'www.'.$default_shop->domain)
                            $uri = $default_shop->domain.$_SERVER['REQUEST_URI'];
                        else
                            $uri = $default_shop->domain.$default_shop->getBaseURI();

                        if (count($params))
                            $url = 'http://'.$uri.'?'.http_build_query($params);
                        else
                            $url = 'http://'.$uri;
                    }
                    header('location: '.$url);
                    exit;
                }
            }

            self::$context_id_shop = $shop->id;
            self::$context_id_shop_group = $shop->id_shop_group;
            self::$context = self::CONTEXT_SHOP;

            return $shop;
        }
}


El código nuevo es este else if que comprueba si existe ARGS y por tanto estamos desde un script,
en ese caso inicializa la tienda por defecto.

.. code-block:: php

        elseif ( isset($_SERVER['argc'] )){
            // patch for console script support
            // console sript
            $shop = new Shop(Configuration::get('PS_SHOP_DEFAULT'));

            if (!Validate::isLoadedObject($shop) || !$shop->active || !$id_shop)
            {
                // No shop found ... too bad, let's redirect to default shop
                $default_shop = new Shop(Configuration::get('PS_SHOP_DEFAULT'));

                // Hmm there is something really bad in your Prestashop !
                if (!Validate::isLoadedObject($default_shop))
                    throw new PrestaShopException('Shop not found');
            }
            // patch for console script support
            // console script

        }


Fuente: http://www.pounstudio.com/fragua/
