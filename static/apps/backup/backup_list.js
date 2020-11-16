$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        dom: 'l<"toolbar">' + "<br>" + 'Bfrtip ',
        buttons: [

        ],
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',
            },
        ]
    });
    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/database_backup/eliminar', 'Esta seguro que desea eliminar este respaldo?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar el respaldo!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });

    $('#delete_all').on('click', function () {
        var parametros = {'action': 'delete_access_all'};
        save_estado('Alerta',
            '/database_backup/lista', 'Esta seguro que desea eliminar todos los respaldos?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar los respaldos!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });

    })

});
