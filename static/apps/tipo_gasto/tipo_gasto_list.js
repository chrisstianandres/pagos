$(function () {
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        language:
            {
              url:  '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
       columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                width: '10%'
            }
        ]
    });
    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/tipo_gasto/eliminar', 'Esta seguro que desea eliminar este tipo de gasto?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});