var datatable;
var datos = {
    fechas: {
        'start_date': '',
        'end_date': '',
        'action': 'list'
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
    daterange();
    datatable = $("#datatable").DataTable({
        destroy: true,
        scrollX: true,
        autoWidth: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: datos.fechas,
            dataSrc: ""
        },
        columns: [
            {"data": "fecha_asig"},
            {"data": "user"},
            {"data": "estado_label"},
            {"data": "id"}
        ],
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
                    text: '<i class="fa fa-file-excel"></i> Excel', className: "btn btn-success my_class",
                    extend: 'excel'
                },
                {
                    text: '<i class="fa fa-file-pdf"></i> PDF',
                    className: 'btn btn-danger my_class',
                    extend: 'pdfHtml5',
                    //filename: 'dt_custom_pdf',
                    orientation: 'landscape', //portrait
                    pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                    download: 'open',
                    exportOptions: {
                        columns: [0, 1, 2, 3],
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
                        doc.pageMargins = [25, 120, 25, 50];
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
                        doc.content[1].table.widths = ['*', '*', '*', '*'];
                        doc.styles.tableBodyEven.alignment = 'center';
                        doc.styles.tableBodyOdd.alignment = 'center';
                    }
                },
            ],
        },
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',

            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<span>' + data + '</span>';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                width: "15%",
                render: function (data, type, row) {
                    var detalle = '<a type="button" rel="detalle" class="btn btn-success btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Detalle de Asignacion" ><i class="fa fa-search"></i></a>' + ' ';
                    var devolver = '<a type="button" rel="devolver" class="btn btn-danger btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Anular"><i class="fa fa-times"></i></a>' + ' ';
                    var finaizar = '<a type="button" rel="finalizar" class="btn btn-warning btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Finalizar"><i class="fas fa-hourglass-end"></i></a>' + ' ';
                    var controlar = row.estado === 1 ? '<a type="button" rel="controlar" class="btn btn-primary btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Controlar Confeccion"><i class="fa fa-cog"></i></a>' + ' ' : ' ';
                    return detalle + controlar + finaizar + devolver;
                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data.estado === 1) {
                $('td', row).eq(2).find('span').addClass('badge bg-warning').attr("style", "color: white");
            } else if (data.estado === 2) {
                $('td', row).eq(2).find('span').addClass('badge bg-success').attr("style", "color: white");
                $('td', row).eq(3).find('a[rel="devolver"]').hide();
                $('td', row).eq(3).find('a[rel="finalizar"]').hide();
            } else if (data.estado === 0) {
                $('td', row).eq(2).find('span').addClass('badge bg-danger').attr("style", "color: white");
                $('td', row).eq(3).find('a[rel="devolver"]').hide();
                $('td', row).eq(3).find('a[rel="finalizar"]').hide();
            }
        }
    });
    $('#datatable tbody')
        .on('click', 'a[rel="devolver"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea anular esta confeccion?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al anular esta confeccion', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    })
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
                        'action': 'detalle',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "producto_base.nombre"},
                    {data: "producto_base.categoria.nombre"},
                    {data: "calidad"},
                    {data: "color.nombre"},
                    {data: "tipo_material.nombre"},
                    {data: "medida_full"},
                    {data: "cant"}
                ]
            });
            $("#tbldetalle_servicios").DataTable({
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
                        'action': 'detalle_maquina',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: 'maquina.tipo.nombre'},
                    {data: 'maquina.serie'}
                ]
            });


            $("#tbldetalle_prendas").DataTable({
                responsive: true,
                autoWidth: true,
                language: {
                    "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
                },
                destroy: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'Post',
                    data: {
                        'action': 'detalle_prendas',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "producto_base.nombre"},
                    {data: "producto_base.categoria.nombre"},
                    {data: "color.nombre"},
                    {data: "talla.talla_full"},
                    {data: "cantidad"}
                ]
            });
            $("#tbldetalle_novedades").DataTable({
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
                        'action': 'detalle_novedades',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "fecha"},
                    {data: "novedad"},
                ]
            });
            $("#tbldetalle_perdidas").DataTable({
                autoWidth: false,
                responsive: true,
                language: {
                    "url": '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
                },
                destroy: true,
                ajax: {
                    url: window.location.pathname,
                    type: 'Post',
                    data: {
                        'action': 'detalle_perdidas',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "producto_base.nombre"},
                    {data: "producto_base.categoria.nombre"},
                    {data: "calidad"},
                    {data: "color.nombre"},
                    {data: "tipo_material.nombre"},
                    {data: "medida_full"},
                    {data: "cantidad"}
                ]
            });

        })
        .on('click', 'a[rel="finalizar"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'finalizar'};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea finalizar esta confeccion?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al finalizar esta confeccion', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    })
                });

        })
        .on('click', 'a[rel="controlar"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            window.location.replace('/asignacion/control/' + data.id);
        });

    $('#nuevo').on('click', function () {
        window.location.href = '/asignacion/nuevo';

    })
});

function daterange() {
    $('input[name="fecha"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-search"></i> Buscar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        },
        showDropdowns: true,
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
