var datatable;
var logotipo;
const toDataURL = url => fetch(url).then(response => response.blob())
    .then(blob => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob)
    }));

toDataURL('/media/imagen.PNG').then(dataUrl => {
    logotipo = dataUrl;
});
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
            {"data": "fecha_ingreso"},
            {"data": "asignacion.lote"},
            {"data": "novedades"},
            {"data": "estado_text"},
            {"data": "id"}
        ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        order: [[3, "desc"]],
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
                        columns: [0, 1, 2, 3, 4, 5],
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
                                columns: [{alignment: 'center', image: logotipo, width: 300}],
                                margin: [280, 10, 0, 0] //[izquierda, arriba, derecha, abajo]
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
                        doc.content[1].table.widths = ['*', '*', '*', '*', '*', '*'];
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
                    var detalle_asig = '<a type="button" rel="detalle_asig" class="btn btn-info btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Detalle de Asignacion" ><i class="fab fa-searchengin"></i></a>' + ' ';
                    var detalle = '<a type="button" rel="detalle" class="btn btn-success btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Detalle de Ingresos de Produccion" ><i class="fa fa-search"></i></a>' + ' ';
                    var anular = '<a type="button" rel="anular" class="btn btn-danger btn-xs btn-round" style="color: white" data-toggle="tooltip" title="Anular"><i class="fa fa-times"></i></a>' + ' ';
                    var agregar = '<a type="button" rel="agregar" class="btn btn-warning btn-xs btn-round" href="add_recurso/'+data+'" style="color: white" data-toggle="tooltip" title="Agregar recursos"><i class="fas fa-plus"></i></a>' + ' ';
                    var finalizar = '<a type="button" rel="finalizar" class="btn btn-success btn-xs btn-round" href="finalizar/'+data+'" style="color: white" data-toggle="tooltip" title="Finalizar Produccion"><i class="far fa-calendar-check"></i></a>' + ' ';
                    return detalle_asig + agregar + detalle + anular+ finalizar;
                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data.estado === 0) {
                $('td', row).eq(3).find('span').addClass('badge bg-success').attr("style", "color: white");
            } else if (data.estado === 2) {
                $('td', row).eq(3).find('span').addClass('badge bg-danger').attr("style", "color: white");
                $('td', row).eq(4).find('a[rel="anular"]').hide();
                $('td', row).eq(4).find('a[rel="detalle_asig"]').hide();

            } else if (data.estado === 1) {
                $('td', row).eq(3).find('span').addClass('badge bg-info').attr("style", "color: white");
                $('td', row).eq(4).find('a[rel="detalle"]').hide();

            }
        }
    });
    $('#datatable tbody')
        .on('click', 'a[rel="anular"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'delete'};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea anular este ingreso de produccion?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al anular este ingreso de produccion', 'far fa-smile-wink', function () {
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
                    {data: 'producto_base.nombre'},
                    {data: 'producto_base.categoria.nombre'},
                    {data: 'producto_base.presentacion.nombre'},
                    {data: 'total'}
                ]
            });
            $("#tblperdida_productos").DataTable({
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
                        'action': 'detalle_perdidas_productos',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: 'producto_base.nombre'},
                    {data: 'producto_base.categoria.nombre'},
                    {data: 'producto_base.presentacion.nombre'},
                    {data: 'id'}
                ]
            });

            $("#tblperdida_materiales").DataTable({
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
                        'action': 'detalle_perdidas_materiales',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: 'material.producto_base.nombre'},
                    {data: 'material.producto_base.categoria.nombre'},
                    {data: 'material.producto_base.presentacion.nombre'},
                    {data: 'id'}
                ]
            });

        })
        .on('click', 'a[rel="detalle_asig"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('#Modal_materiales').modal('show');
            $("#tbldetalle_materiales").DataTable({
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
                        'action': 'detalle_materiales',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: 'producto_base.nombre'},
                    {data: 'producto_base.categoria.nombre'},
                    {data: 'calidad'},
                    {data: 'producto_base.color.nombre'},
                    {data: 'tipo_material.nombre'},
                    {data: 'medida'},
                    {data: 'ud_medida'},
                    {data: 'total'}
                ]
            });
            $("#tbldetalle_maquinas").DataTable({
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
                        'action': 'detalle_maquinas',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: 'maquina.tipo.nombre'},
                    {data: 'maquina.serie'}
                ]
            });
            $("#tblproductos_estimados").DataTable({
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
                        'action': 'detalle_estimados',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: 'producto_base.nombre'},
                    {data: 'producto_base.categoria.nombre'},
                    {data: 'presentacion.nombre'},
                    {data: 'producto_base.color.nombre'},
                    {data: 'talla.talla'},
                    {data: 'total'}
                ]
            });

        })
        .on('click', 'a[rel="finalizar"]', function () {
            $('.tooltip').remove();
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id, 'action': 'finalizar'};
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea finalizar esta asignacion?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al finalizar esta asignacion', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false);
                    })
                });

        });

    $('#nuevo').on('click', function () {
        window.location.href = '/produccion/nuevo';

    })
});

function daterange() {
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
