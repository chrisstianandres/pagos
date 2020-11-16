var datatable;
var logotipo;
const toDataURL = url => fetch(url).then(response => response.blob())
    .then(blob => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob)
    }));

toDataURL('/media/logo_don_chuta.png').then(dataUrl => {
    logotipo = dataUrl;
});
var datos = {
    fechas: {
        'start_date': '',
        'end_date': '',
        'tipo': 0
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
            url: '/venta/data_report',
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
    $('.tipo_prod').select2().on('select2:select', function (e) {
        datos.fechas.tipo = $('.tipo_prod option:selected').val();
        $.ajax({
            type: "POST",
            url: '/venta/data_report',
            data: datos.fechas,
            dataType: 'json',
            success: function (data) {
                datatable.clear();
                datatable.rows.add(data).draw();
            },
        })
    });
    datatable = $("#datatable").DataTable({
        destroy: true,
        scrollX: true,
        autoWidth: false,
        order: [[ 2, "asc" ]],
        ajax: {
            url: '/venta/data_report',
            type: 'POST',
            data: datos.fechas,
            dataSrc: ""
        },
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
            searchPanes: {
                clearMessage: 'Limpiar Filtros',
                collapse: {
                    0: 'Filtros de Busqueda',
                    _: 'Filtros seleccionados (%d)'
                },
                title: {
                    _: 'Filtros seleccionados - %d',
                    0: 'Ningun Filtro seleccionado',
                },
                activeMessage: 'Filtros activos (%d)',
                emptyPanes: 'There are no panes to display. :/',
                sZeroRecords: "No se encontraron resultados",

            }
        },

         dom: 'l<"toolbar">'+"<br>"+'Bfrtip ',
        buttons: [
            {
                className: 'btn-default my_class',
                extend: 'searchPanes',
                config: {
                    cascadePanes: true,
                    viewTotal: true,
                    layout: 'columns-5'
                }
            },
            {
                text: '<i class="far fa-file-pdf"></i> Reporte PDF</i>',
                className: 'btn btn-danger',
                extend: 'pdfHtml5',
                footer: true,
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
                        var MM = monthNames[date.getMonth()]; //monthNames[d.getMonth()])
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
                    doc.content[1].table.widths = ["*", "*", "*", "*", "*","*","*", "*"];
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
                    doc.styles.tableFooter.alignment = 'center';
                }
            },
            {
                text: '<i class="far fa-file-excel"></i> Reporte Excel</i>', className: "btn btn-success my_class",
                extend: 'excel',
                footer: true
            },
            {
                text: '<i class="fas fa-funnel-dollar"></i> Reporte por Totales</i>',
                className: 'btn-primary my_class',
                action: function (e, dt, node, config) {
                    window.location.href = '/venta/report_total'
                }
            },
        ],
        columnDefs: [
            {
                searchPanes: {
                    show: true,
                },
                targets: [1, 2],
            },
            {
                searchPanes: {
                    show: true,
                    options: [
                        {
                            label: 'Menos de  10',
                            value: function (rowData, rowIdx) {
                                return rowData[3] < 10;
                            }
                        },
                        {
                            label: ' 10 a  50',
                            value: function (rowData, rowIdx) {
                                return rowData[3] <= 50 && rowData[3] >= 10;
                            }
                        },
                        {
                            label: ' 50 a  100',
                            value: function (rowData, rowIdx) {
                                return rowData[3] <= 100 && rowData[3] >= 50;
                            }
                        },
                        {
                            label: 'Mas de 100',
                            value: function (rowData, rowIdx) {
                                return rowData[3] > 100;
                            }
                        },
                    ]
                },
                targets: [3],
            },
            {
                searchPanes: {
                    show: true,
                    options: [
                        {
                            label: 'Menos de $ 10',
                            value: function (rowData, rowIdx) {
                                return rowData[4] < 10;
                            }
                        },
                        {
                            label: '$ 10 a $ 50',
                            value: function (rowData, rowIdx) {
                                return rowData[4] <= 50 && rowData[4] >= 10;
                            }
                        },
                        {
                            label: '$ 50 a $ 100',
                            value: function (rowData, rowIdx) {
                                return rowData[4] <= 100 && rowData[4] >= 50;
                            }
                        },
                        {
                            label: '$ 100 a $ 200',
                            value: function (rowData, rowIdx) {
                                return rowData[4] <= 200 && rowData[4] >= 100;
                            }
                        },
                        {
                            label: '$ 200 a $ 300',
                            value: function (rowData, rowIdx) {
                                return rowData[4] <= 300 && rowData[4] >= 200;
                            }
                        },
                        {
                            label: '$ 300 a $ 400',
                            value: function (rowData, rowIdx) {
                                return rowData[4] <= 400 && rowData[4] >= 300;
                            }
                        },
                        {
                            label: '$ 400 a $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[4] <= 500 && rowData[4] >= 400;
                            }
                        },
                        {
                            label: 'Mas de $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[4] > 500;
                            }
                        },
                    ]
                },
                targets: [4],
            },
            {
                searchPanes: {
                    show: true,
                    options: [
                        {
                            label: 'Menos de  $ 10',
                            value: function (rowData, rowIdx) {
                                return rowData[5] < 10;
                            }
                        },
                        {
                            label: '$ 10 a $ 50',
                            value: function (rowData, rowIdx) {
                                return rowData[5] <= 50 && rowData[5] >= 10;
                            }
                        },
                        {
                            label: '$ 50 a $ 100',
                            value: function (rowData, rowIdx) {
                                return rowData[5] <= 100 && rowData[5] >= 50;
                            }
                        },
                        {
                            label: '$ 100 a $ 200',
                            value: function (rowData, rowIdx) {
                                return rowData[5] <= 200 && rowData[5] >= 100;
                            }
                        },
                        {
                            label: '$200 a  $ 300',
                            value: function (rowData, rowIdx) {
                                return rowData[5] <= 300 && rowData[5] >= 200;
                            }
                        },
                        {
                            label: '$ 300 a $ 400',
                            value: function (rowData, rowIdx) {
                                return rowData[5] <= 400 && rowData[5] >= 300;
                            }
                        },
                        {
                            label: '$ 400 a $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[5] <= 500 && rowData[5] >= 400;
                            }
                        },
                        {
                            label: 'Mas de  $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[5] > 500;
                            }
                        },
                    ]
                },
                targets: [5],
            },
            {
                searchPanes: {
                    show: true,
                    options: [
                        {
                            label: 'Menos de  $ 10',
                            value: function (rowData, rowIdx) {
                                return rowData[6] < 10;
                            }
                        },
                        {
                            label: '$ 10 a $ 50',
                            value: function (rowData, rowIdx) {
                                return rowData[6] <= 50 && rowData[6] >= 10;
                            }
                        },
                        {
                            label: '$ 50 a $ 100',
                            value: function (rowData, rowIdx) {
                                return rowData[6] <= 100 && rowData[6] >= 50;
                            }
                        },
                        {
                            label: '$ 100 a $ 200',
                            value: function (rowData, rowIdx) {
                                return rowData[6] <= 200 && rowData[6] >= 100;
                            }
                        },
                        {
                            label: '$200 a  $ 300',
                            value: function (rowData, rowIdx) {
                                return rowData[6] <= 300 && rowData[6] >= 200;
                            }
                        },
                        {
                            label: '$ 300 a $ 400',
                            value: function (rowData, rowIdx) {
                                return rowData[6] <= 400 && rowData[6] >= 300;
                            }
                        },
                        {
                            label: '$ 400 a $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[6] <= 500 && rowData[6] >= 400;
                            }
                        },
                        {
                            label: 'Mas de  $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[6] > 500;
                            }
                        },
                    ]
                },
                targets: [6],
            },
            {
                searchPanes: {
                    show: true,
                    options: [
                        {
                            label: 'Menos de  $ 10',
                            value: function (rowData, rowIdx) {
                                return rowData[7] < 10;
                            }
                        },
                        {
                            label: '$ 10 a $ 50',
                            value: function (rowData, rowIdx) {
                                return rowData[7] <= 50 && rowData[7] >= 10;
                            }
                        },
                        {
                            label: '$ 50 a $ 100',
                            value: function (rowData, rowIdx) {
                                return rowData[7] <= 100 && rowData[7] >= 50;
                            }
                        },
                        {
                            label: '$ 100 a $ 200',
                            value: function (rowData, rowIdx) {
                                return rowData[7] <= 200 && rowData[7] >= 100;
                            }
                        },
                        {
                            label: '$200 a  $ 300',
                            value: function (rowData, rowIdx) {
                                return rowData[7] <= 300 && rowData[7] >= 200;
                            }
                        },
                        {
                            label: '$ 300 a $ 400',
                            value: function (rowData, rowIdx) {
                                return rowData[7] <= 400 && rowData[7] >= 300;
                            }
                        },
                        {
                            label: '$ 400 a $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[7] <= 500 && rowData[7] >= 400;
                            }
                        },
                        {
                            label: 'Mas de  $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[7] > 500;
                            }
                        },
                    ]
                },
                targets: [7],
            },
            {
                targets: '_all',
                class: 'text-center',

            },
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                width: '20%',
                render: function (data, type, row) {
                    return '$ ' + data;
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
            pageTotalsiniva = api
                .column(5, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);
            totaliva = api.column( 5 ).data().reduce( function (a, b) {
                         return intVal(a) + intVal(b);
                         }, 0 );
            pageTotaliva = api
                .column(6, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);
            totalconiva = api.column( 6 ).data().reduce( function (a, b) {
                         return intVal(a) + intVal(b);
                         }, 0 );
            pageTotalconiva = api
                .column(7, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);
            totalconiva = api.column( 7 ).data().reduce( function (a, b) {
                         return intVal(a) + intVal(b);
                         }, 0 );

            cantTotal = api
                .column(3, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);

            // Update footer
            $(api.column(5).footer()).html(
                '$' + parseFloat(pageTotalsiniva).toFixed(2) + '( $ ' + parseFloat(pageTotalsiniva).toFixed(2) + ')'
                // parseFloat(data).toFixed(2)
            );
            $(api.column(6).footer()).html(
                '$' + parseFloat(pageTotaliva).toFixed(2) + '( $ ' + parseFloat(pageTotaliva).toFixed(2) + ')'
                // parseFloat(data).toFixed(2)
            );
            $(api.column(7).footer()).html(
                '$' + parseFloat(pageTotalconiva).toFixed(2) + '( $ ' + parseFloat(pageTotalconiva).toFixed(2) + ')'
                // parseFloat(data).toFixed(2)
            );
            $(api.column(3).footer()).html(
                cantTotal
                // parseFloat(data).toFixed(2)
            );
        },

    });
});

function daterange() {
    // $("div.toolbar").html('<br><div class="col-lg-3"><input type="text" name="fecha" class="form-control form-control-sm input-sm"></div> <br>');
    $('input[name="fecha"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-search"></i> Buscar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        picker['key'] = 1;
        picker['tipo'] = $('.tipo_prod option:selected').val();
        datos.add(picker);
        // filter_by_date();

    }).on('cancel.daterangepicker', function (ev, picker) {
        picker['key'] = 0;
        picker['tipo'] = $('.tipo_prod option:selected').val();
        datos.add(picker);
    });

}
