var user_tipo = parseInt($('input[name="user_tipo"]').val());
var grapie, chart, graph;
function graficos() {
grapie = Highcharts.chart('grapie', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: 'Porcentaje de venta por Producto',
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%'],
            size: '110%'
        }
    },
});
chart = Highcharts.chart('container2', {
    chart: {
        inverted: true,
        polar: false
    },

    title: {
        text: 'Total de Ventas del año'
    },
    xAxis: {
        categories: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    },
    yAxis: {
        title: {
            text: 'Valores'
        }
    },

});
graph = Highcharts.chart('container3', {
    chart: {
        type: 'line'
    },
    title: {
        text: ''
    },
    subtitle: {
        text: 'Contraste de compras y ventas'
    },
    xAxis: {
        categories: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    },
    yAxis: {
        title: {
            text: 'Dolares $'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: true
            },
            enableMouseTracking: false
        }
    },
});
$.ajax({
        url: '/venta/chart',
        type: 'POST',
        data: {'action': 'chart'},
        dataSrc: "",
    }).done(function (data) {
        chart.addSeries(data['dat']);
        grapie.addSeries(
            {
                type: 'pie',
                name: 'Total',
                innerSize: '50%',
                data: data['chart2'].data
            }
        );
        graph.addSeries(
            {
                name: 'Compras',
                data: data['chart3'].compras
            },
        );
        graph.addSeries(
            {
                name: 'Ventas',
                data: data['chart3'].ventas
            }
        );
        var tarjets = data['tarjets'];
       $('#venta_tarjet').html(parseInt(tarjets['data'].ventas)+ '&nbsp;'+'<i class="fas fa-cart-arrow-down"></i>');
       $('#compra_tarjet').html(parseInt(tarjets['data'].compras)+ '&nbsp;'+'<i class="fab fa-shopify"></i>');
       $('#inv_tarjet').html(parseInt(tarjets['data'].inventario)+ '&nbsp;'+'<i class="fab fa-amazon"></i>');
       $('#inv_tarjet_agot').html(parseInt(tarjets['data'].agotados)+ '&nbsp;'+'<i class="fas fa-battery-empty"></i>');
    });
}


function datatbles() {
    $("#datatable").DataTable({
        autoWidth: false,
        dom: "tip",
        ScrollX: '90%',
        language: {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
        },
        ajax: {
            url: '/producto/index',
            type: 'POST',
            dataSrc: "",
        },
        columns: [
            {data: "producto_base.nombre"},
            {data: "producto_base.categoria.nombre"},
            {data: "producto_base.presentacion.nombre"},
            {data: "producto_base.stock"},
            {data: "imagen"}
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<span>' + data + '</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" width="30" height="30" class="img-circle elevation-2" alt="User Image">';
                }
            }
        ],
        createdRow: function (row, data, dataIndex) {
            $('td', row).eq(3).find('span').addClass('badge bg-danger').attr("style", "color: white");
        }
    });
    $("#datatable2").DataTable({
        autoWidth: false,
        // responsive: true,
        dom: "tip",
        // ScrollX: '90%',
        language: {
            "url": "//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json"
        },
        ajax: {
            url: '/compra/index',
            type: 'POST',
            dataSrc: "",
        },
        columns: [
            {data: 'compra.fecha_compra'},
            {data: "material.producto_base.nombre"},
            {data: "material.producto_base.presentacion.nombre"},
            {data: "cantidad"},
            {data: "compra.total"}
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + data;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                width: '10%'
            },
            {
                targets: '_all',
                class: 'text-center',
                orderable: false
            }
        ]
    });
}



$(function () {
    if (user_tipo === 1) {
        datatbles();
         graficos();
    } else {
        $('#venta_client').on('click', function () {
            window.location.href = '/venta/lista'

        });
     $('#alquiler_client').on('click', function () {
            window.location.href = '/alquiler/lista'

        })

    }


});