// script del menu responsive Abrir el menu
var btnMobile = document.getElementById('btn-mobile')
btnMobile.addEventListener('click', function (e) {
    e.preventDefault()
    let mySidenav = document.getElementById("mySidenav")
    mySidenav.classList.toggle("openOffCanvas")
})

// script del menu responsive sticky menu

var nav = document.getElementById('mySidenav')

window.addEventListener('scroll', function () {
    if (window.pageYOffset > nav.offsetTop) {
        nav.classList.add('nav-fixed')
    } else {
        nav.classList.remove('nav-fixed')
    }
})
// script del menu responsive effecto accordeon
var submenu = document.getElementsByClassName('link-submenu')

for (var i = 0; i < submenu.length; i++) {
    submenu[i].onclick = function () {
        var content = this.nextElementSibling

        if (content.style.maxHeight) {
            content.style.maxHeight = null
        } else {
            content.style.maxHeight = content.scrollHeight + "px"
        }

    }
}

// script del slider de producto
let activeImg = 0

function slider(n) {
    let images = document.getElementsByClassName("slider-item")

    for (i = 0; i < images.length; i++) {

        if (images[i].className.includes("active")) {
            images[i].className = images[i].className.replace("active", "")

            break
        }
    }

    activeImg = n
    images[n].className += " active"
}

function next() {
    activeImg++
    if (activeImg > 2) {
        activeImg = 0
    }
    slider(activeImg)
}

function previus() {
    activeImg--
    if (activeImg < 0) {
        activeImg = 2
    }
    slider(activeImg)
}


// script de la navegacipon por tabs
let tabs = Array.prototype.slice.apply(document.querySelectorAll('.tabs-item'));
let panels = Array.prototype.slice.apply(document.querySelectorAll('.tab-panel'));

function insertmapa() {
    var mat = document.getElementById('mapa').textContent;
    console.log(mat);

    document.getElementById('mapa2').innerHTML = mat;

}

function container_popular(Array) {
    $.ajax({
        url: '/producto/lista',
        type: 'POST',
        data: {'action': 'sitio'},
        dataSrc: "",
    }).done(function (data) {
        var html = '';
        $.each(data, function (key, value) {
            html += ' <div class="column is-full">+' +
                '<div class="separator"></div></div>' +
                '<div class="column is-half-tablet is-one-third-desktop column-half">' +
                '<div class="card">' +
                '<img src="' + value['imagen'] + '" alt="">' +
                '<div class="card-info">' +
                '<h4 class="has-text-black has-text-centered has-text-weight-bold"> ' + value['info'] + '</h4>' +
                '<p class="has-text-centered">' + value['descripcion'] + '</p>' +
                '<p class="has-text-centered"> <strong>Precio de venta:</strong> ' + value['pvp'] + '</p>' +
                '<p class="has-text-centered"> <strong>Precio de Alquiler:</strong> ' + value['pvp_alq'] + '</p>' +
                '<p class="has-text-centered"> <strong>Precio de Confeccion:</strong> ' + value['pvp_confec'] + '</p>' +
                '<div class="card-buttons">' +
                '<a href="#" class="btn btn--mini-rounded"><i class="zmdi zmdi-shopping-cart"></i></a>' +
                '<a href="#" class="btn btn--mini-rounded"><i class="zmdi zmdi-favorite-outline"></i></a>' +
                '<a href="producto.html" class="btn btn--mini-rounded"><i class="zmdi zmdi-eye"></i></a>' +
                '</div>' +
                '</div>' +
                '</div>'
        });
        $('#pop').html(html);
    });

}

