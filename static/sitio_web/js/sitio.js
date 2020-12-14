
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
            dict.subtotal = dict.cantidad * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
            iva_emp = (dict.iva_emp/100);
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
        this.list();
    },
    list: function () {
        this.calculate();
        tblventa = $("#datatable").DataTable({
            dom: 't'
        });
    },
     exclude_duplicados: function (array) {
        this.items.productos = [];
        let hash = {};
        result = array.filter(o => hash[o.id] ? false : hash[o.id] = true);
        return result;

    }
};
function container_popular() {
    $.ajax({
        url: '/producto/lista',
        type: 'POST',
        data: {'action': 'sitio'},
        dataSrc: "",
    }).done(function (data) {
        var html = '<div class="columns is-centered is-multiline">' +
            '<div class="column is-full">' +
            '<div class="separator"></div>' +
            '</div>';

        $.each(data, function (key, value) {
            html += '<div class="column is-half-tablet is-one-third-desktop column-half">' +
                '<div class="card">' +
                '<input type="hidden" class="set_venta" value="' + value['id_venta'] + '">' +
                '<input type="hidden" class="set_alquiler" value="' + value['id_alquiler'] + '">' +
                '<input type="hidden" class="set_confeccion" value="' + value['id_confeccion'] + '">' +
                '<img src="' + value['imagen'] + '" alt="">' +
                '<div class="card-info">' +
                '<h4 class="has-text-black has-text-centered has-text-weight-bold"> ' + value['info'] + '</h4>' +
                '<p class="has-text-centered">' + value['descripcion'] + '</p>' +
                '<p class="has-text-centered"> <strong>Precio de venta:</strong> $' + value['pvp'] + '</p>' +
                '<p class="has-text-centered"> <strong>Precio de Alquiler:</strong> $' + value['pvp_alq'] + '</p>' +
                '<p class="has-text-centered"> <strong>Precio de Confeccion:</strong> $' + value['pvp_confec'] + '</p>' +
                '<div class="card-buttons">' +
                '<button class="btn btn--mini-rounded" name="vender" value="' + value['id_venta'] + '" data-toggle="tooltip" title="Comprar"><i class="zmdi zmdi-shopping-cart"></i></button>' +
                '<a class="btn btn--mini-rounded alquilar" data-toggle="tooltip" title="Alquilar"><i class="zmdi zmdi-label"></i></a>' +
                '<a class="btn btn--mini-rounded confeccionar" data-toggle="tooltip" title="Confeccion"><i class="zmdi zmdi-money-box"></i></a>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>'
        });
        $('#pop').html(html);
    });

}

$(function () {
    // $('button[name="vender"]').on('click', function () {
    //        console.log(25)
    //    });

    $(document).on('click', 'button[name="vender"]', function (e) {
         $.ajax({
            type: "POST",
            url: '/producto/lista',
            data: {
                "id": $(this).val(),
                'action': 'get'
            },
            dataType: 'json',
            success: function (data) {
                carrito.add(data);
            },
            error: function (xhr, status, data) {
                alert(data);
            },

        })

    });
});