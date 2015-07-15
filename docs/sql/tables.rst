Tablas
======


Crear
#####


Con clave única:

.. code-block:: sql

    CREATE TABLE `nombre_tabla` (
      `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
      `name` VARCHAR(255) NOT NULL,
      UNIQUE(`name`)
    );


Con claves foráneas y clave única múltiple:

.. code-block:: sql

    CREATE TABLE `mi_tabla` (
        `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `id_otra_tabla` INT UNSIGNED,
        `id_otra_distinta` INT UNSIGNED NOT NULL,
        `name` VARCHAR(255) NOT NULL,
        UNIQUE(`name`, `id_otra_tabla`),
        FOREIGN KEY (`id_otra_tabla`) REFERENCES otra_tabla(`id_otra_tabla`),
        FOREIGN KEY (`id_otra_distinta`) REFERENCES otra_distinta(`id_otra_distinta`)
    );


Tabla con dos campos foráneos como clave primaria. Para crear **relaciones 1-n**:


.. code-block:: sql

    CREATE TABLE `nombre_tabla` (
      `id_uno` INT UNSIGNED NOT NULL,
      `id_dos` INT UNSIGNED NOT NULL,
      FOREIGN KEY (`id_uno`)
        REFERENCES tabla_foranea_uno(`id_foraneo_uno`)
        ON DELETE CASCADE,
      FOREIGN KEY (`id_dos`)
      REFERENCES tabla_foranea_dos(`id_foraneo_dos`)
        ON DELETE CASCADE,
      PRIMARY KEY (`id_uno`, `id_dos`)
    );


Modificar
#########

Añadir campo:

.. code-block:: sql

    ALTER TABLE `nombre_tabla` ADD `id_otra_tabla` int UNSIGNED default null;


Indicar un campo existente como foráneo e indicando un constraint.
En este caso, al eliminarse el elemento padre otra_tabla id_otra_tabla se quedará en null.


.. code-block:: sql

    ALTER TABLE `nombre_tabla`
    ADD FOREIGN KEY (`id_otra_tabla`)
    REFERENCES `otra_tabla`(`id_otra_tabla`) ON DELETE SET NULL;
