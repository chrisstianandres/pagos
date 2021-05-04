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

    $.validator.addMethod("tipo", function (value, element) {

        var tipo = $("#id_tipo").val();
        if (tipo === '0') {
            return ((value.length === 10));
        } else if (tipo === '1') {
            return ((value.length === 13));
        }
    }, "");

    $("#form").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 5,
                maxlength: 50,
                lettersonly: true,
            },
            tipo: {
                required: true
            },
            num_doc: {
                required: true,
                tipo: true,
                digits: true,
                validar: true
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
            nombre: {
                required: "Porfavor ingresa tus nombres y apellidos",
                minlength: "Debe ingresar al menos un nombre y un apellido",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            num_doc: {
                required: "Por favor ingresa tu numero de documento",
                tipo: "Error en el numero de digitos (10 para cedula o 13 para ruc)",
                digits: "Debe ingresar unicamente numeros",
                val_ced: "Numero de documento no valido para Ecuador",
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

    $('#id_nombre')
        .keyup(function () {
            var changue = titleCase($(this).val());
            $(this).val(changue);
        })
        .keypress(function (e) {
            if (e.which >= 48 && e.which <= 57) {
                return false;
            }
        });  //Para solo letras


    $('#id_telefono').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros


    $('#id_num_doc').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros


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
 $('#Modal').on('hidden.bs.modal', function () {
        reset_form('form');
    });

jQuery.validator.addMethod("validar", function (value, element) {
    return validar(element);
}, "Número de documento no valido para Ecuador");

function validar(element) {
    var cad = document.getElementById(element.id).value.trim();
    var total = 0;
    var longitud = cad.length;
    var longcheck = longitud - 1;
    if (longitud === 10) {
        return aux(total, cad);
    } else if (longitud === 13 && cad.slice(10, 13) !== '000') {
        return aux(total, cad);
    } else {
        return false;
    }
}

function aux(total, cad) {
    if (cad !== "") {
        for (var i = 0; i < 9; i++) {
            if (i % 2 === 0) {
                var aux = cad.charAt(i) * 2;
                if (aux > 9) aux -= 9;
                total += aux;
            } else {
                total += parseInt(cad.charAt(i)); // parseInt o concatenará en lugar de sumar
            }
        }

        total = total % 10 ? 10 - total % 10 : 0;
        return parseInt(cad.charAt(9)) === total;
    }
}
