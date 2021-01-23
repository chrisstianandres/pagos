var tblproductos_estimado;
var tblproductos;
var tblperdidas_productos;
var tblperdidas_materiales;
var data_asig = '';
var produccion = {
    items: {
        fecha_ingreso: '',
        asignacion: '',
        novedades: '',
        productos_estimados: [],
        productos: [],
        materiales: [],
        maquinas: [],
        perdidas_productos: [],
        perdidas_materiales: [],
    },
    add_estimado: function (data) {
        this.items.productos_estimados.push(data[0]);
        this.items.productos_estimados = this.exclude_duplicados(this.items.productos_estimados);
        this.list_estimado();

    },
    list_estimado: function () {
        tblproductos_estimado = $("#tblproductos_estimado").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: this.items.productos_estimados,
            columns: [
                {data: 'id'},
                {data: "producto_base.nombre"},
                {data: "producto_base.categoria.nombre"},
                {data: "presentacion.nombre"},
                {data: "producto_base.color.nombre"},
                {data: "cantidad"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    orderable: false,
                    render: function (data, type, row) {
                        console.log(row);
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
    add_producto: function (data) {
        this.items.productos.push(data[0]);
        this.items.productos = this.exclude_duplicados(this.items.productos);
        this.list_estimado();

    },
    list_productos: function () {
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
                {data: "presentacion.nombre"},
                {data: "producto_base.color.nombre"},
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
        this.items.perdidas_productos.push(data);
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
                {data: "presentacion.nombre"},
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
                    max: data.max,
                    step: 1
                });
            },
        });
    },

    add_material: function (data) {
        this.items.materiales.push(data);
        this.items.materiales = this.exclude_duplicados_materiales(this.items.materiales);
        this.list_material();

    },
    list_material: function () {
        tblmateriales = $("#tblinsumos").DataTable({
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
                {data: "producto_base.color.nombre"},
                {data: "tipo_material.nombre"},
                {data: "medida"},
                {data: "ud_medida"},
                {data: "producto_base.stock"},
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
            // rowCallback: function (row, data) {
            //     $(row).find('input[name="cantidad"]').TouchSpin({
            //         min: 1,
            //         max: data.producto_base.stock,
            //         step: 1
            //     });
            // },
            // createdRow: function (row, data, dataIndex) {
            //     if (data.producto_base.stock <= 5) {
            //         $('td', row).eq(8).html('<span class = "badge badge-danger" style="color: white ">' + data.producto_base.stock + '</span>');
            //     } else if (data.producto_base.stock <= 10) {
            //         $('td', row).eq(8).html('<span class = "badge badge-warning" style="color: white ">' + data.producto_base.stock + '</span>');
            //     } else if (data.producto_base.stock > 10) {
            //         $('td', row).eq(8).html('<span class = "badge badge-success" style="color: white ">' + data.producto_base.stock + '</span>');
            //     }
            // }
        });
    },

    add_machine: function (data) {
        this.items.maquinas.push(data);
        this.items.maquinas = this.exclude_duplicados_machine(this.items.maquinas);
        this.list_machine();

    },
    list_machine: function () {
        tblmaquinas = $("#tblmaquinas").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            scrollX: true,
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
    },

    exclude_duplicados_materiales: function (array) {
        this.items.productos = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;

    },
    exclude_duplicados_machine: function (array) {
        this.items.maquinas = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;

    }

};
var action;
$(function () {
    action = $('#action').val();

    if (action === 'finalizar') {

        $('#ingreso_productos').show();
        $('#ingreso_materiales').hide();
        $('#id_lote').prop('readonly', true);
        $('#id_novedades').prop('readonly', true);

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
                var estimada = parseInt(produccion.items.productos[tr.row].cantidad_estimada);
                produccion.items.productos[tr.row].cantidad = cantidad;
                if (estimada >= cantidad) {
                    var perdida = parseInt(estimada - parseInt(produccion.items.productos[tr.row].cantidad));
                    var nuevo = produccion.items.productos[tr.row];
                    nuevo['cantidad'] = perdida;
                    if (perdida === 1) {
                        produccion.add_perdida_producto(nuevo);
                    } else if (perdida === 0){
                        alert(15);
                         produccion.items.perdidas_productos.splice(tr.row, 1);
                    }
                    else {
                        produccion.items.perdidas_productos[tr.row].cantidad = perdida;
                    }
                     produccion.list_perdidas_productos();
                }


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


        $('#id_producto_produccion')
            .on('select2:select', function (e) {
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

        $('#save').on('click', function () {
            if (produccion.items.productos.length === 0) {
                menssaje_error('Error!', "Debe Ingresar los productos resultantes de la prdoduccion", 'far fa-times-circle');
                return false
            }
            var parametros;
            parametros = {'ingresos': JSON.stringify(produccion.items)};
            parametros['action'] = 'finalizar';
            save_with_ajax('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar estos ingresos de produccion?', parametros, function (response) {
                    window.location.href = '/produccion/lista'
                });
        });
    } else {
        $('#save').on('click', function () {
            if ($('#id_lote').val() === "") {
                menssaje_error('Error!', "Debe Ingresar un lote", 'far fa-times-circle');
                return false
            } else if ($('#id_novedades').val() === "") {
                $('#id_novedades').addClass('is-invalid');
            } else if ($('#id_novedades').val() !== "") {
                $('#id_novedades').removeClass('is-invalid').addClass('is-valid');
            } else if (produccion.items.materiales.length === 0) {
                menssaje_error('Error!', "Debe ingresar al menos un material", 'far fa-times-circle');
                return false
            } else if (produccion.items.maquinas.length === 0) {
                menssaje_error('Error!', "Debe ingresar al menos una maquina ", 'far fa-times-circle');
                return false
            } else if (produccion.items.productos_estimados.length === 0) {
                menssaje_error('Error!', "Debe ingresar al menos un producto a producir", 'far fa-times-circle');
                return false
            }
            var parametros;
            produccion.items.fecha_ingreso = $('input[name="fecha_ingreso"]').val();
            produccion.items.lote = $('input[name="lote"]').val();
            produccion.items.novedades = $('textarea[name="novedades"]').val();
            parametros = {'ingresos': JSON.stringify(produccion.items)};
            parametros['action'] = 'add';
            parametros['id'] = '';
            save_with_ajax('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar estos ingresos de produccion?', parametros, function (response) {
                    window.location.replace('/produccion/lista')
                });
        });

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

        $('#id_material')
            .on('select2:select', function (e) {
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

        $('#tblinsumos tbody')
            .on('click', 'a[rel="remove"]', function () {
                var tr = tblmateriales.cell($(this).closest('td, li')).index();
                borrar_todo_alert('Alerta de Eliminación',
                    'Esta seguro que desea eliminar este material de tu detalle?', function () {
                        var p = produccion.items.materiales[tr.row];
                        produccion.items.materiales.splice(tr.row, 1);
                        menssaje_ok('Confirmacion!', 'Material eliminado', 'far fa-smile-wink', function () {
                            produccion.list_material();
                        });
                    })
            })
            .on('change keyup', 'input[name="cantidad"]', function () {
                var cantidad = parseInt($(this).val());
                var tr = tblmateriales.cell($(this).closest('td, li')).index();
                produccion.items.materiales[tr.row].cantidad = cantidad;
            });

           $('#tblproductos_estimado tbody')
            .on('click', 'a[rel="remove"]', function () {
                var tr = tblproductos_estimado.cell($(this).closest('td, li')).index();
                borrar_todo_alert('Alerta de Eliminación',
                    'Esta seguro que desea eliminar este producto de tu detalle?', function () {
                        var p = produccion.items.productos_estimados[tr.row];
                        produccion.items.productos_estimados.splice(tr.row, 1);
                        menssaje_ok('Confirmacion!', 'Producto eliminado', 'far fa-smile-wink', function () {
                            produccion.list_estimado();
                        });
                    })
            })
            .on('change keyup', 'input[name="cantidad"]', function () {
                var cantidad = parseInt($(this).val());
                var tr = tblproductos_estimado.cell($(this).closest('td, li')).index();
                produccion.items.productos_estimados[tr.row].cantidad = cantidad;
            });

    }
    //seleccionar producto del select producto


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


    $('.btnRemoveall').on('click', function () {
        if (compras.items.productos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los productos seleccionados?', function () {
                compras.items.productos = [];
                menssaje_ok('Confirmacion!', 'Productos eliminados', 'far fa-smile-wink', function () {
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
                    var queryParameters = {
                        term: params.term,
                        'action': 'search_asig'
                    };
                    return queryParameters;
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
                    var queryParameters = {
                        term: params.term,
                        'action': 'search_asig'
                    };
                    return queryParameters;
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

});

