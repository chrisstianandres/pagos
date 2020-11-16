var tblventa;
var tblservicios;
var ventas = {
    items: {
        fecha_venta: '',
        cliente: '',
        subtotal: 0.00,
        iva: 0.00,
        iva_emp: 0.00,
        total: 0.00,
        productos: [],
        servicios: [],
    },
    calculate: function () {
        var subtotal = 0.00;
        var iva_emp = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
            iva_emp = dict.iva_emp;
        });
        $.each(this.items.servicios, function (pos, dict) {
            dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
            iva_emp = dict.iva_emp;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva_emp;
        this.items.total = this.items.subtotal + this.items.iva;
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="iva"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (data) {
        this.items.productos.push(data);
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
                {data: "producto.nombre"},
                {data: "producto.categoria.nombre"},
                {data: "producto.presentacion.nombre"},
                {data: "serie"},
                {data: "pvp"},
                {data: "subtotal"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Producto"><i class="fa fa-trash-alt"></i></a>';
                        //return '<a rel="remove" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';

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
                // {
                //     targets: [-3],
                //     class: 'text-center',
                //     orderable: false,
                //     render: function (data, type, row) {
                //         return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';
                //
                //     }
                // }
            ]
        });
    },
    addserv: function (data) {
        this.items.servicios.push(data);
        this.listserv();
    },
    listserv: function () {
        this.calculate();
        tblservicios = $("#tblservicios").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: this.items.servicios,
            columns: [
                {data: 'id'},
                {data: "nombre"},
                {data: "cantidad"},
                {data: "pvp"},
                {data: "subtotal"}
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-sm btn-flat" style="color: white" data-toggle="tooltip" title="Eliminar Servicio"><i class="fa fa-trash-alt"></i></a>';
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
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="pvp" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';

                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + data + '">';

                    }
                }],
            rowCallback: function (row, data,) {
                if (data.idp > 0) {
                    $(row).find('input[name="cantidad"]').TouchSpin({
                        min: 1,
                        max: 100000,
                        step: 1
                    }).attr('disabled', 'disabled');
                }
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 100000,
                    step: 1
                });
                $(row).find('input[name="pvp"]').TouchSpin({
                    min: 1.00,
                    max: 1000000,
                    step: 0.01,
                    decimals: 2,
                    forcestepdivisibility: 'none',
                    boostat: 5,
                    maxboostedstep: 10,
                    prefix: '$'
                });
            }
        });
    },

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
    $('#id_producto').on('select2:select', function (e) {
        var crud = $('input[name="crud"]').val();
        $.ajax({
            type: "POST",
            url: crud,
            data: {
                "id": $('#id_producto option:selected').val(),
            },
            dataType: 'json',
            success: function (data) {
                ventas.add(data['0']);
                $('#id_producto').val(null).trigger('change');
                if (data[0]['producto'].instalacion === 1) {
                    printpdf('Confirmacion!', 'El producto que acaba de agregar requiere instalacion <br> ¿Desear agregar ese servicio a la venta?',
                        function () {
                            aggservicio(1, data[0]['id']);
                            menssaje_ok('Exito!', 'Servicio agregado a la venta <br> ' +
                                'Porfavor revisa el detalle de servicios', 'fas fa-tags', function () {
                            })
                        },
                        function () {
                        });
                }
            },
            error: function (xhr, status, data) {
                alert(data['0']);
            },

        })
    });
    //seleccionar servicio del select servicio
    $('#id_servicio').on('select2:select', function (e) {
        aggservicio($('#id_servicio option:selected').val(), 0);
    });
    //remover producto del detalle
    $('#tblproductos tbody').on('click', 'a[rel="remove"]', function () {
        var tr = tblventa.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar este producto de tu detalle <br> ' +
            'Recuerda que si seleccionaste la instalacion de este producto tambien se eliminará <br>' +
            '<strong>CONTINUAR?</strong>', function () {
                var p = ventas.items.productos[tr.row];
                checkserv(ventas.items.servicios, p);
                ventas.items.productos.splice(tr.row, 1);
                var productos = {'productos': JSON.stringify(ventas.items.productos)};
                productos['id'] = p.id;
                productos['key'] = 0;
                $.ajax({
                    url: '/inventario/remove_select',
                    type: 'POST',
                    data: productos,
                    success: function () {
                        menssaje_ok('Confirmacion!', 'Producto eliminado y servicio', 'far fa-smile-wink', function () {
                            ventas.list();
                            ventas.listserv();
                        });
                    }
                });
            })
    });
    //remover todos los productos del detalle
    $('.btnRemoveall').on('click', function () {
        if (ventas.items.productos.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los productos seleccionados? <br>' +
            'Recuerda que si seleccionaste las instalaciones de estos productos tambien se eliminarán <br>' +
            '<strong>CONTINUAR?</strong>', function () {
                var productos = {'productos': JSON.stringify(ventas.items.productos)};
                productos['id'] = 0;
                productos['key'] = 1;
                $.ajax({
                    url: '/inventario/remove_select',
                    type: 'POST',
                    data: productos,
                    success: function () {
                        menssaje_ok('Confirmacion!', 'Productos y servicios eliminados', 'far fa-smile-wink', function () {
                            checkserv(ventas.items.servicios, ventas.items.productos);
                            ventas.items.productos = [];
                            ventas.listserv();
                            ventas.list();
                        });
                    }
                });
            });
    });
    $('.btnRemoveallserv').on('click', function () {
        if (ventas.items.servicios.length === 0) return false;
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar todos los servicios seleccionados? <br>' +
            '<strong>CONTINUAR?</strong>', function () {
                menssaje_ok('Confirmacion!', 'Productos y servicios eliminados', 'far fa-smile-wink', function () {
                    ventas.items.servicios = [];
                    ventas.listserv();
                });
            });
    });
    //remover servicio del detalle
    $('#tblservicios tbody').on('click', 'a[rel="remove"]', function () {
        var tr = tblservicios.cell($(this).closest('td, li')).index();
        borrar_todo_alert('Alerta de Eliminación',
            'Esta seguro que desea eliminar este servicio de tu detalle?', function () {
                var p = ventas.items.servicios[tr.row];
                ventas.items.servicios.splice(tr.row, 1);
                $('#id_servicio').append('<option value="' + p.id + '">' + p.nombre + '</option>');
                // $('#id_producto').selectpicker('refresh');

                menssaje_ok('Confirmacion!', 'Servicio eliminado', 'far fa-smile-wink', function () {
                    ventas.listserv();
                });
            })
    }).on('change keyup', 'input[name="pvp"]', function () {
        var pvp = parseInt($(this).val());
        var tr = tblservicios.cell($(this).closest('td, li')).index();
        ventas.items.servicios[tr.row].pvp = pvp;
        ventas.calculate();
        $('td:eq(4)', tblservicios.row(tr.row).node()).html('$' + ventas.items.servicios[tr.row].subtotal.toFixed(2));
    }).on('change keyup', 'input[name="cantidad"]', function () {
        var cantidad = parseInt($(this).val());
        var tr = tblservicios.cell($(this).closest('td, li')).index();
        ventas.items.servicios[tr.row].cantidad = cantidad;
        ventas.calculate();
        $('td:eq(4)', tblservicios.row(tr.row).node()).html('$' + ventas.items.servicios[tr.row].subtotal.toFixed(2));
    });
    //boton guardar
    $('#save').on('click', function () {
        if ($('select[name="cliente"]').val() === "") {
            menssaje_error('Error!', "Debe seleccionar un cliente", 'far fa-times-circle');
            return false
        } else if (ventas.items.productos.length === 0 && ventas.items.servicios.length === 0) {
            menssaje_error('Error!', "Debe seleccionar al menos un producto o servicio", 'far fa-times-circle');
            return false
        }
        var action = $('input[name="action"]').val();
        var key = $('input[name="key"]').val();
        var parametros;
        ventas.items.fecha_venta = $('input[name="fecha_venta"]').val();
        ventas.items.cliente = $('#id_cliente option:selected').val();

        parametros = {'ventas': JSON.stringify(ventas.items)};
        save_with_ajax('Alerta',
            '/venta/crear', 'Esta seguro que desea guardar esta venta?', parametros, function (response) {
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
        var parametros = new FormData(this);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/cliente/crearcli', 'Esta seguro que desea guardar este cliente?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este cliente!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        var newOption = new Option(response.cliente['full_name'], response.cliente['id'], false, true);
                        $('#id_cliente').append(newOption).trigger('change');
                    });
                });
        }

    });
    //buscar cliente en el select cliente
    $('#id_cliente').select2({
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
            url: '/cliente/data',
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                };
                return queryParameters;
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
    $('#id_producto').select2({
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
            url: '/inventario/data_select',
            data: function (params) {
                var queryParameters = {
                    term: params.term,
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
});


function aggservicio(id, idp) {
    var crudserv = $('input[name="crudserv"]').val();
    $.ajax({
        type: "POST",
        url: crudserv,
        data: {
            "id": id,
        },
        dataType: 'json',
        success: function (data) {
            data[0]['idp'] = idp;
            ventas.addserv(data[0]);
            $('#id_servicio').val(null).trigger('change');
        },
        error: function (xhr, status, data) {
            alert(data['0']);
        },

    })
}

function checkserv(ser, p) {
    if (ser.length !== 0) {
        for (var srv in ser) {
            ser.forEach(function (car, index, object) {
                if (car.idp === p.id) {
                    object.splice(index, 1);
                }
            });
        }
    }
    if (p.length > 0) {
        for (var pr in p) {
            ser.forEach(function (car, index, object) {
                if (car.idp === p[pr].id) {
                    object.splice(index, 1);
                }
            });
        }
    }
}

function cancel() {
    var productos = {'productos': JSON.stringify(ventas.items.productos)};
    productos['id'] = 0;
    productos['key'] = 1;
    $.ajax({
        url: '/inventario/remove_select',
        type: 'POST',
        data: productos,
        success: function () {
            checkserv(ventas.items.servicios, ventas.items.productos);
            window.history.back();
        }
    });

}

//
//const fruits = ["apple", "banana", "cantaloupe", "blueberries", "grapefruit"];
//
// const index = fruits.findIndex(fruit => fruit === "blueberries");
//
// console.log(index); // 3
// console.log(fruits[index]); // blueberries

