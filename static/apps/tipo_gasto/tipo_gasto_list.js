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
            {"data": "id"}
        ],
        language:
            {
                url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json'
            },
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                width: '10%'
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a style="color: white" type="button" class="btn btn-warning btn-sm" rel="edit" ' +
                        'data-toggle="tooltip" title="Editar Datos"><i class="fa fa-user-edit"></i></a>' + ' ';
                    var del = '<a type="button" class="btn btn-danger btn-sm"  style="color: white" rel="del" ' +
                        'data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                    return edit + del

                }
            },
        ]
    });
    $('#datatable tbody')
        .on('click', 'a[rel="del"]', function () {
            action = 'delete';
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id};
            parametros['action'] = action;
            save_estado('Alerta',
                window.location.pathname, 'Esta seguro que desea eliminar este tipo de Gasto?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar este tipo de Gasto!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false)
                    })
                })
        })
        .on('click', 'a[rel="edit"]', function () {
            $('#exampleModalLabel').html('<i class="fas fa-edit"></i>&nbsp;Edicion de un registro');
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('input[name="nombre"]').val(data.nombre);
            $('input[name="descripcion"]').val(data.descripcion);
            $('#Modal').modal('show');
            action = 'edit';
            pk = data.id;
        });


    $('#nuevo').on('click', function () {
        $('#exampleModalLabel').html('<i class="fas fa-plus"></i>&nbsp;Nuevo registro de un Tipo de Gasto');
        $('#Modal').modal('show');
        action = 'add';
        pk = '';
    });

    //enviar formulario de nuevo tipo de gasto
    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', action);
        parametros.append('id', pk);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/tipo_gasto/nuevo', 'Esta seguro que desea guardar este tipo de gasto?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este tipo de gasto!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        reset();
                        datatable.ajax.reload(null, false);
                    });
                });
        }
    });
});