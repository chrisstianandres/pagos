$(document).ready(function () {

    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return this.optional(element) || /^[a-zA-z\s\ñ\Ñ," "]+$/i.test(value);
    }, "Letters and spaces only please");


    $.validator.setDefaults({
        errorClass: 'invalid-feedback',

        highlight: function (element, errorClass, validClass) {
            $(element)
                .addClass("is-invalid")
                .removeClass("is-valid");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element)
                .addClass("is-valid")
                .removeClass("is-invalid");
        }
    });
    $("#form").validate({
        rules: {
            titulo: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            mision: {
                required: true,
                minlength: 5,
                maxlength: 500
            },
            vision: {
                required: true,
                minlength: 5,
                maxlength: 500
            },
            mapa: {
                required: true,
                minlength: 5,
                maxlength: 500
            }
        },
        messages: {
            titulo: {
                required: "Porfavor ingresa un titulo para el sitio",
                minlength: "Debe ingresar al menos 3 letras",
                maxlength: "Ingresa maximo 50 caracteres",
            },
            mision: {
                required: "Porfavor ingresa una mision",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Ingresa maximo 500 caracteres",
            },
             vision: {
                required: "Porfavor ingresa una vision",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Ingresa maximo 500 caracteres",
            },
            mapa: {
                required: "Porfavor copia y pega un mapa de google y pegalo aqui",
            },
        },
    });

    $('#id_titulo').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });
    $('#id_mision #id_vision').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });

});
