$(document).ready(function () {
    var option = $('input[name="option"]').val();
    if (option === 'editar') {
        $('#id_cedula').attr('readonly', 'true');
    }

    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return this.optional(element) || /^[a-z," "]+$/i.test(value);
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

    validar();
    $("#form").validate({
        rules: {
            first_name: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            last_name: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            cedula: {
                required: true,
                minlength: 10,
                maxlength: 10,
                digits: true,
                val_ced: true
            },
            email: {
                required: true,
                email: true
            },
            telefono: {
                required: true,
                minlength: 9,
                maxlength: 9,
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            },


        },
        messages: {
            first_name: {
                required: "Por favor ingresa tus nombres",
                minlength: "Debe ingresar al menos un nombre",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            last_name: {
                required: "Por favor ingresa tus apellidos",
                minlength: "Debe ingresar al menos un apellido",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            cedula: {
                required: "Por favor ingresa tu numero de documento",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
                val_ced: "Numero de cedula no valido para Ecuador"
            },
            email: "Debe ingresar un correo valido",
            telefono: {
                required: "Por favor ingresa tu numero celular",
                minlength: "Tu numero de documento debe tener al menos 9 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 9 digitos",
            },
            direccion: {
                required: "Por favor ingresa una direccion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Tu direccion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_first_name').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });

});



