var carrito = {
    items: {
        fecha_venta: '',
        cliente: '',
        subtotal: 0.00,
        total: 0.00,
        productos: [],
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
        this.items.productos = this.exclude_duplicados(this.items.productos);
        localStorage.setItem('carrito', JSON.stringify(this.items.productos));

        this.list();
    },
    list: function () {
        this.calculate();
        if (carrito.items.productos.length >= 1) {
            $('#paypal_btn').show();
        } else {
            $('#paypal_btn').hide();
        }
        var numero = this.items.productos.length;
        if (numero >= 1) {
            $('#count').html(numero);
        } else {
            $('#count').html('');
        }
        tblventa = $("#tblproductos").DataTable({

            autoWidth: false,
            dataSrc: "",
            responsive: true,
            dom:
                "<'row'<'col-sm-12'tr>>",
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: carrito.items.productos,
            columns: [
                {data: 'id'},
                {data: "producto_base.nombre"},
                {data: "producto_base.categoria.nombre"},
                {data: "color.nombre"},
                {data: "talla.talla_full"},
                {data: "stock"},
                {data: "cantidad_venta"},
                {data: "pvp"},
                {data: "subtotal"}
            ],
            destroy: true,
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    width: '5%',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-xs btn-flat rounded-pill" style="color: white" data-toggle="tooltip" title="Quitar Producto"><i class="fa fa-trash"></i></a>';
                        //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';

                    }
                },
                {
                    targets: [-2, -1],
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
                        return '<input type="text" name="cantidad" value="' + data + '">';

                    }
                }
            ], rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.stock,
                    step: 1,
                    buttondown_class: 'btn btn-primary btn-sm',
                    buttonup_class: 'btn btn-primary btn-sm',

                }).keypress(function (e) {
                    if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
                        return false;
                    }
                }).keyup(function (e) {
                    e.preventDefault();
                    if($(this).val()>data.stock){
                         menssaje_error('Error!', 'No puede elegir una cantidad mayor que el stock disponible', 'fas fa-exclamation-circle');
                    }

                });//Para solo numeros
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

    if (localStorage.getItem('carrito')) {
        carro_respaldo = JSON.parse(localStorage.getItem('carrito'));
        carrito.items.productos = carro_respaldo;
        carrito.list();
    } else {
        carrito.list();
    }


    $('#tblproductos tbody')
        .on('click', 'a[rel="remove"]', function () {
            localStorage.clear();
            var tr = tblventa.cell($(this).closest('td, li')).index();
            borrar_todo_alert('Alerta de Eliminación',
                'Esta seguro que desea eliminar este producto del carrito <br> ' +
                '<strong>CONTINUAR?</strong>', function () {
                    carrito.items.productos.splice(tr.row, 1);
                    localStorage.setItem('carrito', JSON.stringify(carrito.items.productos));
                    carrito.list();
                })
        })
        .on('change keyup', 'input[name="cantidad"]', function () {
            localStorage.clear();
            var cantidad = parseInt($(this).val());
            var tr = tblventa.cell($(this).closest('td, li')).index();
            carrito.items.productos[tr.row].cantidad_venta = cantidad;
            carrito.calculate();
            localStorage.setItem('carrito', JSON.stringify(carrito.items.productos));
            $('td:eq(8)', tblventa.row(tr.row).node()).html('$' + carrito.items.productos[tr.row].subtotal.toFixed(2));

        });

    paypal.Buttons({
        createOrder: function (data, actions) {
            // This function sets up the details of the transaction, including the amount and line item details.
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: $('#id_total').val()
                    }
                }]
            });
        },
        onApprove: function (data, actions) {
            // This function captures the funds from the transaction.
            return actions.order.capture().then(function (details) {
                // This function shows a transaction success message to your buyer.
                if (carrito.items.productos.length === 0) {
                    menssaje_error('Error!', "Debe seleccionar al menos un producto", 'far fa-times-circle');
                    return false
                }
                var parametros;
                carrito.items.fecha_venta = $('input[name="fecha_trans"]').val();
                carrito.items.cliente = $('#user_id').val();
                parametros = {'ventas': JSON.stringify(carrito.items)};
                parametros['action'] = 'add';
                parametros['id'] = '';
                $.ajax({
                    dataType: 'JSON',
                    type: 'POST',
                    url: '/venta/nuevo_online',
                    data: parametros,
                }).done(function (data) {
                    if (!data.hasOwnProperty('error')) {
                        callback(data);
                        return false;
                    }
                    menssaje_error('Error', data.error, 'fas fa-exclamation-circle');

                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert(textStatus + ': ' + errorThrown);
                });
            });
        }
    }).render('#paypal-button-container');
    //This function displays Smart Payment Buttons on your web page.


    $('#save').on('click', function () {
        if (carrito.items.productos.length === 0) {
            menssaje_error('Error!', "Debe seleccionar al menos un producto", 'far fa-times-circle');
            return false
        }
        var parametros;
        carrito.items.fecha_venta = $('input[name="fecha_trans"]').val();
        carrito.items.cliente = $('#user_id').val();
        parametros = {'ventas': JSON.stringify(carrito.items)};
        parametros['action'] = 'reserva';
        parametros['id'] = '';
        save_with_ajax('Alerta',
            '/venta/nuevo_online', 'Esta seguro que desea reservar esta venta?', parametros,
            function (response) {
                localStorage.clear();
                printpdf('Alerta!', '¿Desea generar el comprobante en PDF?', function () {
                    window.open('/venta/printpdf/' + response['id'], '_blank');
                    // location.href = '/venta/printpdf/' + response['id'];
                    location.href = '/venta/lista';
                }, function () {
                    location.href = '/venta/lista';
                })

            });
    });

    $('#id_inventario')
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
                        'action': 'search',
                        'ids': JSON.stringify(carrito.get_ids())
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
                    "id": $('#id_inventario option:selected').val(),
                    'action': 'get'
                },
                dataType: 'json',
                success: function (data) {
                    carrito.add(data);
                    $('#id_inventario').val(null).trigger('change');
                },
                error: function (xhr, status, data) {
                    alert(data);
                },

            })
        });


    //modal buscar
    $('#id_search_producto').on('click', function () {
        $('#Modal_lista').modal('show');
        tbl_prod = $("#tbl_prod").DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
            },
            ajax: {
                url: '/producto/lista',
                type: 'POST',
                data: {'action': 'list_venta', 'ids': JSON.stringify(carrito.get_ids())},
                dataSrc: ""
            },
            columns: [
                {"data": "producto_base.nombre"},
                {"data": "producto_base.categoria.nombre"},
                {"data": "color.nombre"},
                {"data": "talla.talla_full"},
                {"data": "stock"},
                {"data": "producto_base.descripcion"},
                {"data": "pvp"},
                {"data": "pvp_alq"},
                {"data": "imagen"},
                {"data": "id"}
            ],

            columnDefs: [
                {
                    targets: [-3, -4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span>$ ' + parseFloat(data).toFixed(2) + '</span>';
                    }
                },
                {
                    targets: '__all',
                    class: 'text-center'
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" width="30" height="30" class="img-circle elevation-2" alt="User Image">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    width: '10%',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a style="color: white" type="button" class="btn btn-success btn-xs" rel="check" ' +
                            'data-toggle="tooltip" title="Seleccionar producto"><i class="fa fa-check-circle"></i></a>' + ' '

                    }
                },
            ]

        });
    });
    //select producto de table
    $('#tbl_prod tbody').on('click', 'a[rel="check"]', function () {
        var tr = tbl_prod.cell($(this).closest('td, li')).index();
        var data = tbl_prod.row(tr.row).data();
        var parametros = {'id': data.id, 'action': 'get'};
        $.ajax({
            dataType: 'JSON',
            type: 'POST',
            url: '/producto/lista',
            data: parametros,
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                carrito.add(data);
                $('#Modal_lista').modal('hide');
                return false;
            }
            menssaje_error(data.error, data.content, 'fa fa-times-circle');
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        });
    });
});