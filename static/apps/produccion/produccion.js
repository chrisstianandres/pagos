var tblproductos;
var tblperdidas_productos;
var tblperdidas_materiales;
var data_asig='';
var produccion = {
    items: {
        fecha_ingreso: '',
        asignacion: '',
        novedades: '',
        productos: [],
        perdidas_productos: [],
        perdidas_materiales: [],
    },
    add: function (data) {
        this.items.productos.push(data[0]);
        this.items.productos = this.exclude_duplicados(this.items.productos);
        this.list();

    },
    list: function () {
        tblproductos = $("#tblinventario").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: this.items.productos,
            columns: [
                {data: 'id'},
                {data: "producto_base.nombre"},
                {data: "producto_base.categoria.nombre"},
                {data: "producto_base.presentacion.nombre"},
                {data: "cantidad"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Insumo"><i class="fa fa-trash-alt"></i></a>';
                        //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';

                    }
                },
                {
                    targets: '_all',
                    class: 'text-center'
                },
            ],
            rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 10000000,
                    step: 1
                });
            },
        });
    },

    add_perdida_producto: function (data) {
        console.log(data);
        this.items.perdidas_productos.push(data[0]);
        this.items.perdidas_productos = this.exclude_duplicados_perdidas_productos(this.items.perdidas_productos);
        this.list_perdidas_productos();

    },
    list_perdidas_productos: function () {
        tblperdidas_productos = $("#tblperdidas_productos").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: this.items.perdidas_productos,
            columns: [
                {data: 'id'},
                {data: "producto_base.nombre"},
                {data: "producto_base.categoria.nombre"},
                {data: "producto_base.presentacion.nombre"},
                {data: "cantidad"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Insumo"><i class="fa fa-trash-alt"></i></a>';
                        //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';

                    }
                },
                {
                    targets: '_all',
                    class: 'text-center'
                },
            ],
            rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 10000000,
                    step: 1
                });
            },
        });
    },

    add_perdida_materiales: function (data) {
        this.items.perdidas_materiales.push(data);
        this.items.perdidas_materiales = this.exclude_duplicados_perdidas_materiales(this.items.perdidas_materiales);
        this.list_perdidas_materiales();

    },
    list_perdidas_materiales: function () {
        tblperdidas_materiales = $("#tblperdidas_materiales").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: this.items.perdidas_materiales,
            columns: [
                {data: 'id'},
                {data: "nombre"},
                {data: "categoria.nombre"},
                {data: "presentacion.nombre"},
                {data: "cantidad"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Insumo"><i class="fa fa-trash-alt"></i></a>';
                        //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="'+data+'">';

                    }
                },
                {
                    targets: '_all',
                    class: 'text-center'
                },
            ],
            rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.max,
                    step: 1
                });
            },
        });
    },

    exclude_duplicados: function (array) {
        this.items.productos = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;

    },
    exclude_duplicados_perdidas_productos: function (array) {
        this.items.perdidas_productos = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;

    },
    exclude_duplicados_perdidas_materiales: function (array) {
        this.items.perdidas_materiales = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;

    }

};
$(function () {
    //seleccionar producto del select producto
    $('#id_producto').on('select2:select', function (e) {
        $.ajax({
            type: "POST",
            url: '/producto/lista',
            data: {
                "id": $('#id_producto option:selected').val(),
                "action": 'get_rep'
            },
            dataType: 'json',
            success: function (data) {
                produccion.add(data);
                $('#id_producto').val(null).trigger('change');
            },
            error: function (xhr, status, data) {
                menssaje_error('Error', data[0], 'fa fa-times', function () {

                });
            },

        })
    })
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
                url: '/producto/lista',
                data: function (params) {
                    var queryParameters = {
                        term: params.term,
                        'action': 'search_rep'
                    };
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca un Producto',
            minimumInputLength: 1,
        });

    $('#id_productos_perdida').on('select2:select', function (e) {
        $.ajax({
            type: "POST",
            url: '/producto/lista',
            data: {
                "id": $('#id_productos_perdida option:selected').val(),
                "action": 'get_rep'
            },
            dataType: 'json',
            success: function (data) {
                produccion.add_perdida_producto(data);
                $('#id_productos_perdida').val(null).trigger('change');
            },
            error: function (xhr, status, data) {
                menssaje_error('Error', data[0], 'fa fa-times', function () {

                });
            },

        })
    })
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
                url: '/producto/lista',
                data: function (params) {
                    var queryParameters = {
                        term: params.term,
                        'action': 'search_rep'
                    };
                    return queryParameters;
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca un Producto',
            minimumInputLength: 1,
        });

    $('#id_material').on('select2:select', function (e) {
        $.ajax({
            type: "POST",
            url: '/material/lista',
            data: {
                "id": $('#id_material option:selected').val(),
                "action": 'get_perd'
            },
            dataType: 'json',
            success: function (data) {
                produccion.add_perdida_materiales(data[0]);
                $('#id_material').val(null).trigger('change');
            },
            error: function (xhr, status, data) {
                menssaje_error('Error', data[0], 'fa fa-times', function () {

                });
            },

        })
    })
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
                url: '/material/lista',
                data: function (params) {
                    if (data_asig !== '') {
                        var queryParameters = {
                            term: params.term,
                            'action': 'search_perd',
                            "asig": data_asig,
                        };
                        return queryParameters;
                    } else {
                        menssaje_error('Error', 'Debe buscar un lote para poder ingresar perdidas de materiales', 'fa fa-times',
                            function () {

                            })
                    }
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca un Material',
            minimumInputLength: 1,
        });


    //cantidad de productos
    $('#tblinventario tbody')
        .on('click', 'a[rel="remove"]', function () {
        var tr = tblproductos.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar este producto de tu detalle?', function () {
                var p = produccion.items.productos[tr.row];
                produccion.items.productos.splice(tr.row, 1);
                menssaje_ok('Confirmacion!', 'Producto eliminado', 'far fa-smile-wink', function () {
                    produccion.list();
                });
            })
    })
        .on('change keyup', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = tblproductos.cell($(this).closest('td, li')).index();
            produccion.items.productos[tr.row].cantidad = cantidad;
        });


    $('#tblperdidas_productos tbody')
        .on('click', 'a[rel="remove"]', function () {
        var tr = tblperdidas_productos.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar este producto de tu detalle de perdidas?', function () {
                var p = produccion.items.perdidas_productos[tr.row];
                produccion.items.perdidas_productos.splice(tr.row, 1);
                menssaje_ok('Confirmacion!', 'Producto eliminado', 'far fa-smile-wink', function () {
                    produccion.list_perdidas_productos();
                });
            })
    })
        .on('change keyup', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = tblperdidas_productos.cell($(this).closest('td, li')).index();
            produccion.items.perdidas_productos[tr.row].cantidad = cantidad;
        });


    $('#tblperdidas_materiales tbody')
        .on('click', 'a[rel="remove"]', function () {
        var tr = tblperdidas_materiales.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar este material de tu detalle de perdidas?', function () {
                var p = produccion.items.perdidas_materiales[tr.row];
                produccion.items.perdidas_materiales.splice(tr.row, 1);
                menssaje_ok('Confirmacion!', 'Material eliminado', 'far fa-smile-wink', function () {
                    produccion.list_perdidas_materiales();
                });
            })
    })
        .on('change keyup', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = tblperdidas_materiales.cell($(this).closest('td, li')).index();
            produccion.items.perdidas_materiales[tr.row].cantidad = cantidad;
        });


    $('#btnRemoveall_inventario').on('click', function () {
        if (produccion.items.productos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los productos Ingresados?', function () {
                produccion.items.productos = [];
                menssaje_ok('Confirmacion!', 'Productos eliminados', 'far fa-smile-wink', function () {
                    produccion.list();
                });
            });
    });

    $('#btnRemoveall_perdidas_productos').on('click', function () {
        if (produccion.items.perdidas_productos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los productos Ingresados como perdidas?', function () {
                produccion.items.perdidas_productos = [];
                menssaje_ok('Confirmacion!', 'Productos eliminados', 'far fa-smile-wink', function () {
                    produccion.list_perdidas_productos();
                });
            });
    });

    $('#btnRemoveall_perdidas_materiales').on('click', function () {
        if (produccion.items.perdidas_materiales.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los materiales Ingresados como perdidas?', function () {
                produccion.items.perdidas_materiales = [];
                menssaje_ok('Confirmacion!', 'Materiales eliminados', 'far fa-smile-wink', function () {
                    produccion.list_perdidas_materiales();
                });
            });
    });

    $('#save').on('click', function () {
        if ($('#id_asignacion').val() === "") {
            menssaje_error('Error!', "Debe selecionar un lote", 'far fa-times-circle');
            return false
        } else if ($('#id_novedades').val()===""){
            $('#id_novedades').addClass('is-invalid');
        } else if ($('#id_novedades').val()!==""){
            $('#id_novedades').removeClass('is-invalid').addClass('is-valid');
        } else if (produccion.items.productos.length === 0 && produccion.items.perdidas_materiales.length === 0 && produccion.items.perdidas_productos.length === 0) {
            menssaje_error('Error!', "Debe ingresar al menos un producto y/o alguna perdida de material o producto", 'far fa-times-circle');
            return false
        }
        var parametros;
        produccion.items.fecha_ingreso = $('input[name="fecha_ingreso"]').val();
        produccion.items.novedades = $('textarea[name="novedades"]').val();
        produccion.items.asignacion = $('#id_asignacion').val();
        parametros = {'ingresos': JSON.stringify(produccion.items)};
        parametros['action'] = 'add';
        parametros['id'] = '';
        save_with_ajax('Alerta',
            window.location.pathname, 'Esta seguro que desea guardar estos ingresos de produccion?', parametros, function (response) {
                window.location.replace('/produccion/lista')
            });
    });

    $('#id_asignacion').select2({
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
            url: '/asignacion/lista',
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    'action': 'search'
                };
                return queryParameters;
            },
            processResults: function (data) {
                data_asig = data[0];
                return {
                    results: data
                };
            },
            add: function (data) {

                var newOption = new Option(data.id, data.text, false, true);
                $('#id_asignacion').append(newOption).trigger('change');
            },

        },
        placeholder: 'Busca un numero de lote',
        minimumInputLength: 1,
    });

});
