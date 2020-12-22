var datatable;
$(function () {
    datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        dom: "<'row'<'col-sm-12 col-md-12'B>>" +
            "<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'list'},
            dataSrc: ""
        },
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
                    text: 'Eliminar todos los respaldos <i class="fas fa-trash">',
                    className: 'btn btn-danger btn-sm',
                    attr: {id: 'delete_all'},
                    action: function (e, dt, node, config) {
                        delete_All();
                    }
                }]
        },
        columns: [
            {data: 'id'},
            {data: "fecha"},
            {data: "archive"},
            {data: "archive_path"}
        ],
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',
            },
             {
                targets: [-1],
                render: function (data, type, row) {
                    var descargar = '<a type="button" class="btn btn-success btn-xs" data-toggle="tooltip"\n' +
                        '                       title="Descargar"\n' +
                        '                       href="'+row.archive_path+ '"><i class="fas fa-download"></i></a>'+ ' ';
                    var eliminar = '<a type="button" rel="del" class="btn btn-danger btn-xs btn-round" ' +
                        'style="color: white" data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>';
                    return descargar+eliminar;
                }
            },
        ]
    });
    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data.id};
        save_estado('Alerta',
            '/database_backup/eliminar', 'Esta seguro que desea eliminar este respaldo?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar el respaldo!', 'far fa-smile-wink', function () {
                     datatable.ajax.reload(null,false);
                })
            });
    });

    function delete_All() {
        if (! datatable.data().any()) return false;
        var parametros = {'action': 'delete_access_all'};
        save_estado('Alerta',
            '/database_backup/lista', 'Esta seguro que desea eliminar todos los respaldos?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar los respaldos!', 'far fa-smile-wink', function () {
                    datatable.ajax.reload(null,false);
                })
            });

    }

    $('#nuevo').on('click', function (e) {
        e.preventDefault();
        var parametros = {'action': 'add'};
        save_estado('Alerta',
            '/database_backup/nuevo', 'Esta seguro que desea realizar un respaldo de base de datos?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al al generar el respaldo de base de datos!', 'far fa-smile-wink', function () {
                    datatable.ajax.reload(null, false);
                })
            });

    })


});
