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
        'action': 'list',
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
        responsive: true,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: datos.fechas,
            dataSrc: ""
        },
        dom: "<'row'<'col-sm-12 col-md-12'B>>" +
            "<'row'<'col-sm-12 col-md-6'l>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        buttons: {
            dom: {
                button: {
                    className: 'float-md-right',

                },
                container: {
                    className: 'buttons-container'
                }
            },
            buttons: [
                {
                    text: '<i class="fa fa-file-pdf"></i> Reporte PDF',
                    className: 'btn btn-danger my_class',
                    extend: 'pdfHtml5',
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
                        doc.content[1].table.widths = [50, '*', '*', '*', '*'];
                        doc.styles.tableBodyEven.alignment = 'center';
                        doc.styles.tableBodyOdd.alignment = 'center';
                    }
                },
                {
                    text: '<i class="fa fa-file-excel"></i> Reporte Excel', className: "btn btn-success my_class",
                    extend: 'excel'
                },
                {
                    className: 'btn btn-info',
                    text: '<i class="far fa-keyboard"></i> &nbsp;Tipo de Gasto</a>',
                    action: function (e, dt, node, config) {
                        window.location.href = '/tipo_gasto/lista'
                    }
                },
            ],
        },
        columns: [
            {"data": "id"},
            {"data": "fecha_pago"},
            {"data": "tipo_gasto.nombre"},
            {"data": "valor"},
            {"data": "detalle"},
            {"data": "id"}
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                render: function (data, type, row) {

                    var devolver = '<a type="button" rel="del" class="btn btn-danger btn-sm btn-round" style="color: white" data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>';
                    var editar = '<a type="button" rel="edit" class="btn btn-success btn-sm btn-round" style="color: white" data-toggle="tooltip" title="Editar"><i class="fa fa-edit"></i></a>' + ' ';
                    return editar + devolver;
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$ ' + parseFloat(data).toFixed(2);
                }
            },
        ],
    });
    $('#datatable tbody')
        .on('click', 'a[rel="del"]', function () {
            action = 'delete';
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id};
            parametros['action'] = action;
            save_estado('Alerta',
                '/gasto/nuevo', 'Esta seguro que desea eliminar este gasto?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar este gasto!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false)
                    })
                })
        })
        .on('click', 'a[rel="edit"]', function () {
            $('#exampleModalLabel').html('<i class="fas fa-edit"></i>&nbsp;Edicion de un registro');
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            console.log(data);
            $('input[name="fecha_pago"]').val(data.fecha_pago).attr('readonly', false).daterangepicker({
                singleDatePicker: true,
                showDropdowns: true,
                minYear: 1901,
                maxDate: new Date(),
                locale: {
                    format: 'DD-MM-YYYY',
                    applyLabel: '<i class="fas fa-search"></i> Aplicar',
                    cancelLabel: '<i class="fas fa-times"></i> Cancelar',
                },
            });
            $('input[name="valor"]').val(data.valor);
            $('input[name="detalle"]').val(data.detalle);
            $('select[name="tipo_gasto"]').val(data.tipo_gasto.id).trigger('change');
            $('#Modal').modal('show');
            action = 'edit';
            pk = data.id;
        });
    //boton agregar cliente
    $('#nuevo').on('click', function () {
        $('#exampleModalLabel').html('<i class="fas fa-plus"></i>&nbsp;Nuevo registro de un gasto ');
        $('#Modal').modal('show');
        action = 'add';
        pk = '';
    });

    //enviar formulario de nuevo cliente
    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', action);
        parametros.append('id', pk);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/gasto/nuevo', 'Esta seguro que desea guardar este gasto?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este gasto!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        reset();
                        datatable.ajax.reload(null, false);
                    });
                });
        }
    });
});

function daterange() {
    $('input[name="fecha"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-search"></i> Buscar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        },
        maxDate: new Date(),
    }).on('apply.daterangepicker', function (ev, picker) {
        picker['key'] = 1;
        datos.add(picker);
        // filter_by_date();

    }).on('cancel.daterangepicker', function (ev, picker) {
        picker['key'] = 0;
        datos.add(picker);

    });

}
