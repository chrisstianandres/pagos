var tblventa, tbl_prod_list;
var ventas = {
    items: {
        fecha_venta: '',
        inicio_produccion: '',
        fin_produccion: '',
        cliente: '',
        subtotal: 0.00,
        iva: 0.00,
        iva_emp: 0.00,
        total: 0.00,
        productos: []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.productos, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate: function () {
        var subtotal = 0.00;
        var iva_emp = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            console.log(dict);
            dict.subtotal = dict.cantidad_venta * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
            iva_emp = (dict.iva_emp / 100);
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva_emp;
        this.items.total = this.items.subtotal + this.items.iva;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="iva"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (data) {
        this.items.productos.push(data[0]);
        this.list();
    },
    list: function () {
        this.calculate();
        tblventa = $("#tblproductos").DataTable({
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
                {data: "cantidad_venta"},
                {data: "pvp"},
                {data: "subtotal"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-xs btn-flat rounded-pill" style="color: white" data-toggle="tooltip" title="Quitar Producto"><i class="fa fa-times"></i></a>';
                        //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';

                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';

                    }
                },
            ],
            rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]')
                    .keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                })
                    .TouchSpin({
                    min: 1,
                    max: 100,
                    step: 1
                });
            }
        });
    },
    exclude_duplicados: function (array) {
        this.items.productos = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;

    }
};
$(function () {
    $('.sidebar-mini').addClass('sidebar-collapse');
    var action = '';
    var pk = '';
    //seleccionar producto del select producto
    $('#id_producto')
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
                        'id': '',
                        'ids': JSON.stringify(ventas.get_ids())
                    };
                },
                processResults: function (data) {
                    return {
                        results: data
                    };

                },

            },
            placeholder: 'Busca un Producto',
            minimumInputLength: 1,
        })
        .on('select2:select', function (e) {
            $.ajax({
                type: "POST",
                url: '/producto/lista',
                data: {
                    "id": $('#id_producto option:selected').val(),
                    'action': 'get'
                },
                dataType: 'json',
                success: function (data) {
                    ventas.add(data);
                    $('#id_producto').val(null).trigger('change');
                },
                error: function (xhr, status, data) {
                    alert(data);
                },

            })
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
                data: {'action': 'search_asig_table', 'ids': JSON.stringify(ventas.get_ids())},
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
            var ex = [];
            ex.push(data);
            ventas.add(ex);
            $('#Modal_lista_producto').modal('hide');
        });
    //remover producto del detalle
    $('#tblproductos tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblventa.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar este producto de tu detalle <br> ' +
                '<strong>CONTINUAR?</strong>', function () {
                    ventas.items.productos.splice(tr.row, 1);
                    ventas.list();
                })
        })
        .on('change keyup', 'input[name="cantidad"]', function () {
            var cantidad = parseInt($(this).val());
            var tr = tblventa.cell($(this).closest('td, li')).index();
            ventas.items.productos[tr.row].cantidad_venta = cantidad;
            ventas.calculate();
            $('td:eq(7)', tblventa.row(tr.row).node()).html('$' + ventas.items.productos[tr.row].subtotal.toFixed(2));
        });
    //remover todos los productos del detalle
    $('.btnRemoveall').on('click', function () {
        if (ventas.items.productos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los productos seleccionados? <br>' +
            '<strong>CONTINUAR?</strong>', function () {
                ventas.items.productos = [];
                ventas.list();
            });
    });
    //boton guardar
    $('#save').on('click', function () {
        if ($('select[name="user"]').val() === "") {
            menssaje_error('Error!', "Debe seleccionar un cliente", 'far fa-times-circle');
            return false
        } else if (ventas.items.productos.length === 0) {
            menssaje_error('Error!', "Debe seleccionar al menos un producto", 'far fa-times-circle');
            return false
        }
        var parametros;
        ventas.items.fecha_venta = $('input[name="fecha_trans"]').val();
        ventas.items.inicio_produccion = $('#id_fecha_ingreso').data('daterangepicker').startDate.format('YYYY-MM-DD');
        ventas.items.fin_produccion = $('#id_fecha_ingreso').data('daterangepicker').endDate.format('YYYY-MM-DD');
        ventas.items.cliente = $('#id_user option:selected').val();

        parametros = {'confeccion': JSON.stringify(ventas.items)};
        parametros['action'] = 'add';
        parametros['id'] = '';
        save_with_ajax('Alerta',
            '/confeccion/nuevo', 'Esta seguro que desea guardar esta confeccion?', parametros, function (response) {
                printpdf('Alerta!', '¿Desea generar el comprobante en PDF?', function () {
                    window.open('/confeccion/printpdf/' + response['id'], '_blank');
                    // location.href = '/venta/printpdf/' + response['id'];
                    location.href = '/confeccion/lista';
                }, function () {
                    location.href = '/confeccion/lista';
                })

            });

    });
    //boton agregar cliente
    $('#id_new_client').on('click', function () {
        $('#Modal').modal('show');
    });
    //enviar formulario de nuevo cliente
    $('#form').on('submit', function (e) {
        e.preventDefault();
        action = 'add_cliente';
        var parametros = new FormData(this);
        parametros.append('action', action);
        parametros.append('id', pk);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                window.location.pathname, 'Esta seguro que desea guardar este cliente?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este cliente!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        var newOption = new Option(response.cliente['full_name'], response.cliente['id'], false, true);
                        $('#id_user').append(newOption).trigger('change');
                    });
                });
        }

    });
    //buscar cliente en el select cliente
    $('#id_user').select2({
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
            url: '/cliente/lista',
            data: function (params) {
                return {
                    term: params.term,
                    'action': 'search'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };

            },

        },
        placeholder: 'Busca un cliente',
        minimumInputLength: 1,
    });
    //mostrar el modal con el formulario cliente
    $('#Modal').on('hidden.bs.modal', function (e) {
        reset();
        $('#form').trigger("reset");
    });


    var start = moment();
    var end = moment();


    $('#id_fecha_ingreso').daterangepicker({
        startDate: start,
        endDate: end,
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-search"></i> Selccionar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
            customRangeLabel: "Fecha personalizada",
        },
        minDate: moment(),
        ranges: {
            'Hoy': [moment(), moment()],
            '7 Dias': [moment(), moment().add(6, 'days')],
            '30 Dias': [moment(), moment().add(30, 'days')],
            '90 Dias': [moment(), moment().add(90, 'days')],
            '180 Dias': [moment(), moment().add(180, 'days')]
        }
    }, cb);


    cb(start, end);

});

function cb(start, end) {
    $('#id_fecha_ingreso span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
}

