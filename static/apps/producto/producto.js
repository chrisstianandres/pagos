$(document).ready(function () {
    edit_cat();
    var action = '';
    var pk = '';
    $('input[name="pvp"], input[name="pvp_alq"], input[name="pvp_confec"]').TouchSpin({
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
            categoria: {
                required: true
            },
            presentacion: {
                required: true
            },
        },
        messages: {
            nombre: {
                required: "Porfavor ingresa el nombre del producto",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            descripcion: {
                required: "Porfavor ingresa una descripcion del producto",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            categoria: {
                required: "Debe escoger una categoria de producto",

            },
            presentacion: {
                required: "Debe escoger una presentacion de producto",

            },
        },
    });
    $('#id_nombre').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });
    $('#id_descripcion').keyup(function () {
        var pal = $(this).val();
        var changue = pal.substr(0, 1).toUpperCase() + pal.substr(1);
        $(this).val(changue);
    });

    $('#id_new_producto').on('click', function () {
        $('#Modal_prod').modal('show');
        action = 'add';
        pk = '';
    });
    $('#id_new_categoria').on('click', function () {
        $('#Modal').modal('show');
        action = 'add';
        pk = '';
    });
    $('#id_new_presentacion').on('click', function () {
        $('#Modal2').modal('show');
        action = 'add';
        pk = '';
    });
    $('#id_producto_base')
        .select2({
            theme: "classic",
            language: {
                inputTooShort: function () {
                    return "Ingresa al menos un caracter...";
                },
                "noResults": function () {
                    return "Sin resultados";
                },
                "searching": function () {
                    return "Buscando...";
                }
            },
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: '/producto/nuevo',
                data: function (params) {
                    var queryParameters = {
                        term: params.term,
                        'action': 'search'
                    };
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data,
                    };
                },
            },
            placeholder: 'Busca un Producto',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            $.ajax({
                type: "POST",
                url: '/producto/nuevo',
                data: {
                    "id": $('#id_producto_base option:selected').val(),
                    'action': 'get'
                },
                dataType: 'json',
                success: function (data) {
                  console.log(data[0].descripcion);
                    $('#id_des').val(data[0].descripcion);
                    $('#id_cat').val(data[0]['categoria'].nombre);
                    $('#id_pres').val(data[0]['presentacion'].nombre);
                },
                error: function (xhr, status, data) {
                    alert(data);
                },

            })
        });

    $('#form_prod').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add_base');
        parametros.append('id', '');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este producto?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este producto!', 'far fa-smile-wink', function () {
                        $('#Modal_prod').modal('hide');
                        var newOption = new Option(response.producto_base['nombre'], response.producto_base['id'], false, true);
                        $('#id_producto_base').append(newOption).trigger('change');
                    });
                });
        }
    });
    $('#form_cat').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', action);
        parametros.append('id', pk);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/categoria/nuevo', 'Esta seguro que desea guardar esta categoria?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta categoria!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        var newOption = new Option(response.categoria['nombre'], response.categoria['id'], false, true);
                        $('#id_categoria').append(newOption).trigger('change');
                    });
                });
        }
    });
    $('#form_pre').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', action);
        parametros.append('id', pk);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/presentacion/nuevo', 'Esta seguro que desea guardar esta presentacion?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta presentacion!', 'far fa-smile-wink', function () {
                        $('#Modal2').modal('hide');
                        var newOption = new Option(response.presentacion['full'], response.presentacion['id'], false, true);
                        $('#id_presentacion').append(newOption).trigger('change');
                    });
                });
        }
    });

});

function edit_cat() {

    if ($('#id_producto_base').val() !== ''){
        $.ajax({
                type: "POST",
                url: '/producto/nuevo',
                data: {
                    "id": $('#id_producto_base').val(),
                    'action': 'get'
                },
                dataType: 'json',
                success: function (data) {
                  console.log(data);
                    $('#id_des').val(data[0].descripcion);
                    $('#id_cat').val(data[0]['categoria'].nombre);
                    $('#id_pres').val(data[0]['presentacion'].nombre);
                },
                error: function (xhr, status, data) {
                    alert(data);
                },
            })
    }

}
