var datatable;
var user_tipo = $('input[name="user_tipo"]').val();
var datos = {
    fechas: {
        'start_date': '',
        'end_date': '',
        'action': 'confeccion',
    },
    add: function (data) {
        if (data.key === 1) {
            this.fechas['start_date'] = data.startDate.format('YYYY-MM-DD');
            this.fechas['end_date'] = data.endDate.format('YYYY-MM-DD');
        } else {
            this.fechas['start_date'] = '';
            this.fechas['end_date'] = '';
        }
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            data: this.fechas,
            success: function (data) {
                datatable.clear();
                datatable.rows.add(data).draw();
            }
        });

    },
};
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    daterange();
    datatable = $("#datatable").DataTable({
        // responsive: true,
        destroy: true,
        scrollX: true,
        autoWidth: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: datos.fechas,
            dataSrc: ""
        },
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        order: [[0, "desc"]],
        dom: "<'row'<'col-sm-12 col-md-12'B>>" +
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        buttons: {
            dom: {
                button: {
                    className: '',

                },
                container: {
                    className: 'buttons-container float-md-right'
                }
            },
            buttons: [
                {
                    text: '<i class="fa fa-file-excel"> </i> Excel', className: "btn btn-success my_class",
                    extend: 'excel'
                },
                {
                    text: '<i class="fa fa-file-pdf"> </i> PDF',
                    className: 'btn btn-danger my_class',
                    extend: 'pdfHtml5',
                    //filename: 'dt_custom_pdf',
                    orientation: 'landscape', //portrait
                    pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                    download: 'open',
                    exportOptions: {
                        columns: [0, 1, 2, 3, 4, 5, 6, 7],
                        search: 'applied',
                        order: 'applied'
                    },
                    customize: function (doc) {
                        const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                            "Noviembre", "Diciembre"
                        ];
                        var date = new Date();

                        function formatDateToString(date) {
                            // 01, 02, 03, ... 29, 30, 31
                            var dd = (date.getDate() < 10 ? '0' : '') + date.getDate();
                            // 01, 02, 03, ... 10, 11, 12
                            // month < 10 ? '0' + month : '' + month; // ('' + month) for string result
                            var MM = monthNames[date.getMonth() + 1]; //monthNames[d.getMonth()])
                            // 1970, 1971, ... 2015, 2016, ...
                            var yyyy = date.getFullYear();
                            // create the format you want
                            return (dd + " de " + MM + " de " + yyyy);
                        }

                        var jsDate = formatDateToString(date);

                        //[izquierda, arriba, derecha, abajo]
                        doc.pageMargins = [25, 180, 25, 50];
                        doc.defaultStyle.fontSize = 12;
                        doc.styles.tableHeader.fontSize = 14;
                        doc['header'] = (function () {
                            return {
                                columns: [{
                                    alignment: 'center',
                                    italics: true,
                                    text: empresa,
                                    fontSize: 45,

                                }],
                            }
                        });
                        doc['footer'] = (function (page, pages) {
                            return {
                                columns: [
                                    {
                                        alignment: 'left',
                                        text: ['Reporte creado el: ', {text: jsDate.toString()}]
                                    },
                                    {
                                        alignment: 'right',
                                        text: ['Pagina ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                    }
                                ],
                                margin: 20
                            }
                        });
                        var objLayout = {};
                        objLayout['hLineWidth'] = function (i) {
                            return .5;
                        };
                        objLayout['vLineWidth'] = function (i) {
                            return .5;
                        };
                        objLayout['hLineColor'] = function (i) {
                            return '#000000';
                        };
                        objLayout['vLineColor'] = function (i) {
                            return '#000000';
                        };
                        objLayout['paddingLeft'] = function (i) {
                            return 4;
                        };
                        objLayout['paddingRight'] = function (i) {
                            return 4;
                        };
                        doc.content[0].layout = objLayout;
                        doc.content[1].table.widths = [65, '*', "*", 85, 75, 85, '*', '*'];
                        doc.styles.tableBodyEven.alignment = 'center';
                        doc.styles.tableBodyOdd.alignment = 'center';
                    }
                },
            ],
        },
        columns: [
            {data: 'transaccion.fecha_trans'},
            {data: 'fecha_entrega'},
            {data: "transaccion.user.full_name"},
            {data: "transaccion.subtotal"},
            {data: "transaccion.iva"},
            {data: "transaccion.total"},
            {data: "transaccion.id"},
            {data: "estado"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',

            },
            {
                targets: [-4, -5, -6],
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
                    return '<span>' + data + '</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                width: '15%',
                render: function (data, type, row) {
                    console.log(row);
                    var detalle = '<a type="button" rel="detalle" class="btn btn-success btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Detalle de Productos" ><i class="fa fa-search"></i></a>' + ' ';
                    var entregar = row.transaccion.user.tipo === 1 ? '<a type="button" rel="entregar" class="btn btn-warning btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Entregar" ><i class="fa fa-check"></i></a>' + ' ': '';
                    var devolver = row.transaccion.user.tipo === 1 ? '<a type="button" rel="devolver" class="btn btn-danger btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Devolver"><i class="fa fa-times"></i></a>' + ' ': '';
                    var pdf = row.transaccion.user.tipo === 1 ? '<a type="button" href= "/confeccion/printpdf/' + data + '" rel="pdf" class="btn btn-primary btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Reporte PDF"><i class="fa fa-file-pdf"></i></a>':'';
                    var dar = row.estado === 3 ? '<a type="button" rel="dar" class="btn btn-primary btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Confirmar"><i class="fas fa-thumbs-up"></i></a>' : '';
                    return detalle + dar + entregar + devolver + pdf;
                }
            },
            {
                targets: [-3],
                render: function (data, type, row) {
                    return pad(data, 10);
                }
            }
        ],
        createdRow: function (row, data, dataIndex) {
            console.log(data.confeccion.estado);
            if (data.estado === 1) {
                $('td', row).eq(7).html('<span class="badge badge-success" style="color: white"> ENTREGADA');
                $('td', row).eq(8).find('a[rel="entregar"]').hide();
                if (user_tipo === '0') {
                    $('td', row).eq(8).find('a[rel="devolver"]').hide();
                }
            } else if (data.estado === 0) {
                if (data.confeccion.estado === 1) {
                    $('td', row).eq(7).html('<span class="badge badge-warning" style="color: white"> EN PRODUCCION');
                    $('td', row).eq(1).html('<span class="badge badge-warning" style="color: white"> SIN FECHA');
                    $('td', row).eq(8).find('a[rel="entregar"]').hide();
                } else {
                    $('td', row).eq(7).html('<span class="badge badge-warning" style="color: white"> POR ENTREGAR');
                    $('td', row).eq(1).html('<span class="badge badge-warning" style="color: white"> SIN FECHA');
                    if (user_tipo === '0') {
                        $('td', row).eq(8).find('a[rel="entregar"]').hide();
                        $('td', row).eq(8).find('a[rel="devolver"]').hide();
                    }
                }

            } else if (data.estado === 2) {
                $('td', row).eq(7).html('<span class="badge badge-danger" style="color: white"> ANULADA');
                $('td', row).eq(1).html('<span class="badge badge-danger" style="color: white"> ANULADA');
                $('td', row).eq(8).find('a[rel="devolver"]').hide();
                $('td', row).eq(8).find('a[rel="entregar"]').hide();
                $('td', row).eq(8).find('a[rel="pdf"]').hide();
            } else if (data.estado === 3) {
                $('td', row).eq(7).html('<span class="badge badge-primary" style="color: white"> RESERVADA');
                $('td', row).eq(1).html('<span class="badge badge-primary" style="color: white"> RESERVADA');
                $('td', row).eq(8).find('a[rel="entregar"]').hide();
                if (user_tipo === '0') {
                    $('td', row).eq(8).find('a[rel="entregar"]').hide();
                    $('td', row).eq(8).find('a[rel="dar"]').hide();
                }
            }

        }
    });

    $('#datatable tbody')
        .on('click', 'a[rel="devolver"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'anular'};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea anular/delvover esta confeccion?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al anular/delvover la confeccion', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    })
                });

        })
        .on('click', 'a[rel="entregar"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'entregar'};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea realizar la entrega de esta/as confecciones?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al entregar la/as confecciones', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    });

                });
        })
        .on('click', 'a[rel="detalle"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('#Modal').modal('show');
            $("#tbldetalle_productos").DataTable({
                responsive: true,
                autoWidth: false,
                language: {
                    "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
                },
                destroy: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'Post',
                    data: {
                        'id': data.confeccion.id,
                        'action': 'detalle'
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: 'producto'},
                    {data: 'categoria'},
                    {data: 'color'},
                    {data: 'talla'},
                    {data: 'cantidad'},
                    {data: 'pvp'},
                    {data: 'subtotal'}
                ],
                columnDefs: [
                    {
                        targets: '_all',
                        class: 'text-center'
                    },

                    {
                        targets: [-1, -2],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                ],
                footerCallback: function (row, data, start, end, display) {
                    var api = this.api(), data;

                    // Remove the formatting to get integer data for summation
                    var intVal = function (i) {
                        return typeof i === 'string' ?
                            i.replace(/[\$,]/g, '') * 1 :
                            typeof i === 'number' ?
                                i : 0;
                    };
                    // Total over this page
                    pageTotal = api
                        .column(3, {page: 'current'})
                        .data()
                        .reduce(function (a, b) {
                            return intVal(a) + intVal(b);
                        }, 0);

                    // Update footer
                    $(api.column(3).footer()).html(
                        '$' + parseFloat(pageTotal).toFixed(2)
                        // parseFloat(data).toFixed(2)
                    );
                },
            });
        })
        .on('click', 'a[rel="dar"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'estado'};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea realizar la confirmacion de esta/as confeccion/es?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al confirmar la confeccion', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    });

                });
        });

    $('#nuevo').on('click', function () {
        if (user_tipo === '0') {
            window.location.href = '/confeccion/nuevo_online'
        } else {
            window.location.href = '/confeccion/nuevo'
        }

    })
});

function daterange() {
    $("div.toolbar").html('<br><div class="col-lg-3"><input type="text" name="fecha" class="form-control form-control-sm input-sm"></div> <br>');
    $('input[name="fecha"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-search"></i> Buscar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        picker['key'] = 1;
        datos.add(picker);
        // filter_by_date();

    }).on('cancel.daterangepicker', function (ev, picker) {
        picker['key'] = 0;
        datos.add(picker);

    });

}

function pad(str, max) {
    str = str.toString();
    return str.length < max ? pad("0" + str, max) : str;
}
