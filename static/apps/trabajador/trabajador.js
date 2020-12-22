var user_tipo = $('input[name="user_tipo"]').val();
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
    $("#form").validate({
        rules: {
            username: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
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
                digits: true
            },
            correo: {
                required: true,
                email: true
            },
            avatar: {
                required: false
            },
            telefono: {
                required: true,
                minlength: 9,
                digits: true
            },
            celular: {
                required: true,
                minlength: 10,
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            },
            password: {
                required: true,
                minlength: 5
            },


        },
        messages: {
            username: {
                required: "Por favor ingresa un nombre de usuario",
                minlength: "Debe ingresar al menos tres letras"
            },
            first_name: {
                required: "Por favor ingresa tus nombres",
                minlength: "Debe ingresar al menos tres letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            last_name: {
                required: "Por favor ingresa tus apellidos",
                minlength: "Debe ingresar al menos tres letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            cedula: {
                required: "Por favor ingresa tu numero de cedula",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            correo: "Debe ingresar un correo valido",
            cargo: "Debe seleccionar un cargo",
            password: {
                required: "Debe Ingresar una contraseña",
                minlength: "Tu contraseña debe tener al menos 5 digitos"
            },
            telefono: {
                required: "Por favor ingresa tu numero convencional",
                minlength: "Tu numero de documento debe tener al menos 9 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            celular: {
                required: "Por favor ingresa tu numero celular",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            direccion: {
                required: "Por favor ingresa una direccion",
                minlength: "Ingresa al menos 5 letras",
                maxlength: "Tu direccion debe tener maximo 50 caracteres",
            },
        },
    });

    $('#id_nombres').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });
    $('#id_apellidos').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });
    if (user_tipo==='0'){
         $('#id_groups').select2({
        theme: 'classic',
        languaje: 'es',
        placeholder: 'Buscar...',
    }).prop('disabled',true);
    } else {
         $('#id_groups').select2({
        theme: 'classic',
        languaje: 'es',
        placeholder: 'Buscar...',
    });
    }


});
