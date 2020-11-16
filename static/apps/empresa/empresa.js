$(document).ready(function () {
    $('#id_nombre').attr('readonly', true);
    $('#id_ciudad').attr('readonly', true);
    $('#id_ruc').attr('readonly', true);
    $('#id_correo').attr('readonly', true);
    $('#id_direccion').attr('readonly', true);
    $('#id_telefono').attr('readonly', true);
    $('#id_indice').TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '%'
    }).attr('readonly', true);
    $('#editar').on("click", editar);
    $('input[name="iva"]').TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '%'
    }).attr('disabled', true);
});

function editar() {
    $('#guardar').show();
    $('#editar').hide();
    $('#id_nombre').attr('readonly', false);
    $('#id_ciudad').attr('readonly', false);
    $('#id_ruc').attr('readonly', false);
    $('#id_correo').attr('readonly', false);
    $('#id_direccion').attr('readonly', false);
    $('#id_iva').attr('disabled', false);
    $('#id_telefono').attr('readonly', false);
}