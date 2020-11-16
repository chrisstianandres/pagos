$(function () {
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
            password: {
                required: true,
                minlength: 3,
                maxlength: 50
            }
        },
        messages: {
            username: {
                required: "Porfavor ingresa un usuario valido",
                minlength: "Debe ingresar al menos 3 caracteres"
            },
            password: {
                required: "Porfavor ingresa una contraseña valida",
                minlength: "Debe ingresar al menos 3 caracteres"
            }
        },
    });
    $('#log').on('click', function () {

        if ($('input[name="username"]').val() === "") {
            menssaje_error('Error!', "Debe ingresar un Username", 'far fa-times-circle');
            return false
        } else if ($('input[name="password"]').val() === "") {
            menssaje_error('Error!', "Debe ingresar una contraseña", 'far fa-times-circle');
            return false
        }
        var parametros;
        parametros = {
            'username': $('input[name="username"]').val(),
            'password': $('input[name="password"]').val()
        };
        login('/connect/', parametros, function () {
            window.$.dialog({
                icon: 'fa fa-spinner fa-spin',
                title: 'Iniciando Sesion!',
                content: false
            });
            setTimeout(function () {
                location.href = '/';
            }, 2000);

        }, function () {
            $('input[name="username"]').val("");
            $('input[name="password"]').val("");
            reset();

        });
    });
});

