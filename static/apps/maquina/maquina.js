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
    $("#form_tipo").validate({
        rules: {
            nombre: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            descripcion: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre de la maquina",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            descripcion: {
                required: "Por favor ingresa una descripcion",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
        },
    });

    $('#id_new_tipo').on('click', function () {
        $('#Modal').modal('show');
        action = 'add_tipo';
        pk = '';
    });
    var valu = $('#id_serie').val();

    if (valu === 0) {
        $('#id_serie').val('');
    }

    $('#form_tipo').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', action);
        parametros.append('id', pk);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/maquina/nuevo', 'Esta seguro que desea guardar este tipo de maquina?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar tipo de maquina!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        var newOption = new Option(response.tipo['nombre']+' / '+response.tipo['descripcion'], response.tipo['id'], false, true);
                        if (action==='edit_tipo_save'){
                            $('#id_tipo').find("option[value='" + pk + "']").remove();
                        }
                        $('#id_tipo').append(newOption).trigger('change');
                    });
                });
        }
    });

    $('#id_tipo').on('change', function () {
        if ($(this).val()) {
            $('#id_editar_tipo').fadeIn();
            $('#id_new_tipo').fadeOut();
        } else {
            $('#id_editar_tipo').fadeOut();
            $('#id_new_tipo').fadeIn();
        }

    });


    $('#id_editar_tipo').on('click', function () {
        $.ajax({
            type: "POST",
            url: window.location.pathname,
            data: {
                "id": $('#id_tipo').val(),
                'action': 'edit_tipo'
            },
            dataType: 'json',
            success: function (data) {
                $('#Modal').modal('show');
                action = 'edit_tipo_save';
                pk = $('#id_tipo').val();
                $('#id_nombre').val(data[0].nombre);
                $('#id_descripcion').val(data[0].descripcion);
            },
            error: function (xhr, status, data) {
                alert(data);
            },

        });

    });

});
