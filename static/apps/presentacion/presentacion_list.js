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
        ],
    });
    $('#datatable tbody').on('click', 'a[rel="del"]', function () {
        var tr = datatable.cell($(this).closest('td, li')).index();
        var data = datatable.row(tr.row).data();
        var parametros = {'id': data['0']};
        save_estado('Alerta',
            '/presentacion/eliminar', 'Esta seguro que desea eliminar esta presentacion?', parametros,
            function () {
                menssaje_ok('Exito!', 'Exito al eliminar la presentacion!', 'far fa-smile-wink', function () {
                    location.reload();
                })
            });
    });
});