$(document).ready(function () {
    var action = '';
    var pk = '';
    $('input[name="p_compra"]').TouchSpin({
        min: 1.00,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        forcestepdivisibility: 'none',
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    });
    $('.select2').select2({
        language: {
            "noResults": function () {
                return "Sin resultados";
            }
        },
        theme: "classic"
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
            ud_medida: {
                required: true,
                lettersonly: true,
                minlength: 1,
                maxlength: 10
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
            ud_medida: {
                required: "Porfavor ingresa una unidad de medida",
                minlength: "Debe ingresar al menos 3 letras",
                lettersonly: "Debe ingresar unicamente letras y espacios"
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
    $('#id_descripcion').keyup(function () {
        var changue = titleCase($(this).val());
        $(this).val(changue);
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
    $('#id_new_tipo_material').on('click', function () {
        $('#Modal_tipo').modal('show');
        action = 'add';
        pk = '';
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
    $('#form_tipo').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', action);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/tipo_mat/nuevo', 'Esta seguro que desea guardar este tipo de material?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este tipo de material!', 'far fa-smile-wink', function () {
                        $('#Modal_tipo').modal('hide');
                        var newOption = new Option(response.tipo_material['nombre'], response.tipo_material['id'], false, true);
                        $('#id_tipo_material').append(newOption).trigger('change');
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

    $('#id_new_color').on('click', function () {
        $('#Modal_color').modal('show');
        action = 'add';
        pk = '';
    });
    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return this.optional(element) || /^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/i.test(value);
        //[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$
    }, "Letters and spaces only please");


    $('#id_medida').TouchSpin({
        min: 1,
        max: 1000000,
        step: 1
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
