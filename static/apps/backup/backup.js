var parametros = {};
$(document).ready(function () {
    $('#form').on('submit', function (e) {
        e.preventDefault();
        // save_with_ajax('Alerta!', '/database_backup/nuevo/', 'Esta seguro que desea realizar un respaldo de base de datos?',
        //     '1', location.href = "/" );
        // // save_with_ajax('Alerta!', '/database_backup/nuevo/', 'Esta seguro que desea realizar un respaldo de base de datos?',
        // //     null, location.href = "/database_backup/lista");
        parametros = {
            'action': $('input[name="action"]').val()
        };
        save_with_ajax('Alerta',
            '/database_backup/nuevo', 'Esta seguro que desea realizar un respaldo de base de datos?', parametros, function (response) {
                location.href = '/database_backup/lista';

            });

    });

});
