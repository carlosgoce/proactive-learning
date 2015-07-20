Imágenes
========


Autocargar imagen en div
########################

.. code-block:: html

    <form id="form1">
        <input type='file' id="imgInp" />
        <img id="blah" src="#" alt="your image" />
    </form>


.. code-block:: javascript

    function readURL(input) {

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#blah').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imgInp").change(function(){
        readURL(this);
    });
