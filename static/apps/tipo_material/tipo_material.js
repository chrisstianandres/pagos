$(document).ready(function () {

    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return this.optional(element) || /^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/i.test(value);
        //[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$
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
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre del tipo de material",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios",
            },
        },
    });

    $("#form_tipo").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre del tipo de material",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios",
            },
        },
    });

    $('#id_nombre_tipo_material')
        .keyup(function () {
            var changue = titleCase($(this).val());
            $(this).val(changue);
        })
        .keypress(function (e) {
            if (e.which >= 48 && e.which <= 57) {
                return false;
            }
        });  //Para solo letras


    $('#Modal').on('hidden.bs.modal', function () {
        reset_form('form');
    });
});


function titleCase(texto) {
        const re = /(^|[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ])(?:([a-záéíóúüñ])|([A-ZÁÉÍÓÚÜÑ]))|([A-ZÁÉÍÓÚÜÑ]+)/gu;
        return texto.replace(re,
            (m, caracterPrevio, minuscInicial, mayuscInicial, mayuscIntermedias) => {
                const locale = ['es', 'gl', 'ca', 'pt', 'en'];
                if (mayuscIntermedias)
                    return mayuscIntermedias.toLocaleLowerCase(locale);
                return caracterPrevio + (minuscInicial ? minuscInicial.toLocaleUpperCase(locale) : mayuscInicial);
            }
        );
    }