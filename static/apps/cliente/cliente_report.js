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
        'end_date': ''
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
            url: '/cliente/data_report',
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
        order: [[2, "asc"]],
        ajax: {
            url: '/cliente/data_report',
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

        dom: 'l<"toolbar">' + "<br>" + 'Bfrtip ',
        //"<'row'<'col-md-6'l><'col-md-6'Bf>>"
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
                text: '<i class="far fa-file-pdf"></i> Reporte PDF',
                className: 'btn btn-danger',
                extend: 'pdfHtml5',
                footer: true,
                //filename: 'dt_custom_pdf',
                orientation: 'landscape', //portrait
                pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                download: 'open',
                exportOptions: {
                    columns: ':visible',
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
                    doc.content[1].table.widths = [50,70,150, 70, 120, 60, 150, 70];
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
        ],
        columnDefs: [
            {
                searchPanes: {
                    show: false,
                },
                targets: [0, 1],
            },
            {
                searchPanes: {
                    show: true,
                },
                targets: [2],
            },

            {
                targets: '_all',
                class: 'text-center',

            },
        ],
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
