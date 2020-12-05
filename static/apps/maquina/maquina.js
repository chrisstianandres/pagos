$(document).ready(function () {
    $('.select2').select2({
        language: {
            "noResults": function () {
                return "Sin resultados";
            }
        },
        theme: "classic"
    });

    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return this.optional(element) || /^[a-zA-z\s\ñ\Ñ," "]+$/i.test(value);
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
            tipo: {
                required: true,
            },
            serie: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
        },
        messages: {
            tipo: {
                required: "Porfavor escoje un tipo de maquina",
            },
            serie: {
                required: "Porfavor ingresa una serie",
                minlength: "Debe ingresar al menos 3 caracteres",
                maxlength: "Debe ingresar hasta 50 caracteres"
            },
        },
    });

    $('#id_new_tipo').on('click', function () {
        $('#Modal').modal('show');
        action = 'add';
        pk = '';
    });
    var valu = $('#id_serie').val();

    if (valu===0){
        $('#id_serie').val('');
    }

    $('#form_tipo').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add_tipo');
        parametros.append('id', '');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/maquina/nuevo', 'Esta seguro que desea guardar este tipo de maquina?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar tipo de maquina!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        var newOption = new Option(response.tipo['nombre'], response.tipo['id'], false, true);
                        $('#id_tipo').append(newOption).trigger('change');
                    });
                });
        }
    });

});
