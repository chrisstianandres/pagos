$(document).ready(function () {
    $('#id_nombre').attr('readonly', true);
    $('#id_ciudad').attr('readonly', true);
    $('#id_ruc').attr('readonly', true);
    $('#id_correo').attr('readonly', true);
    $('#id_direccion').attr('readonly', true);
    $('#id_facebook').attr('readonly', true);
    $('#id_instagram').attr('readonly', true);
    $('#id_twitter').attr('readonly', true);
    $('#id_telefono').attr('readonly', true);
    $('#id_indice').TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '%'
    }).prop('disabled', true);
    $('#editar').on("click", editar);
    $('input[name="iva"]').TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '%'
    }).prop('disabled', true);

});

function editar() {
    $('#guardar').show();
    $('#editar').hide();
    $('#id_nombre').attr('readonly', false);
    $('#id_ciudad').attr('readonly', false);
    $('#id_ruc').attr('readonly', false);
    $('#id_correo').attr('readonly', false);
    $('#id_direccion').attr('readonly', false);
    $('#id_facebook').attr('readonly', false);
    $('#id_instagram').attr('readonly', false);
    $('#id_twitter').attr('readonly', false);
    $('#id_iva').prop('disabled', false);
    $('#id_indice').prop('disabled', false);
    $('#id_telefono').attr('readonly', false);
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
$("#signupForm").validate({
    rules: {
        nombre: {
            required: true,
            minlength: 3,
            maxlength: 20
        },
        ciudad: {
            required: true,
            minlength: 3,
            maxlength: 25
        },
        ruc: {
            required: true,
            minlength: 13,
            maxlength: 13,
            digits: true
        },
        correo: {
            required: true,
            email: true
        },
        direccion: {
            required: true,
            minlength: 5,
            maxlength: 50
        },
        facebook: {
            required: false
        },
        instagram: {
            required: false
        },
        twitter: {
            required: false
        },
        telefono: {
            required: true,
            minlength: 10,
            maxlength: 10,
            digits: true
        },
    },
    messages: {
        nombre: {
            required: "Porfavor ingresa el nombre de la empresa",
            minlength: "Debe ingresar al menos 3 letras",
            maxlength: "Debe ingresar hasta 20 letras",
            lettersonly: "Debe ingresar unicamente letras y espacios"
        },
        ciudad: {
            required: "Porfavor ingresa la ciudad donde se encuentra la empresa",
            minlength: "Debe ingresar al menos 3 letras",
            maxlength: "Debe ingresar hasta 25 letras",
            lettersonly: "Debe ingresar unicamente letras y espacios"
        },
        ruc: {
            required: "Porfavor ingresa el numero de ruc",
            minlength: "Tu numero de documento debe tener al menos 13 digitos",
            maxlength: "Tu numero de documento debe tener hasta 13 digitos",
            digits: "Debe ingresar unicamente numeros"
        },
        telefono: {
            required: "Porfavor ingresa el numero celular de la empresa",
            minlength: "Tu numero de documento debe tener al menos 10 digitos",
            digits: "Debe ingresar unicamente numeros",
            maxlength: "EL numero de documento debe tener maximo 10 digitos",
        },
        direccion: {
            required: "Porfavor ingresa una direccion de la empresa",
            minlength: "Ingresa al menos 5 letras",
            maxlength: "Tu direccion debe tener maximo 50 caracteres",
        }
    },
});

