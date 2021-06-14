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
        'action': 'report'
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
        responsive: true,
        autoWidth: false,
        order: [[2, "asc"]],
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: datos.fechas,
            dataSrc: ""
        },
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },

       dom: "<'row'<'col-sm-12 col-md-12'B>>" +
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>"+
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        //"<'row'<'col-md-6'l><'col-md-6'Bf>>"
        buttons: {
             dom: {
                button: {
                    className: '',

                },
                container: {
                    className: 'buttons-container float-right'
                }
            },
            buttons: [
            {
                text: '<i class="far fa-file-pdf"></i> Reporte PDF',
                className: 'btn btn-danger',
                extend: 'pdfHtml5',
                footer: true,
                //filename: 'dt_custom_pdf',
                orientation: 'landscape', //portrait
                pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                download: 'open',
                exportOptions: {
                    columns: [0, 1, 2, 3, 4],
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
                    doc.content[1].table.widths = ["*", "*", "*", "*", "*"];
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
                    doc.styles.tableFooter.alignment = 'center';
                }
            },
            {
                text: '<i class="far fa-file-excel"></i> Reporte Excel', className: "btn btn-success my_class",
                extend: 'excel',
                footer: true
            },
                {
                text: '<i class="fas fa-tags"></i> Alquileres Reservados',
                className: 'btn btn-info',
                action: function (e, dt, node, config) {
                    window.location.href = '/alquiler/report_total_reservadas'
                }
            },
            {
                text: '<i class="fas fa-tags"></i> Alquileres no entregados',
                className: 'btn btn-primary',
                action: function (e, dt, node, config) {
                    window.location.href = '/alquiler/report_total_pendientes'
                }
            },
            {
                text: '<i class="fab fa-amazon"></i> Reporte por Productos',
                className: 'btn btn-warning',
                action: function (e, dt, node, config) {
                    window.location.href = '/alquiler/report_by_product'
                }
            },
        ]
        },
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',

            },
            {
                targets: [-1],
                width: '20%',
                render: function (data, type, row) {
                    return '$ ' + data;
                }
            },
            {
                targets: [-2, -3],
                render: function (data, type, row) {
                    return '$ ' + parseFloat(data).toFixed(2);
                }
            },
        ],
        footerCallback: function (row, start, end, display) {
            var api = this.api(), data;

            // Remove the formatting to get integer data for summation
            var intVal = function (i) {
                return typeof i === 'string' ?
                    i.replace(/[$,]/g, '') * 1 :
                    typeof i === 'number' ?
                        i : 0;
            };
            // Total over this page
            pageTotalsiniva = api
                .column(3, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);
            // total full table
            pageTotalsiniva = api.column(3).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);

            // Total over this page
            pageTotaliva = api
                .column(4, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);
            // total full table
            totaliva = api.column(4).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);
// Total over this page
            pageTotalconiva = api
                .column(2, {page: 'current'})
                .data()
                .reduce(function (a, b) {
                    return intVal(a) + intVal(b);
                }, 0);
            // total full table
            totalconiva = api.column(2).data().reduce(function (a, b) {
                return intVal(a) + intVal(b);
            }, 0);


            // Update footer
            $(api.column(2).footer()).html(
                '$ ' + parseFloat(pageTotalsiniva).toFixed(2) + ' ( $ ' + parseFloat(pageTotalsiniva).toFixed(2) + ')'
                // parseFloat(data).toFixed(2)
            );
             $(api.column(4).footer()).html(
                '$ ' + parseFloat(pageTotaliva).toFixed(2) + ' ( $ ' + parseFloat(pageTotaliva).toFixed(2) + ')'
                // parseFloat(data).toFixed(2)
            );
              $(api.column(3).footer()).html(
                '$ ' + parseFloat(pageTotalconiva).toFixed(2) + ' ( $ ' + parseFloat(pageTotalconiva).toFixed(2) + ')'
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
        datos.add(picker);
        // filter_by_date();

    }).on('cancel.daterangepicker', function (ev, picker) {
        picker['key'] = 0;
        datos.add(picker);
    });

}
