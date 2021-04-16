var tbl_mat_list, tbl_prod_list, tblnovedades, calendar = false;
var tblproductos;
var tblperdidas_materiales;
var data_asig = '';
var action, pk_nov, buscar_mat;
var produccion = {
    items: {
        materiales: [],
        maquinas: [],
        perdidas: [],
        productos: []
    },
    get_ids_maquina: function () {
        var ids = [];
        $.each(this.items.maquinas, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },

    get_ids_perdida: function () {
        var ids = [];
        $.each(this.items.perdidas, function (key, value) {
            ids.push(value.id_det);
        });
        return ids;
    },
    get_ids_material: function () {
        var ids = [];
        $.each(this.items.materiales, function (key, value) {
            ids.push(value.id)
        });
        return ids;
    },
    get_ids_estimado: function () {
        var ids = [];
        $.each(this.items.productos, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },

    list_novedades: function () {
        tblnovedades = $("#tblnovedades").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {'action': 'novedades'},
                dataSrc: ""
            },
            columns: [
                {data: "fecha"},
                {data: "novedad"},
                {data: "id"}
            ],
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        var edit = '<a rel="edit" type="button" class="btn btn-success btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Editar"><i class="fa fa-edit"></i></a>' + ' ';
                        var del = '<a rel="del" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                        return edit + del;
                        //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: '_all',
                    class: 'text-center'
                },
            ]
        });
    },

    add_perdida_materiales: function (data) {
        var item = [];
        item.push(data);
        $.each(item, function (key, value) {
            value['cantidad'] = 1;
        });
        this.items.perdidas.push(data);
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
            data: this.items.perdidas,
            columns: [
                {data: 'id'},
                {data: "producto_base.nombre"},
                {data: "producto_base.categoria.nombre"},
                {data: "calidad"},
                {data: "color.nombre"},
                {data: "tipo_material.nombre"},
                {data: "medida_full"},
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
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" ' +
                            'autocomplete="off" value="' + data + '">';

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
                    max: data.ingreso_actual + data.cantidad,
                    step: 1
                }).keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                });//Para solo numeros

            }
        });
    },

    add_material: function (data) {
        this.items.materiales.push(data);
        this.list_material();

    },
    list_material: function () {
        tblmateriales = $("#tblinsumos")
            .DataTable({
                destroy: true,
                autoWidth: false,
                dataSrc: "",
                scrollX: true,
                language: {
                    "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
                },
                data: this.items.materiales,
                columns: [
                    {data: 'id'},
                    {data: "producto_base.nombre"},
                    {data: "producto_base.categoria.nombre"},
                    {data: "calidad"},
                    {data: "color.nombre"},
                    {data: "tipo_material.nombre"},
                    {data: "medida_full"},
                    {data: "stock_actual"},
                    {data: "cant"}
                ],
                columnDefs: [
                    {
                        targets: [0],
                        orderable: false,
                        render: function (data, type, row) {
                            if (row.cant - row.ingreso_actual === 0) {
                                return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Insumo"><i class="fa fa-trash-alt"></i></a>';
                            } else {
                                return '';
                            }

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
                    var minimo;
                    if (data.cant - data.ingreso_actual <= 1) {
                        minimo = 5;
                    } else {
                        minimo = data.cant - data.ingreso_actual;
                    }
                    $(row).find('input[name="cantidad"]').TouchSpin({
                        min: minimo,
                        max: data.stock_actual,
                        step: 1
                    })
                        .keypress(function (e) {
                            if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                                return false;
                            }
                        });//Para solo numeros
                },
                createdRow: function (row, data, dataIndex) {
                    if (data.stock_actual <= 5) {
                        $('td', row).eq(7).html('<span class = "badge badge-danger" style="color: white ">' + data.stock_actual + '</span>');
                    } else if (data.stock_actual <= 10) {
                        $('td', row).eq(7).html('<span class = "badge badge-warning" style="color: white ">' + data.stock_actual + '</span>');
                    } else if (data.stock_actual > 10) {
                        $('td', row).eq(7).html('<span class = "badge badge-success" style="color: white ">' + data.stock_actual + '</span>');
                    }
                }
            });
    },

    add_machine: function (data) {
        this.items.maquinas.push(data);
        this.list_machine();

    },
    list_machine: function () {
        tblmaquinas = $("#tblmaquinas").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: this.items.maquinas,
            columns: [
                {data: 'id'},
                {data: "tipo.nombre"},
                {data: "tipo.descripcion"},
                {data: "serie"},
                {data: "estado"},
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
                        return '<span class="badge badge-success"> DISPONIBLE </span>';

                    }
                },
                {
                    targets: '_all',
                    class: 'text-center'
                },
            ]
        });
    },

    add_estimado: function (data) {
        this.items.productos.push(data[0]);
        this.list_estimado();

    },
    list_estimado: function () {
        tblproductos = $("#tblproductos").DataTable({
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
                {data: "color.nombre"},
                {data: "talla.talla_full"},
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
                    min: 5,
                    max: 200,
                    step: 1
                }).keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                });//Para solo numeros
            },
        });
    },


    chek_max: function (data, tr) {
        $.each(this.items.materiales, function (key, value) {
            if (value.id_det === data) {
                produccion.items.materiales[key].ingreso_actual = value.cant
            }

        });
        produccion.items.perdidas.splice(tr.row, 1);
        this.list_material();
    },

    chek_perd: function (e, data, tr) {
        $.each(this.items.materiales, function (key, value) {
            if (value.id_det === data) {
                produccion.items.materiales[key].ingreso_actual = value.cant - tr;
            }
        });
        tblmateriales.clear();
        tblmateriales.rows.add(produccion.items.materiales).draw();
    },

    chek_asig: function (data, tr, ub) {
        if(this.items.perdidas.length>0){
            $.each(this.items.perdidas, function (key, value) {
            if (value.id_det === data) {
                produccion.items.perdidas[key].ingreso_actual = tr - value.cantidad;
            }
        });
        } else {
            console.log(produccion.items.materiales[ub].ingreso_actual);
            produccion.items.materiales[ub].ingreso_actual = tr;
        }

        tblperdidas_materiales.clear();
        tblperdidas_materiales.rows.add(produccion.items.perdidas).draw();
    }
};
$(function () {
    var inicio = new Date($('#inicio').val());
    var fin = new Date($('#fin').val());
    cb(moment(inicio), moment(fin));
    $('#id_lote').prop('readonly', true);


    $('#id_asignacion')
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
                url: '/asignacion/lista',
                data: function (params) {
                    return {
                        term: params.term,
                        'action': 'search'
                    };
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


    $('.btnRemoveall').on('click', function () {
        if (compras.items.productos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todas las prendas seleccionados?', function () {
                compras.items.productos = [];
                menssaje_ok('Confirmacion!', 'Prendas eliminadas', 'far fa-smile-wink', function () {
                    compras.list();
                });
            });
    });


    $('#id_inventario_material')
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
                    return {
                        term: params.term,
                        'action': 'search_asig',
                        'ids': JSON.stringify(produccion.get_ids_material())
                    };
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca un material',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            $.ajax({
                type: "POST",
                url: '/material/lista',
                data: {
                    "id": $('#id_inventario_material option:selected').val(),
                    "action": 'get_asig'
                },
                dataType: 'json',
                success: function (data) {
                    produccion.add_material(data[0]);
                    $('#id_inventario_material option:selected').remove();
                },
                error: function (xhr, status, data) {
                    menssaje_error('Error', data[0], 'fa fa-times', function () {

                    });
                },

            })
        });
    $('#id_maquina')
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
                url: '/maquina/lista',
                data: function (params) {
                    return {
                        term: params.term,
                        'action': 'search_asig',
                        'ids': JSON.stringify(produccion.get_ids_maquina())
                    };
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca una maquina',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            $.ajax({
                type: "POST",
                url: '/maquina/lista',
                data: {
                    "id": $('#id_maquina option:selected').val(),
                    "action": 'get_asig'
                },
                dataType: 'json',
                success: function (data) {
                    produccion.add_machine(data[0]);
                    $('#id_maquina option:selected').remove();
                },
                error: function (xhr, status, data) {
                    menssaje_error('Error', data[0], 'fa fa-times', function () {

                    });
                },

            })
        });


    $('#tblinsumos tbody')
        .on('click', 'a[rel="remove"]', function () {
            if (produccion.items.materiales.length === 1) {
                menssaje_error('Imposible eliminar', 'No puedes eliminar todos los materiales de esta confeccion', 'fa fa-ban', function () {
                })
            } else {
                var tr = tblmateriales.cell($(this).closest('td, li')).index();
                borrar_todo_alert('Alerta de Eliminación',
                    'Esta seguro que desea eliminar este material de tu detalle?', function () {
                        var p = produccion.items.materiales[tr.row];
                        produccion.items.materiales.splice(tr.row, 1);
                        menssaje_ok('Confirmacion!', 'Material eliminado', 'far fa-smile-wink', function () {
                            produccion.list_material();
                        });
                    })
            }
        })
        .on('change keyup', 'input[name="cantidad"]', function (e) {
            var cantidad = parseInt($(this).val());
            var tr = tblmateriales.cell($(this).closest('td, li')).index();
            var data = tblmateriales.row(tr.row).data();
            produccion.items.materiales[tr.row].cant = cantidad;
            if (e.cancelable) {
                e.preventDefault();
            }
            produccion.chek_asig(data.id_det, cantidad, tr.row);

        });


    $('#tblmaquinas tbody')
        .on('click', 'a[rel="remove"]', function () {
            if (produccion.items.maquinas.length === 1) {
                menssaje_error('Imposible eliminar', 'No puedes eliminar todas los maquinas de esta confeccion', 'fa fa-ban', function () {
                })
            } else {
                var tr = tblmaquinas.cell($(this).closest('td, li')).index();
                borrar_todo_alert('Alerta de Eliminación',
                    'Esta seguro que desea eliminar esta maquina de la confeccion?', function () {
                        var data = tblmaquinas.row(tr.row).data();
                        $.ajax({
                            dataType: 'JSON',
                            type: 'POST',
                            url: window.location.pathname,
                            data: {'id': data.id, 'action': 'estado_maquina'},
                        }).done(function (data) {
                            if (!data.hasOwnProperty('error')) {
                                produccion.items.maquinas.splice(tr.row, 1);
                                return false;
                            }
                            menssaje_error(data.error, data.content, 'fa fa-times-circle');
                        }).fail(function (jqXHR, textStatus, errorThrown) {
                            alert(textStatus + ': ' + errorThrown);
                        });
                        menssaje_ok('Confirmacion!', 'Maquina eliminado', 'far fa-smile-wink', function () {
                            produccion.list_machine();
                        });
                    })
            }
        });


    $('#buscar_material_tabla').on('click', function () {
        $('#Modal_lista_material').modal('show');
        tbl_mat_list = $('#tbl_mat_search').DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            ajax: {
                url: '/material/lista',
                type: 'POST',
                data: {'action': 'search_asig_table', 'ids': JSON.stringify(produccion.get_ids_material())},
                dataSrc: ""
            },
            columns: [
                {data: "producto_base.nombre"},
                {data: "producto_base.categoria.nombre"},
                {data: "calidad"},
                {data: "color.nombre"},
                {data: "tipo_material.nombre"},
                {data: "medida_full"},
                {data: "stock_actual"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a type="button" rel="take" class="btn btn-success btn-xs" style="color: white"><i class="fas fa-arrow-circle-right"></i>';

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
                    max: data.stock_actual,
                    step: 1
                }).keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                });//Para solo numeros

            },
            createdRow: function (row, data, dataIndex) {
                if (data.stock_actual <= 5) {
                    $('td', row).eq(6).html('<span class = "badge badge-danger" style="color: white ">' + data.stock_actual + '</span>');
                } else if (data.stock_actual <= 10) {
                    $('td', row).eq(6).html('<span class = "badge badge-warning" style="color: white ">' + data.stock_actual + '</span>');
                } else if (data.stock_actual > 10) {
                    $('td', row).eq(6).html('<span class = "badge badge-success" style="color: white ">' + data.stock_actual + '</span>');
                }
            }
        });
    });

    $('#tbl_mat_search tbody')
        .on('click', 'a[rel="take"]', function () {
            var tr = tbl_mat_list.cell($(this).closest('td, li')).index();
            var data = tbl_mat_list.row(tr.row).data();
            data['cantidad'] = 1;
            produccion.add_material(data);
            $('#Modal_lista_material').modal('hide');
        });

    $('#buscar_maquina_tabla').on('click', function () {
        $('#Modal_lista_maquina').modal('show');
        tbl_maq_list = $('#tbl_maq_search').DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            ajax: {
                url: '/maquina/lista',
                type: 'POST',
                data: {'action': 'search_asig_table', 'ids': JSON.stringify(produccion.get_ids_maquina())},
                dataSrc: ""
            },
            columns: [
                {data: "tipo.nombre"},
                {data: "tipo.descripcion"},
                {data: "serie"},
                {data: "estado_full"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a type="button" rel="take" class="btn btn-success btn-xs" style="color: white"><i class="fas fa-arrow-circle-right"></i>';

                    }
                },
                {
                    targets: '_all',
                    class: 'text-center'
                },
            ],
            createdRow: function (row, data, dataIndex) {
                if (data.estado === 0) {
                    $('td', row).eq(3).html('<span class = "badge badge-success" style="color: white ">' + data.estado_full + '</span>');
                } else if (data.estado === 1) {
                    $('td', row).eq(3).html('<span class = "badge badge-danger" style="color: white ">' + data.estado_full + '</span>');
                } else if (data.estado === 2) {
                    $('td', row).eq(3).html('<span class = "badge badge-primary" style="color: white ">' + data.estado_full + '</span>');
                }
            }
        });
    });

    $('#tbl_maq_search tbody')
        .on('click', 'a[rel="take"]', function () {
            var tr = tbl_maq_list.cell($(this).closest('td, li')).index();
            var data = tbl_maq_list.row(tr.row).data();
            produccion.add_machine(data);
            $('#Modal_lista_maquina').modal('hide');
        });


    $('#tblnovedades tbody')
        .on('click', 'a[rel="edit"]', function () {
            action = 'edit_novedad';
            calendar = true;
            var fecha = new Date();
            var tr = tblnovedades.cell($(this).closest('td, li')).index();
            var data = tblnovedades.row(tr.row).data();
            pk_nov = data.id;
            $('#Modal_novedades').modal('show');
            $('#id_novedad').val(data.novedad);
            $('#id_fecha').val(data.fecha).daterangepicker({
                locale: {
                    format: 'YYYY-MM-DD',
                    applyLabel: '<i class="fa fa-check"></i> Selccionar',
                    cancelLabel: '<i class="fas fa-times"></i> Cancelar',
                },
                singleDatePicker: true,
                showDropdowns: true,
                minDate: new Date($('#inicio').val()),
                maxDate: fecha
            });
        })
        .on('click', 'a[rel="del"]', function () {
            action = 'del_novedad';
            var tr = tblnovedades.cell($(this).closest('td, li')).index();
            var data = tblnovedades.row(tr.row).data();
            pk_nov = data.id;
            var parametros = {'id': data.id, 'action': action};
            save_estado('Eliminando novedad', window.location.pathname,
                'Seguro que quiere eliminar esta novedad?', parametros, function () {
                    produccion.list_novedades();
                })
        });


    $('#btnRemoveall_novedades').on('click', function () {
        if (tblnovedades.rows().count() === 0) return false;
        action = 'del_novedad_all';
        var parametros = {'action': action};
        save_estado('Eliminar todas las  novedades', window.location.pathname,
            'Seguro que quiere eliminar todas las novedades?', parametros, function () {
                produccion.list_novedades();
            })
    });


    $('#btn_new_novedad')
        .on('click', function () {
            $('#Modal_novedades').modal('show');
            action = 'add_novedad';
            pk_nov = '';
            $('#id_novedad').text('');
            if (calendar) {
                $('#id_fecha').prop('readonly', true).data('daterangepicker').remove();
            } else {
                $('#id_fecha').prop('readonly', true);
            }

        });


    $('#form_novedades')
        .on('submit', function (e) {
            e.preventDefault();
            var isvalid = $(this).valid();
            var parametros = {
                'action': action, 'novedad': $('#id_novedad').val(), 'id': pk_nov,
                'fecha': $('#id_fecha').val()
            };
            if (isvalid) {
                save_with_ajax('Dsea realizar esta accion?', window.location.pathname,
                    'Esta Guardar esta novedad', parametros, function () {
                        $('#Modal_novedades').modal('hide');
                        reset_form('#form_novedades');
                        produccion.list_novedades();
                    })
            }
        });


    $("#form_novedades").validate({
        rules: {
            novedad: {
                required: true,
                minlength: 5,
                maxlength: 200
            }
        },
        messages: {
            novedad: {
                required: "Ingresa una novedad",
                minlength: "Debe ingresar al menos 5 letras",
                maxlength: "Debe ingresar hasta 200 letras",
            }
        }
    });
    $('#Modal_novedades').on('hidden.bs.modal', function (e) {
        reset_form('#form_novedades');
    });

    $('#btnadd_perdida')
        .on('click', function () {
            $('#Modal_perdida_material').modal('show');
            buscar_mat = $('#tbl_buscar_mat').DataTable({
                destroy: true,
                autoWidth: false,
                dataSrc: "",
                responsive: true,
                language: {
                    "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
                },
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {'action': 'get_det_asig', 'ids': JSON.stringify(produccion.get_ids_perdida())},
                    dataSrc: ""
                },
                columns: [
                    {data: "producto_base.nombre"},
                    {data: "producto_base.categoria.nombre"},
                    {data: "calidad"},
                    {data: "color.nombre"},
                    {data: "tipo_material.nombre"},
                    {data: "medida_full"},
                    {data: "maximo"},
                    {data: 'id'},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        orderable: false,
                        render: function () {
                            return '<a rel="take" type="button" class="btn btn-success btn-sm btn-flat" ' +
                                'style="color: white" data-toggle="tooltip" title="Elgir">' +
                                '<i class="fas fa-arrow-circle-right"></i></a>';
                        }
                    },
                    {
                        targets: '_all',
                        class: 'text-center'
                    },
                ]
            });
        });

    $('#tbl_buscar_mat tbody')
        .on('click', 'a[rel="take"]', function () {
            var tr = buscar_mat.cell($(this).closest('td, li')).index();
            var data = buscar_mat.row(tr.row).data();
            produccion.add_perdida_materiales(data);
            $('#Modal_perdida_material').modal('hide');
        });


    $('#btnRemoveall_perdidas')
        .on('click', function () {
            if (produccion.items.perdidas.length === 0) return false;
            var tr = tblperdidas_materiales.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar todas las perdidas de esta confeccion?', function () {
                    produccion.items.perdidas = [];
                    menssaje_ok('Confirmacion!', 'Perdidas Eliminadas eliminado', 'far fa-smile-wink', function () {
                        produccion.list_perdidas_materiales();
                    });
                })
        });


    $('#tblperdidas_materiales tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblperdidas_materiales.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar esta perdida?', function () {
                    var data = tblperdidas_materiales.row(tr.row).data();
                    produccion.chek_max(data.id_det, tr);
                    menssaje_ok('Confirmacion!', 'Perdida eliminada', 'far fa-smile-wink', function () {
                        produccion.list_perdidas_materiales();
                    });
                })

        })
        .on('change keyup', 'input[name="cantidad"]', function (e) {
            var cantidad = parseInt($(this).val());
            var tr = tblperdidas_materiales.cell($(this).closest('td, li')).index();
            produccion.items.perdidas[tr.row].cantidad = cantidad;
            var data = tblperdidas_materiales.row(tr.row).data();
            if (e.cancelable) {
                e.preventDefault();
            }
            produccion.chek_perd(e, data.id_det, cantidad);

        });


