$(document).ready(function () {
    $('input[name="talla"]').TouchSpin({
        min: 32,
        max: 56,
        step: 2,
    });
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
    $("#form_talla").validate({
        rules: {
            talla: {
                required: true,
                minlength: 1,
                maxlength: 3,
                digits:true
            },
            eqv_letra: {
                required: true,
                minlength: 1,
                maxlength: 4,
                lettersonly: true
            },
        },
        messages: {
            talla: {
                required: "Por favor ingresa una talla",
                minlength: "Debe ingresar al menos un numero",
                digits: "Debe ingresar unicamente numeros"
            },
            eqv_letra: {
                required: "Por favor ingresa la talla equivalente en letras",
                minlength: "Debe ingresar al menos 1 letra",
                maxlength: "Debe ingresar maximo 4 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
        },
    });

});