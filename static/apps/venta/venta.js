var tblventa;
var tbl_prod;
var ventas = {
    items: {
        fecha_venta: '',
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
            console.log('estoy calculando');
            dict.subtotal = dict.cantidad_venta * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
            iva_emp = (dict.iva_emp / 100);
            console.log(dict);
        });
        this.items.subtotal = subtotal;
        console.log(subtotal);
        this.items.iva = this.items.subtotal * iva_emp;
        this.items.total = this.items.subtotal + this.items.iva;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="iva"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (data) {
        this.items.productos.push(data[0]);
        this.items.productos = this.exclude_duplicados(this.items.productos);
        this.list();
    },
    list: function () {
        console.log('estoy listando');
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
                {data: "stock"},
                {data: "cantidad_venta"},
                {data: "pvp"},
                {data: "subtotal"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    width: '5%',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-xs btn-flat rounded-pill" style="color: white" data-toggle="tooltip" title="Quitar Producto"><i class="fa fa-times"></i></a>';
                    }
                },
                {
                    targets: [-1, -2],
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
                }
            ], rowCallback: function (row, data) {
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.stock,
                    step: 1
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
        ventas.items.productos = carro_respaldo;
        console.log('estoy cargando el carrito del localstorge');
        ventas.list();
    } else {
        ventas.list();
    }
    var action = '';
    var pk = '';
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
            $('td:eq(8)', tblventa.row(tr.row).node()).html('$' + ventas.items.productos[tr.row].subtotal.toFixed(2));
        });
    //remover todos los productos del detalle
    $('.btnRemoveall').on('click', function () {
        if (ventas.items.productos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los productos seleccionados? <br>' +
            '<strong>CONTINUAR?</strong>', function () {
                ventas.items.productos = [];
                localStorage.clear();
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
        ventas.items.cliente = $('#id_user option:selected').val();
        parametros = {'ventas': JSON.stringify(ventas.items)};
        parametros['action'] = 'add';
        parametros['id'] = '';
        save_with_ajax('Alerta',
            '/venta/nuevo', 'Esta seguro que desea guardar esta venta?', parametros,
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
    //buscar produto del select producto
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
                    "id": $('#id_inventario option:selected').val(),
                    'action': 'get'
                },
                dataType: 'json',
                success: function (data) {
                    ventas.add(data);
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
                data: {'action': 'list_venta', 'ids': JSON.stringify(ventas.get_ids())},
                dataSrc: ""
            },
            columns: [
                {"data": "producto_base.nombre"},
                {"data": "producto_base.categoria.nombre"},
                {"data": "stock"},
                {"data": "producto_base.descripcion"},
                {"data": "pvp"},
                {"data": "pvp_alq"},
                {"data": "pvp_confec"},
                {"data": "imagen"},
                {"data": "id"}
            ],

            columnDefs: [
                {
                    targets: [-7],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span>' + data + '</span>';
                    }
                },
                {
                    targets: [-3, -4, -5],
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
                            'data-toggle="tooltip" title="Seleccionar prenda"><i class="fas fa-arrow-circle-right"></i></a>' + ' '

                    }
                },
            ],
            createdRow: function (row, data, dataIndex) {
                if (data.stock >= 51) {
                    $('td', row).eq(2).find('span').addClass('badge badge-success').attr("style", "color: white");
                } else if (data.stock >= 10) {
                    $('td', row).eq(2).find('span').addClass('badge badge-warning').attr("style", "color: white");
                } else if (data.stock <= 9) {
                    $('td', row).eq(2).find('span').addClass('badge badge-danger').attr("style", "color: white");
                }

            }

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
                ventas.add(data);
                $('#Modal_lista').modal('hide');
                return false;
            }
            menssaje_error(data.error, data.content, 'fa fa-times-circle');
        }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
        });
    });
});

