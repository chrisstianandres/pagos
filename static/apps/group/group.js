$(document).ready(function () {
    $('#id_permissions').select2({
        theme: 'classic',
        languaje: 'es',
        placeholder: 'Buscar...',
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
    $("#form").validate({
        rules: {
            name: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            permissions: {
                required: true,
            }
        },
        messages: {
            name: {
                required: "Por favor escribre un nombre para el grupo",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            permissions: {
                required: "Por favor selecciona al menos un permiso",
            },
        },
    });
    $('#id_detalle').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });

});
