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
            url: '/inventario/data',
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
            url: '/inventario/data',
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

            }
        },
        order: [[4, "desc"]],
        dom: 'l<"toolbar">' + "<br>" + 'Bfrtip ',
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
                text: '<i class="fa fa-file-pdf"></i> Reporte PDF',
                className: 'btn btn-danger my_class',
                extend: 'pdfHtml5',
                //filename: 'dt_custom_pdf',
                orientation: 'landscape', //portrait
                pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                download: 'open',
                exportOptions: {
                    columns: [1, 2, 3, 4, 5, 6, 7],
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
                    doc.content[1].table.widths = ['*', '*', '*', '*', '*','*', '*'];
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
                }
            },
            {
                text: '<i class="fa fa-file-excel"></i> Reporte Excel', className: "btn btn-success my_class",
                extend: 'excel'
            }
        ],
        columnDefs: [
            {
                searchPanes: {
                    show: false,
                },
                targets: [0, 1, 2],
            },
            {
                searchPanes: {
                    show: true,
                },
                targets: [3, 4, 5, 6, 7],
            },
            {
                searchPanes: {
                    show: true,
                    options: [
                        {
                            label: 'FINALIZADA',
                            value: function (rowData, rowIdx) {
                                return rowData[5] === 'FINALIZADA';
                            }
                        },
                        {
                            label: 'DEVUELTA',
                            value: function (rowData, rowIdx) {
                                return rowData[5] === 'DEVUELTA';
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
                            label: 'Menos de $ 10',
                            value: function (rowData, rowIdx) {
                                return rowData[3] < 10;
                            }
                        },
                        {
                            label: '$ 10 a $ 50',
                            value: function (rowData, rowIdx) {
                                return rowData[3] <= 50 && rowData[3] >= 10;
                            }
                        },
                        {
                            label: '$ 50 a $ 100',
                            value: function (rowData, rowIdx) {
                                return rowData[3] <= 100 && rowData[3] >= 50;
                            }
                        },
                        {
                            label: '$ 100 a $ 200',
                            value: function (rowData, rowIdx) {
                                return rowData[3] <= 200 && rowData[3] >= 100;
                            }
                        },
                        {
                            label: '$ 200 a $ 300',
                            value: function (rowData, rowIdx) {
                                return rowData[3] <= 300 && rowData[3] >= 200;
                            }
                        },
                        {
                            label: '$ 300 a $ 400',
                            value: function (rowData, rowIdx) {
                                return rowData[3] <= 400 && rowData[3] >= 300;
                            }
                        },
                        {
                            label: '$ 400 a $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[3] <= 500 && rowData[3] >= 400;
                            }
                        },
                        {
                            label: 'Mas de $ 500',
                            value: function (rowData, rowIdx) {
                                return rowData[3] > 500;
                            }
                        },
                    ]
                },
                targets: [3],
            },
            {
                targets: '_all',
                class: 'text-center',

            },
            {
                targets: [-1],
                class: 'text-center',
                width: "8%",
                render: function (data, type, row) {
                    return  '<a type="button" rel="devolver" class="btn btn-danger btn-sm btn-round" style="color: white" data-toggle="tooltip" title="Eliminar"><i class="fa fa-times"></i></a>' + ' ';;
                }
            },
            {
                targets: [2, -2],
                render: function (data, type, row) {
                    return '<span>' + data + '</span>';
                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data[2] === 'No vendido' && data[7] === 'En Stock') {
                $('td', row).eq(2).find('span').addClass('badge bg-success').attr("style", "color: white");
                $('td', row).eq(7).find('span').addClass('badge bg-success').attr("style", "color: white");
            } else {
                $('td', row).eq(7).find('span').addClass('badge bg-danger').attr("style", "color: white");
                $('td', row).eq(8).find('a[rel="devolver"]').hide();
            }

        }
    });
    $('#datatable tbody').on('click', 'a[rel="devolver"]', function () {
        $('.tooltip').remove();
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data[0]};
        save_estado('Alerta',
            '/inventario/eliminar', 'Esta seguro que desea eliminar este producto del inventario?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar el producto del inventario', 'far fa-smile-wink', function () {
                    datatable.ajax.reload(null, false);
                })
            });
    });


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