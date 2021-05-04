var datatable;

$(function () {
    datatable = $("#datatable").DataTable({
        responsive: true,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'list'},
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
                    text: '<i class="fa fa-file-pdf"></i> PDF',
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
                        doc.content[1].table.widths = ['*', '*', '*'];
                        doc.styles.tableBodyEven.alignment = 'center';
                        doc.styles.tableBodyOdd.alignment = 'center';
                    }
                },
                {
                    text: '<i class="fa fa-file-excel"></i> Excel', className: "btn btn-success my_class",
                    extend: 'excel'
                },
            ],
        },
        columns: [
            {"data": "id"},
            {"data": "talla"},
            {"data": "eqv_letra"},
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
            }
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
                '/talla/nuevo', 'Esta seguro que desea eliminar esta talla?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar esta talla!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false)
                    })
                })
        })
        .on('click', 'a[rel="edit"]', function () {
            $('#exampleModalLabel').html('<i class="fas fa-edit"></i>&nbsp;Edicion de un registro');
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('input[name="talla"]').val(data.talla);
            $('input[name="eqv_letra"]').val(data.eqv_letra);
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
                '/talla/nuevo', 'Esta seguro que desea guardar esta talla?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta talla!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        datatable.ajax.reload(null, false);
                    });
                });
        }
    });


      $('#Modal').on('hidden.bs.modal', function () {
        reset_form('form');
    });
     $('#id_talla_num').keypress(function (e) {
        if (e.which !== 8 && e.which !== 0 && (e.which < 48 || e.which > 57)) {
            return false;
        }
    });//Para solo numeros
    $('#id_eqv_letra').keypress(function (e) {
        if (e.which >= 48 && e.which <= 57) {
            return false;
        }
    });  //Para solo letras


});
