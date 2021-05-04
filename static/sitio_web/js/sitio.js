var carrito = {
    items: {
        fecha_venta: '',
        subtotal: 0.00,
        total: 0.00,
        productos: [],
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
        var array = this.items.productos;
        if (array.length === 0) {
            array.push(data[0]);
            borrar_producto_carito('Trabajando!!', 'Agregando producto al carrito!', function () {
                menssaje_ok('Correcto!', 'Producto agregado al carrito!',
                    'fas fa-cart-plus', function () {
                    })
            })
        } else {
            var key = this.verify(array, data);

            if (key === 1) {
                borrar_producto_carito('Trabajando!!', 'Agregando producto al carrito!', function () {
                    menssaje_error('Atencion!', 'Este producto ya esta en tu carrito agrega mas cantidad desde este',
                        'fas fa-exclamation-circle', function () {
                        })
                })
            } else {
                array.push(data[0]);
                borrar_producto_carito('Trabajando!!', 'Agregando producto al carrito!', function () {
                    menssaje_ok('Correcto!', 'Producto agregado al carrito!',
                        'fas fa-cart-plus', function () {
                        })
                })
            }
        }
        this.items.productos = this.exclude_duplicados(this.items.productos);
        localStorage.setItem('carrito', JSON.stringify(this.items.productos));
        this.list();
    },
    list: function () {
        this.calculate();
        var numero = this.items.productos.length;
        if (numero >= 1) {
            $('#count').html(numero);
        } else {
            $('#count').html('');
        }

        tblventa = $("#datatable").DataTable({
            autoWidth: false,
            dataSrc: "",
            responsive: true,
            dom:
                "<'row'<'col-sm-12'tr>>",
            language: {
                // "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
                "emptyTable": "<strong>El carrito esta Vacio :´(</strong>"
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
                        return '<a rel="remove" type="button" class="btn btn-danger btn-xs btn-flat rounded-pill" style="color: white" data-toggle="tooltip" title="Quitar Producto"><i class="zmdi zmdi-delete"></i></a>';
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
                    if ($(this).val() > data.stock) {
                        menssaje_error('Error!', 'No puede elegir una cantidad mayor que el stock disponible', 'fas fa-exclamation-circle');
                    }

                }).on('change', function (e) {
                    if ($(this).val() === '') {
                        $(this).val(1);
                        localStorage.clear();
                        var cantidad = parseInt($(this).val());
                        var tr = tblventa.cell($(this).closest('td, li')).index();
                        carrito.items.productos[tr.row].cantidad_venta = cantidad;
                        carrito.calculate();
                        localStorage.setItem('carrito', JSON.stringify(carrito.items.productos));
                        $('td:eq(8)', tblventa.row(tr.row).node()).html('$' + carrito.items.productos[tr.row].subtotal.toFixed(2));
                    }

                })
            }
        });
    },
    exclude_duplicados: function (array) {
        this.items.productos = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;
    },
    verify: function (array, data) {
        ok = 0;
        $.each(array, function (key, value) {
                console.log(value.id);
                if (data[0].id === value.id) {
                    ok = 1;
                    return false;
                }
            }
        );
        return ok;
    }
};


function catalogo(tipo) {
    $.ajax({
        url: '/producto/sitio',
        type: 'POST',
        data: {'action': 'categoria', 'id': tipo},
        dataSrc: "",
    }).done(function (data) {
        console.log(data);
        var html = '<div class="columns is-centered is-multiline">' +
            '<div class="column is-full">' +
            '</div>';
        $.each(data, function (key, value) {
            html += '<div class="column is-half-tablet is-one-third-desktop column-half">' +
                '<div class="card">' +
                '<input type="hidden" class="set_venta" value="' + value['id'] + '">' +
                '<input type="hidden" class="set_alquiler" value="' + value['id'] + '">' +
                '<img src="' + value['imagen'] + '" alt="">' +
                '<div class="card-info">' +
                '<h4 class="has-text-black has-text-centered has-text-weight-bold"> ' + value['nombre_full'] + '</h4>' +
                '<p class="has-text-centered">' + value.producto_base['descripcion'] + '</p>' +
                '<p class="has-text-centered"> <strong>Precio de venta:</strong> $' + value['pvp'] + '</p>' +
                '<p class="has-text-centered"> <strong>Precio de Alquiler:</strong> $' + value['pvp_alq'] + '</p>' +
                '<p class="has-text-centered"> <strong>STOCK: </strong>' + value['stock'] + '</p>' +
                '<div class="card-buttons">' +
                '<button class="btn btn--mini-rounded" name="vender" value="' + value['id'] + '" data-toggle="tooltip" title="Añadir al carrito"><i class="zmdi zmdi-shopping-cart"></i></button>' +
                '<p>Los precios aqui mostrados no incluyen IVA</p>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>'
        });
        $('#masvendidos').html(html);
    });
}

$(function () {
    $('#categorias').select2({
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
    });
    var superuser = $('input[name="superuser"]').val();
    if (localStorage.getItem('carrito')) {
        carro_respaldo = JSON.parse(localStorage.getItem('carrito'));
        carrito.items.productos = carro_respaldo;
        carrito.list();
    } else {
        carrito.list();
    }

    $(document).on('click', 'button[name="vender"]', function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: '/producto/sitio',
            data: {
                "id": $(this).val(),
                'action': 'get'
            },
            dataType: 'json',
            success: function (data) {
                if (data[0].stock === 0) {
                    menssaje_error('Error', 'Lo sentimos este producto no tiene stok disponible', 'far fa-sad-tear', function () {
                    })
                } else {
                    carrito.add(data);
                }

            },
            error: function (xhr, status, data) {
                alert(data);
            },

        })
    });


    $(document).on('click', 'a[rel="btn_carrito"]', function (e) {
        e.preventDefault();
        $('#myModal').animate({
            height: "toggle"
        }, 1200).css("display", "block")

    });

    $(document).on('click', '#carrito_bajo', function (e) {
        e.preventDefault();
        $('html, body').animate({scrollTop: 0}, 1250);
        setTimeout(function () {
            // some point in future.
            $('#myModal').animate({
                height: "toggle"
            }, 100).css("display", "block")
        }, 1300);


    });

    $(document).on('click', 'a[rel="pay"]', function (e) {
        e.preventDefault();
        if (carrito.items.productos.length === 0) return false;
        localStorage.setItem('pagar', 1);
        if (superuser === 'USUARIO') {
            window.location.href = '/venta/nuevo'
        } else {
            window.location.href = '/venta/online'
        }
    });

    $(document).on('click', 'a[rel="clear_car"]', function (e) {
        if (carrito.items.productos.length === 0) return false;
        e.preventDefault();
        borrar_todo_alert('Atencion!', 'Esta seguro que desea vaciar el carrito?', function () {
            borrar_producto_carito('Trabajando!!', 'Vaciando carrito', function () {
                menssaje_ok('Correcto!', 'El carrito fue vaciado!',
                    'fas fa-shopping-cart', function () {
                        carrito.items.productos = [];
                        localStorage.clear();
                        carrito.list();
                    })
            })
        });
    });


    $(document).on('click', '#moreven-tab', function (e) {
        e.preventDefault();
        var categoria = $('#categorias');
        if ($(this).hasClass("active")) {
            catalogo(categoria.val());
            categoria.on('change', function () {
                catalogo(categoria.val());
            })
        }
    });

    $('.close').on('click', function () {
        $('#myModal').css("display", "none")
    });


    $('#datatable tbody')
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
});