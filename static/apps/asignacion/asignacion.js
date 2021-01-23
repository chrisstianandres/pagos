var tblcompra;
var tblmaquinas;
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
                    $('td', row).eq(4).html('<span class = "badge badge-danger" style="color: white ">' + data.producto_base.stock + '</span>');
                } else if (data.producto_base.stock <= 10) {
                    $('td', row).eq(4).html('<span class = "badge badge-warning" style="color: white ">' + data.producto_base.stock + '</span>');
                } else if (data.producto_base.stock > 10) {
                    $('td', row).eq(4).html('<span class = "badge badge-success" style="color: white ">' + data.producto_base.stock + '</span>');
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
    //cantidad de productos


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
        parametros['action'] = 'add';
        parametros['id'] = '';
        save_with_ajax('Alerta',
            window.location.pathname, 'Esta seguro que desea guardar esta asignacion?', parametros, function (response) {
                window.location.replace('/asignacion/lista')
            });
    });
});

