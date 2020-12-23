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
    var action = '';
    var pk = '';
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'list'},
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "tipo"},
            {"data": "num_doc"},
            {"data": "correo"},
            {"data": "telefono"},
            {"data": "direccion"},
            {"data": "id"}
        ],
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
        dom: "<'row'<'col-sm-12 col-md-12'B>>" +
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>"+
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
         buttons: {
            dom: {
                button: {
                    className: '',

                },
                container: {
                    className: 'float-md-right'
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
                        columns: [0, 1, 2, 3, 4, 5, 6],
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
                        doc.content[1].table.widths = [35, '*', 55, 90, 180, 70, 150];
                        doc.styles.tableBodyEven.alignment = 'center';
                        doc.styles.tableBodyOdd.alignment = 'center';
                    }
                },
                {
                    text: '<i class="fa fa-file-excel"></i> Reporte Excel',
                    className: "btn btn-success btn-space float-right",
                    extend: 'excel'
                }
            ]
        },
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a style="color: white" type="button" class="btn btn-warning btn-xs" rel="edit" ' +
                        'data-toggle="tooltip" title="Editar Datos"><i class="fa fa-user-edit"></i></a>' + ' ';
                    var del = '<a type="button" class="btn btn-danger btn-xs"  style="color: white" rel="del" ' +
                        'data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                    return edit + del

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
                '/proveedor/nuevo', 'Esta seguro que desea eliminar este proveedor?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar este proveedor!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false)
                    })
                })
        })
        .on('click', 'a[rel="edit"]', function () {
            $('#exampleModalLabel').html('<i class="fas fa-edit"></i>&nbsp;Edicion de un registro');
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('input[name="nombre"]').val(data.nombre);
            $('select[name="tipo"]').val(data.tipo_val).prop('disabled', true);
            $('input[name="num_doc"]').val(data.num_doc).attr('readonly', true);
            $('input[name="correo"]').val(data.correo);
            $('input[name="telefono"]').val(data.telefono);
            $('input[name="direccion"]').val(data.direccion);
            $('#Modal').modal('show');
            action = 'edit';
            pk = data.id;
        });


    //boton agregar proveedor
    $('#nuevo').on('click', function () {
        $('#exampleModalLabel').html('<i class="fas fa-plus"></i>&nbsp;Nuevo registro de un Proveedor ');
        $('input[name="num_doc"]').attr('readonly', false);
        $('select[name="tipo"]').attr('disabled', false);
        $('#Modal').modal('show');
        action = 'add';
        pk = '';
    });

    //enviar formulario de nuevo cliente
    $('#form').on('submit', function (e) {
        e.preventDefault();
        $('select[name="tipo"]').attr('disabled', false);
        var parametros = new FormData(this);
        parametros.append('action', action);
        parametros.append('id', pk);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/proveedor/nuevo', 'Esta seguro que desea guardar este proveedor?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este proveedor!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        reset();
                        datatable.ajax.reload(null, false);
                    });
                });
        }
    });
});