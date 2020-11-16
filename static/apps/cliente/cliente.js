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
            nombres: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
            apellidos: {
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
            telefono: {
                required: true,
                minlength: 10,
                digits: true
            },
            direccion: {
                required: true,
                minlength: 5,
                maxlength: 50
            },


        },
        messages: {
            nombres: {
                required: "Porfavor ingresa tus nombres",
                minlength: "Debe ingresar al menos un nombre",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            apellidos: {
                required: "Porfavor ingresa tus apellidos",
                minlength: "Debe ingresar al menos un apellido",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            cedula: {
                required: "Porfavor ingresa tu numero de documento",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            correo: "Debe ingresar un correo valido",
            telefono: {
                required: "Porfavor ingresa tu numero celular",
                minlength: "Tu numero de documento debe tener al menos 10 digitos",
                digits: "Debe ingresar unicamente numeros",
                maxlength: "Tu numero de documento debe tener maximo 10 digitos",
            },
            direccion: {
                required: "Porfavor ingresa una direccion",
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

});



