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
$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
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
                    0: 'Ningun Filtro seleccionados',
                },
                activeMessage: 'Filtros activos (%d)',
                emptyPanes: 'No existen suficientes datos para generar filtros :('

            }
        },
        dom: 'l<"toolbar">' + "<br>" + 'Bfrtip ',
        buttons: [
            {
                className: 'btn-default my_class', extend: 'searchPanes', config: {
                    cascadePanes: true,
                    viewTotal: true,
                    layout: 'columns-4'
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
                    columns: [0, 1, 2],
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
                    doc.content[1].table.widths = [35, 180, 180];
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
                targets: [0, 1, 2, 3],
                class: 'text-center'
            },
            // {
            //     searchPanes: {
            //         show: true,
            //     },
            //     targets: [0, 1, 2, 3, 5, 6]
            // },
            // {
            //     searchPanes: {
            //         show: true,
            //         options: [
            //             {
            //                 label: 'Menos de 20',
            //                 value: function (rowData, rowIdx) {
            //                     return rowData[4] < 20;
            //                 }
            //             },
            //             {
            //                 label: '20 a 30',
            //                 value: function (rowData, rowIdx) {
            //                     return rowData[4] <= 30 && rowData[4] >= 20;
            //                 }
            //             },
            //             {
            //                 label: '30 a 40',
            //                 value: function (rowData, rowIdx) {
            //                     return rowData[4] <= 40 && rowData[4] >= 30;
            //                 }
            //             },
            //             {
            //                 label: '40 a 50',
            //                 value: function (rowData, rowIdx) {
            //                     return rowData[4] <= 50 && rowData[4] >= 40;
            //                 }
            //             },
            //             {
            //                 label: '50 a 60',
            //                 value: function (rowData, rowIdx) {
            //                     return rowData[4] <= 60 && rowData[4] >= 50;
            //                 }
            //             },
            //             {
            //                 label: 'Mas de 60',
            //                 value: function (rowData, rowIdx) {
            //                     return rowData[4] > 60;
            //                 }
            //             },
            //         ]
            //     },
            //     targets: [4],
            // },
        ]

    });
    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/servicio/eliminar', 'Esta seguro que desea eliminar este servicio?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar el servicio!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});