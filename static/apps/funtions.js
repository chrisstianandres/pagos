function borrar_todo_alert(title, content, callback, callback2) {
    $.confirm({
        title: title,
        icon: 'fas fa-exclamation-triangle',
        type: 'red',
        typeAnimated: true,
        content: content,
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    callback();
                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red'
            },
        }
    });
}

function save_with_ajax(title, url, content, parametros, callback) {
    $.confirm({
        theme: 'modern',
        icon: 'fas fa-exclamation-circle',
        title: title,
        type: 'blue',
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        data: parametros,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        menssaje_error('Error', data.error, 'fas fa-exclamation-circle');

                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    });
                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red',
                action: function () {

                }
            }
        }
    });
}

function callback(response) {
    printpdf('Alerta!', '¿Desea generar el comprobante en PDF?', function () {
        window.open('/venta/printpdf/' + response['id'], '_blank');
        // location.href = '/venta/printpdf/' + response['id'];
        localStorage.clear();
        location.href = '/venta/lista';
    }, function () {
        localStorage.clear();
        location.href = '/venta/lista';
    })

}

function callback_2(response, entidad) {
    printpdf('Alerta!', '¿Desea generar el comprobante en PDF?', function () {
        window.open('/' + entidad + '/printpdf/' + response['id'], '_blank');
        localStorage.clear();
        location.href = '/' + entidad + '/lista';
    }, function () {
        localStorage.clear();
        location.href = '/' + entidad + '/lista';
    })

}

function save_estado(title, url, content, parametros, callback) {
    $.confirm({
        theme: 'modern',
        type: 'red',
        icon: 'fas fa-exclamation-circle',
        title: title,
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        data: parametros,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        menssaje_error(data.error, data.content, 'fa fa-times-circle');
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    });
                    //

                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red',
                action: function () {
                }
            }
        }
    });
}

function printpdf(title, content, callback, cancel) {
    $.confirm({
            theme: 'modern',
            type: 'blue',
            icon: 'fas fa-exclamation-circle',
            title: title,
            content: content,
            columnClass: 'small',
            draggable: true,
            buttons: {
                si: {
                    text: '<i class="fas fa-check"></i> Si',
                    btnClass: 'btn-blue',
                    action: function () {
                        callback();
                    }
                },
                no: {
                    text: '<i class="fas fa-times"></i> No',
                    btnClass: 'btn-red',
                    action: function () {
                        cancel();
                    }
                }
            }
        }
    );
}

function menssaje_error(title, content, icon, callback) {
    var obj = $.confirm({
        theme: 'modern',
        icon: icon,
        title: title,
        type: 'red',
        content: content,
        draggable: true,
        buttons: {
            info: {
                text: '<i class="fas fa-check"></i> Ok',
                btnClass: 'btn-blue'
            },
        }
    });
    setTimeout(function () {
        // some point in future.
        obj.close();
    }, 3000);
}

function error_login(title, content, icon, callback) {
    $.confirm({
        theme: 'modern',
        icon: icon,
        title: title,
        type: 'red',
        content: content,
        draggable: true,
        buttons: {
            info: {
                text: '<i class="fas fa-check"></i> Ok',
                btnClass: 'btn-blue',
                action: function () {
                    callback();
                }

            },
        }
    });
}

function menssaje_ok(title, content, icon, callback) {
    $.confirm({
        theme: 'modern',
        icon: icon,
        type: 'green',
        title: title,
        content: content,
        draggable: true,
        buttons: {
            info: {
                text: '<i class="fas fa-check"></i> Ok',
                btnClass: 'btn-blue',
                action: function (data) {
                    callback(data);
                }
            },
        }
    });
}

function login(url, parametros, callback, callback2) {
    $.ajax({
        dataType: 'JSON',
        type: 'POST',
        url: url,
        data: parametros,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            callback();
            return false;
        }
        error_login('Error', data.error, 'fas fa-exclamation-circle', callback2);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    })


}

function save_with_ajax2(title, url, content, parametros, callback) {
    $.confirm({
        theme: 'modern',
        icon: 'fas fa-exclamation-circle',
        title: title,
        type: 'blue',
        content: content,
        columnClass: 'small',
        draggable: true,
        buttons: {
            si: {
                text: '<i class="fas fa-check"></i> Si',
                btnClass: 'btn-blue',
                action: function () {
                    $.ajax({
                        dataType: 'JSON',
                        type: 'POST',
                        url: url,
                        processData: false,
                        contentType: false,
                        data: parametros,
                    }).done(function (data) {
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        menssaje_error_form('Error', data.error, 'fas fa-exclamation-circle');

                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    });
                }
            },
            no: {
                text: '<i class="fas fa-times"></i> No',
                btnClass: 'btn-red',
                action: function () {

                }
            }
        }
    });
}

function reset() {
    $("#form")[0].reset();
    var validator = $("#form").validate();
    validator.resetForm();
    $('.is-valid').removeClass('is-valid');
    $('.is-invalid').removeClass('is-invalid');
}

function menssaje_error_form(title, content, icon, callback) {
    var html = '<ul>';
    $.each(content, function (key, value) {
        html += '<li>' + key + ': ' + value + '</li>'
    });
    html += '</ul>';
    $.confirm({
        theme: 'modern',
        icon: icon,
        title: title,
        type: 'red',
        content: html,
        draggable: true,
        buttons: {
            info: {
                text: '<i class="fas fa-check"></i> Ok',
                btnClass: 'btn-blue'
            },
        }
    });
}


function borrar_producto_carito(title, content, callback) {
    var obj = $.dialog({
        icon: 'fa fa-spinner fa-spin',
        title: title,
        content: content,
        type: 'blue',
        typeAnimated: true,
        draggable: true,
        onClose: function () {
            callback();
        },
    });
    setTimeout(function () {
        // some point in future.
        obj.close();
    }, 2000);


}

function validar() {
    jQuery.validator.addMethod("val_ced", function (value, element) {
        if (value.length === 10 || value.length === 13) {
            $.ajax({
                type: "POST",
                url: '/verificar/',
                data: {'data': value.toString()},
                dataType: 'json',
                success: function (data) {
                    if (!data.hasOwnProperty('error')) {
                        $(element).addClass("is-valid").removeClass("is-invalid");
                        return false;
                    }
                    $(element).addClass("is-invalid").removeClass("is-valid");
                },
            })
        }
        return true;
        // return this.optional(element) || /^[a-z," "]+$/i.test(value);
    }, "");

}