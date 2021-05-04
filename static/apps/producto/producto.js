var datatable;
$(document).ready(function () {
    edit_cat();
    var action = '';
    var pk = '';
    $('input[name="pvp"]').TouchSpin({
        min: 1.00,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        forcestepdivisibility: 'none',
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    }).on('change keyup', function () {
        $('input[name="pvp_alq"]').trigger('touchspin.destroy');
        precio();
    }).keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 46 || e.which > 57 || e.which === 47)) {
            return false;
        }
    });
    precio();

    function precio() {
        var max = $('input[name="pvp"]').val();
        $('input[name="pvp_alq"]').val(1.00).TouchSpin({
            min: 1.00,
            max: parseFloat(max).toFixed(2),
            step: 0.01,
            decimals: 2,
            forcestepdivisibility: 'none',
            boostat: 5,
            maxboostedstep: 10,
            prefix: '$'
        }).prop('readonly', true);
    }

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
            producto_base: {
                required: true
            },
            descripcion: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            categoria: {
                required: true
            },
            color: {
                required: true
            },
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre del producto",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            producto_base: {
                required: "Elige un producto producto"
            },
            descripcion: {
                required: "Por favor ingresa una descripcion del producto",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            categoria: {
                required: "Debe escoger una categoria de producto",

            },
            color: {
                required: "Debe escoger un color",

            },
        },
    });
    $('#id_nombre_producto').keyup(function () {
        var changue = titleCase($(this).val());
        $(this).val(changue);
    }).keypress(function (e) {
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    });  //Para solo letras
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
    $('#id_new_talla').on('click', function () {
        $('#Modal_talla').modal('show');
        action = 'add';
        pk = '';
    });

    $('#id_new_color').on('click', function () {
        $('#Modal_color').modal('show');
        action = 'add';
        pk = '';
    });


    $('#id_search_producto').on('click', function () {
        $('#Modal_prod_table').modal('show');
        datatable = $('#datatable').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
            },
            ajax: {
                url: '/producto/lista',
                type: 'POST',
                data: {'action': 'list_add'},
                dataSrc: ""
            },
            columns: [
                {"data": "nombre"},
                {"data": "categoria.nombre"},
                {"data": "descripcion"},
                {"data": "id"}
            ],
            columnDefs: [
                {
                    targets: '__all',
                    class: 'text-center'
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a style="color: white" type="button" class="btn btn-success btn-xs" rel="select" ' +
                            'data-toggle="tooltip" title="Selcionar producto"><i class="fa fa-check"></i></a>' + ' ';

                    }
                },
            ]
        })
    });

    $('#datatable tbody')
        .on('click', 'a[rel="select"]', function () {
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'get'};
            $.ajax({
                dataType: 'JSON',
                type: 'POST',
                url: '/producto/nuevo',
                data: parametros,
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    var new_data = {
                        id: data[0].id,
                        text: data[0].nombre
                    };
                    var newOption = new Option(new_data.text, new_data.id, false, true);
                    $('#id_producto_base').append(newOption).trigger('change');
                    $('#id_des').val(data[0].descripcion);
                    $('#id_cat').val(data[0]['categoria'].nombre);
                    $('#Modal_prod_table').modal('hide');
                    return false;
                }
                menssaje_error(data.error, data.content, 'fa fa-times-circle');
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            });
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
                    return {
                        term: params.term,
                        'action': 'search'
                    };
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
                    $('#id_des').val(data[0].descripcion);
                    $('#id_cat').val(data[0]['categoria'].nombre);
                    $('#id_col').val(data[0]['color'].nombre);
                },
                error: function (xhr, status, data) {
                    alert(data);
                },

            })
        })
        .on("change", function () {
            if ($(this).val() === "") {
                $('#id_des').val("");
                $('#id_cat').val("");
                $('#id_col').val("");
            }
        });

    $('#id_despcripcion_producto')
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
                url: '/categoria/nuevo',
                data: function (params) {
                    return {
                        term: params.term,
                        'action': 'search'
                    };
                },
                processResults: function (data) {
                    return {
                        results: data,
                    };
                },
            },
            placeholder: 'Busca una Categoria',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            $.ajax({
                type: "POST",
                url: '/categoria/nuevo',
                data: {
                    "id": $('#id_despcripcion_producto option:selected').val(),
                    'action': 'get'
                },
                dataType: 'json',
                success: function (data) {
                    var newOption = new Option(data[0]['nombre'], data[0]['id'], false, true);
                    $('#id_despcripcion_producto').append(newOption).trigger('change');
                },
                error: function (xhr, status, data) {
                    alert(data);
                },

            })
        });
    $('#id_color')
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
                url: '/color/nuevo',
                data: function (params) {
                    return {
                        term: params.term,
                        'action': 'search'
                    };
                },
                processResults: function (data) {
                    return {
                        results: data,
                    };
                },
            },
            placeholder: 'Busca un color',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            $.ajax({
                type: "POST",
                url: '/color/nuevo',
                data: {
                    "id": $('#id_color option:selected').val(),
                    'action': 'get'
                },
                dataType: 'json',
                success: function (data) {
                    var newOption = new Option(data[0]['nombre'], data[0]['id'], false, true);
                    $('#id_color').append(newOption).trigger('change');
                },
                error: function (xhr, status, data) {
                    alert(data);
                },

            })
        });

    $('#id_talla')
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
            placeholder: 'Busca una talla',
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
                        $('#id_des').val(response.producto_base.descripcion);
                        $('#id_cat').val(response.producto_base.categoria.nombre);
                        $('#id_col').val(response.producto_base.color.nombre);
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
                        $('#id_despcripcion_producto').append(newOption).trigger('change');
                    });
                });
        }
    });
    $('#form_talla').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/talla/nuevo', 'Esta seguro que desea guardar esta talla?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta talla!', 'far fa-smile-wink', function () {
                        $('#Modal_talla').modal('hide');
                        var newOption = new Option(response.talla['talla'] + '/' + response.talla['eqv_letra'], response.talla['id'], false, true);
                        $('#id_talla').append(newOption).trigger('change');
                    });
                });
        }
    });

    $('#form_color').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/color/nuevo', 'Esta seguro que desea guardar este color?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este color!', 'far fa-smile-wink', function () {
                        $('#Modal_color').modal('hide');
                        var newOption = new Option(response.color['nombre'], response.color['id'], false, true);
                        $('#id_color').append(newOption).trigger('change');
                    });
                });
        }
    });


    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add');
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar esta prenda?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta prenda!', 'far fa-smile-wink', function () {
                        window.location.replace('/producto/lista')
                    });
                });
        }
    });


    $("#form_prod").validate({
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
            }
        },
        messages: {
            nombre: {
                required: "Por favor ingresa el nombre del producto",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            producto_base: {
                required: "Elige un producto producto"
            },
            descripcion: {
                required: "Por favor ingresa una descripcion del producto",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            categoria: {
                required: "Debe escoger una categoria de producto",

            }
        },
    });

    $('#Modal_prod').on('hidden.bs.modal', function () {
        reset_form('#form_prod');
    });

    $('#Modal').on('hidden.bs.modal', function () {
        reset_form('#form_cat');
    });

     $('#Modal_color').on('hidden.bs.modal', function () {
        reset_form('#form_color');
    });

     $('#Modal_talla').on('hidden.bs.modal', function () {
        reset_form('#form_talla');
    });

});

function edit_cat() {

    if ($('#id_producto_base').val() !== '') {
        $.ajax({
            type: "POST",
            url: '/producto/nuevo',
            data: {
                "id": $('#id_producto_base').val(),
                'action': 'get'
            },
            dataType: 'json',
            success: function (data) {
                $('#id_des').val(data[0].descripcion);
                $('#id_cat').val(data[0]['categoria'].nombre);
            },
            error: function (xhr, status, data) {
                alert(data);
            },
        })
    }

}
