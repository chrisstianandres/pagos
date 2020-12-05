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
            {"data": "tipo.nombre"},
            {"data": "tipo.descripcion"},
            {"data": "serie"},
            {"data": "estado"},
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
                        'data-toggle="tooltip" href="/maquina/editar/' + data + '" title="Editar Datos"><i class="fa fa-user-edit"></i></a>' + ' ';
                    var del = '<a type="button" class="btn btn-danger btn-sm"  style="color: white" rel="del" ' +
                        'data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                    return edit + del

                }
            },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data.estado === 0) {
                $('td', row).eq(4).html('<span class = "badge badge-success" style="color: white "> DISPONIBLE </span>');
            } else if (data.estado === 1) {
                $('td', row).eq(4).html('<span class = "badge badge-danger" style="color: white "> EN USO </span>');
            }

        }
    });
    $('#datatable tbody')
        .on('click', 'a[rel="del"]', function () {
            action = 'delete';
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id};
            parametros['action'] = 'delete';
            save_estado('Alerta',
                '/maquina/nuevo', 'Esta seguro que desea eliminar esta maquina?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar esta maquina!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false)
                    })
                })
        });


    $('#nuevo').on('click', function () {
        window.location.replace('/maquina/nuevo')
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
                '/maquina/nuevo', 'Esta seguro que desea guardar esta maquina?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar esta maquina!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        reset();
                        datatable.ajax.reload(null, false);
                    });
                });
        }
    });


});