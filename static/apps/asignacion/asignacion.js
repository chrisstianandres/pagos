var tblcompra;
var compras = {
    items: {
        fecha_asig: '',
        lote: '',
        productos: [],
        maquinas: [],
    },
    add: function (data) {
        this.items.productos.push(data);
        this.items.productos = this.exclude_duplicados(this.items.productos);
        this.list();

    },
    list: function () {
        tblcompra = $("#tblinsumos").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            scrollX: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: this.items.productos,
            columns: [
                {data: 'id'},
                {data: "producto_base.nombre"},
                {data: "producto_base.categoria.nombre"},
                {data: "producto_base.presentacion.nombre"},
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
            rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.producto_base.stock,
                    step: 1
                });
            },
            createdRow: function (row, data, dataIndex) {
            if (data.producto_base.stock <= 5) {
                $('td', row).eq(4).html('<span class = "badge badge-danger" style="color: white ">'+ data.producto_base.stock+'</span>');
            } else if (data.data.producto_base.stock <= 10) {
                $('td', row).eq(4).html('<span class = "badge badge-warning" style="color: white ">'+ data.producto_base.stock+'</span>');
            } else if (data.data.producto_base.stock > 10) {
                $('td', row).eq(4).html('<span class = "badge badge-success" style="color: white ">'+ data.producto_base.stock+'</span>');
            }

        }
        });
    },

    add_machine: function (data) {
        this.items.maquinas.push(data);
        this.items.maquinas = this.exclude_duplicados_machine(this.items.maquinas);
        this.list_machine();

    },
    list_machine: function () {
        tblcompra = $("#tblmaquinas").DataTable({
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
    exclude_duplicados_machine: function (array) {
        this.items.maquinas = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;

    }

};
$(function () {
    //texto de los selects
    $('.select2').select2({
        "language": {
            "noResults": function () {
                return "Sin resultados";
            }
        },
        allowClear: true
    });
    //seleccionar producto del select producto
    $('#id_inventario_material').on('select2:select', function (e) {
        $.ajax({
            type: "POST",
            url: '/material/lista',
            data: {
                "id": $('#id_inventario_material option:selected').val(),
                "action": 'get_asig'
            },
            dataType: 'json',
            success: function (data) {
                compras.add(data[0]);
                $('#id_inventario_material option:selected').remove();
            },
            error: function (xhr, status, data) {
                menssaje_error('Error', data[0], 'fa fa-times', function () {

                });
            },

        })
    });
    //cantidad de productos
    $('#tblinsumos tbody').on('click', 'a[rel="remove"]', function () {
        var tr = tblcompra.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar este producto de tu detalle?', function () {
                var p = compras.items.productos[tr.row];
                compras.items.productos.splice(tr.row, 1);
                $('#id_material').append('<option value="' + p.id + '">' + p.nombre + '</option>');
                menssaje_ok('Confirmacion!', 'Material eliminado', 'far fa-smile-wink', function () {
                    compras.list();
                });
            })
    })
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

    $('#save').on('click', function () {
        if ($('input[name="lote"]').val() === "") {
            menssaje_error('Error!', "Debe ingresar un numero de lote", 'far fa-times-circle');
            return false
        } else if (compras.items.productos.length === 0 && compras.items.maquinas.length === 0) {
            menssaje_error('Error!', "Debe seleccionar al menos un material y/o una maquina", 'far fa-times-circle');
            return false
        }
        var parametros;
        compras.items.fecha_asig = $('input[name="fecha_asig"]').val();
        compras.items.lote = $('#id_lote').val();
        console.log(compras.items);
        parametros = {'asignaciones': JSON.stringify(compras.items)};
        parametros['action']='add';
        parametros['id']='';
        save_with_ajax('Alerta',
            window.location.pathname, 'Esta seguro que desea guardar esta asignacion?', parametros, function (response) {
                window.location.replace('/asignacion/lista')
            });
    });

    $('#id_inventario_material').select2({
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
    });
    $('#id_maquina').select2({
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
    });

     $('#id_maquina').on('select2:select', function (e) {
        $.ajax({
            type: "POST",
            url: '/maquina/lista',
            data: {
                "id": $('#id_maquina option:selected').val(),
                "action": 'get_asig'
            },
            dataType: 'json',
            success: function (data) {
                compras.add_machine(data[0]);
                $('#id_maquina option:selected').remove();
            },
            error: function (xhr, status, data) {
                menssaje_error('Error', data[0], 'fa fa-times', function () {

                });
            },

        })
    });

});

