$(document).ready(function () {
    $('input[name="valor"]').TouchSpin({
        min: 0.05,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        forcestepdivisibility: 'none',
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
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
            tipo_gasto: {
                required: true
            },
            detalle: {
                required: true,
                minlength: 3,
                maxlength: 50
            }
        },
        messages: {
            tipo_gasto: {
                required: "Porfavor selecciona un tipo de gasto",
            },
            detalle: {
                required: "Porfavor ingresa un detalle",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
        },
    });
    $('#id_detalle').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });

});