//    Productos


    $('#id_producto_estimado')
        .on('select2:select', function (e) {
            $.ajax({
                type: "POST",
                url: '/producto/lista',
                data: {
                    "id": $('#id_producto_estimado option:selected').val(),
                    "action": 'get_rep'
                },
                dataType: 'json',
                success: function (data) {
                    produccion.add_estimado(data);
                    $('#id_producto_estimado').val(null).trigger('change');
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
                    return {
                        term: params.term,
                        'action': 'search_rep',
                        'ids': JSON.stringify(produccion.get_ids_estimado())
                    };
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca una Prenda',
            minimumInputLength: 1,
        });


    $('#buscar_producto_tabla').on('click', function () {
        $('#Modal_lista_producto').modal('show');
        tbl_prod_list = $('#tbl_prod_search').DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            ajax: {
                url: '/producto/lista',
                type: 'POST',
                data: {'action': 'search_asig_table', 'ids': JSON.stringify(produccion.get_ids_estimado())},
                dataSrc: ""
            },
            columns: [
                {data: "producto_base.nombre"},
                {data: "producto_base.categoria.nombre"},
                {data: "color.nombre"},
                {data: "talla.talla_full"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a type="button" rel="take" class="btn btn-success btn-xs" style="color: white"><i class="fas fa-arrow-circle-right"></i>';

                    }
                },
                {
                    targets: '_all',
                    class: 'text-center'
                },
            ],
            createdRow: function (row, data, dataIndex) {
                if (data.estado === 0) {
                    $('td', row).eq(3).html('<span class = "badge badge-success" style="color: white ">' + data.estado_full + '</span>');
                } else if (data.estado === 1) {
                    $('td', row).eq(3).html('<span class = "badge badge-danger" style="color: white ">' + data.estado_full + '</span>');
                } else if (data.estado === 2) {
                    $('td', row).eq(3).html('<span class = "badge badge-primary" style="color: white ">' + data.estado_full + '</span>');
                }
            }
        });
    });

    $('#tbl_prod_search tbody')
        .on('click', 'a[rel="take"]', function () {
            var tr = tbl_prod_list.cell($(this).closest('td, li')).index();
            var data = tbl_prod_list.row(tr.row).data();
            data['cantidad'] = 5;
            var ex = [];
            ex.push(data);
            produccion.add_estimado(ex);
            $('#Modal_lista_producto').modal('hide');
        });


    $('#tblproductos tbody')
        .on('click', 'a[rel="remove"]', function () {
            if (produccion.items.productos.length === 1) {
                menssaje_error('Imposible eliminar', 'No puedes eliminar todos las prendas a confeccionar', 'fa fa-ban', function () {
                })
            } else {
                var tr = tblproductos.cell($(this).closest('td, li')).index();
                borrar_todo_alert('Alerta de Eliminación',
                    'Esta seguro que desea eliminar esta prenda de la produccion?', function () {
                        var p = produccion.items.productos[tr.row];
                        produccion.items.productos.splice(tr.row, 1);
                        menssaje_ok('Confirmacion!', 'Prenda eliminada', 'far fa-smile-wink', function () {
                            produccion.list_estimado();
                        });
                    })
            }
        })
        .on('change keyup', 'input[name="cantidad"]', function (e) {
            var cantidad = parseInt($(this).val());
            var tr = tblproductos.cell($(this).closest('td, li')).index();
            if (e.cancelable) {
                e.preventDefault();
            }
            produccion.items.productos[tr.row].cantidad = cantidad;
        });


    $('#save').on('click', function () {
        var parametros;
        parametros = {'ingresos': JSON.stringify(produccion.items)};
        console.log(produccion.items);
        parametros['action'] = 'add';
        save_with_ajax('Alerta',
            window.location.pathname, 'Esta seguro que desea guardar estos parametros de la confeccion?', parametros, function (response) {
                window.location.href='/asignacion/lista'
            });
    });

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

function cb(start, end) {
    $('#id_fecha_ingreso span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
}