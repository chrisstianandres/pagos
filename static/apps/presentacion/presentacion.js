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
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            abreviatura: {
                required: true,
                maxlength: 50,
            },
            descripcion: {
                required: true,
                minlength: 5,
                maxlength: 50
            }
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre de la categoria",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            abreviatura: {
                required: "Por favor ingresa una abreviatura"
            },
            descripcion: {
                required: "Por favor ingresa una descripcion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "La descripcion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_nombre').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });
    $('#id_descripcion').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });

});
