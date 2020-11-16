var tblinventario;
var inventario = {
    items: {
        prod: [],
    },
    // calculate: function () {
    //     var subtotal = 0.00;
    //     var iva_emp = 0.00;
    //     $.each(this.items.productos, function (pos, dict) {
    //         dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
    //         subtotal += dict.subtotal;
    //         iva_emp = dict.iva_emp;
    //     });
    //     this.items.subtotal = subtotal;
    //     this.items.iva = this.items.subtotal * iva_emp;
    //     this.items.total = this.items.subtotal + this.items.iva;
    //     $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
    //     $('input[name="iva"]').val(this.items.iva.toFixed(2));
    //     $('input[name="total"]').val(this.items.total.toFixed(2));
    // },
    add: function (data) {
        this.items.prod.push(data);
        this.list();
    },
    list: function () {
        // this.calculate();
        tblinventario = $("#datatable").DataTable({
            destroy: true,
            autoWidth: false,
            dataSrc: "",
            scrollX: true,
            language: {
                "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
            data: this.items.prod,
            columns: [
                {data: "producto.nombre"},
                {data: "fecha_compra"},
                {data: "fecha_venta"},
                {data: "serie"}
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="serie" class="form-control form-control-sm input-sm serie" ' +
                            'autocomplete="off" maxlength="50" placeholder="Ingrese Maximo 50 Caracteres" ' +
                            'onkeyup="this.value=this.value.toUpperCase();">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var msg = 'Aun no vendido';
                        return '<span>' + msg + '</span>';
                    }
                },
                {
                    targets: [-3, -2, -1],
                    class: 'text-center'
                }
            ],
            createdRow: function (row, data, dataIndex) {
                if (data['fecha_salida'] === "") {
                    $('td', row).eq(2).find('span').addClass('badge bg-success');
                }
            }
        });
    }
};
$(function () {
    menssaje_ok('Ingreso de Inventario', 'Debe ingresar los productos comprados al inventario', 'fas fa-cart-plus', function () {
    });

    $('#datatable tbody').on('keyup', 'input[name="serie"]', function () {
        var serie = $(this).val();
        var tr = tblinventario.cell($(this).closest('td, li')).index();
        inventario.items.prod[tr.row].serie = serie;
    });

    $('#save').on('click', function () {
        var parametros;
        parametros = {'inventario': JSON.stringify(inventario.items)};
        save_with_ajax('Alerta',
            '/inventario/crear', 'Esta seguro que desea registrar estos productos en el inventario?', parametros, function (response) {
                location.href = '/compra/lista';
            });
    });

});