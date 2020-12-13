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
$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        ajax: {
            url: '/user/groups',
            type: 'POST',
            data: {'action': 'list'},
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "permisos"},
             {"data": "id"},
        ],
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
                text: '<i class="fa fa-file-pdf"></i> Reporte PDF',
                className: 'btn btn-danger btn-space',
                extend: 'pdfHtml5',
                //filename: 'dt_custom_pdf',
                orientation: 'landscape', //portrait
                pageSize: 'A4', //A3 , A5 , A6 , legal , letter
                download: 'open',
                exportOptions: {
                    columns: [1, 2, 3, 4, 5, 6],
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
                    doc.content[1].table.widths = [150, '*', 90, 70, 180, 70];
                    doc.styles.tableBodyEven.alignment = 'center';
                    doc.styles.tableBodyOdd.alignment = 'center';
                }
            },
            {
                text: '<i class="fa fa-file-excel"></i> Reporte Excel', className: "btn btn-success btn-space",
                extend: 'excel'
            }
        ],
        },

       dom: "<'row'<'col-sm-12 col-md-12'B>>" +
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>"+
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        columnDefs: [
            {
                targets: '__all',
                class: 'text-center'
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a style="color: white" type="button" class="btn btn-warning btn-xs" rel="edit" ' +
                        'data-toggle="tooltip" href="/material/editar/'+ data +'" title="Editar Datos"><i class="fa fa-edit"></i></a>' + ' ';
                    var del = '<a type="button" class="btn btn-danger btn-xs"  style="color: white" rel="del" ' +
                        'data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                    return edit + del

                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var html = '';
                    $.each(row.permisos, function (key, value) {
                        html += '<span class="badge badge-success">' + value.nombre + '</span>'+' '
                    });
                    return html;

                }
            },
        ],
        // createdRow: function (row, data, dataIndex) {
        //     console.log(data);
        //     if (data.producto_base.stock >= 51) {
        //         $('td', row).eq(4).find('span').addClass('badge badge-success').attr("style", "color: white");
        //     } else if (data.producto_base.stock >= 10) {
        //         $('td', row).eq(4).find('span').addClass('badge badge-warning').attr("style", "color: white");
        //     } else if (data.producto_base.stock <= 9) {
        //         $('td', row).eq(4).find('span').addClass('badge badge-danger').attr("style", "color: white");
        //     }
        //
        // }

    });
    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data.id, 'action': 'delete'};
        save_estado('Alerta',
            '/material/nuevo', 'Esta seguro que desea eliminar este material?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar el material!', 'far fa-smile-wink', function () {
                    datatable.ajax.reload(null, false);
                })
            });
    });

    $('#nuevo').on('click', function () {
        window.location.replace('/user/newgroup')

    })
});