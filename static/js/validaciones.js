$(document).ready(function(){
    $("#registroForm").submit(function(event){
        // Evitar que el formulario se envíe automáticamente
        event.preventDefault();
        
        // Realizar las validaciones
        var rut = $("#rut").val();
        var nombre = $("#nombre").val();
        var apellidoPaterno = $("#apellidoPaterno").val();
        var apellidoMaterno = $("#apellidoMaterno").val();
        
        var genero = $("#genero").val();
        var celular = $("#celular").val();

        // Rut: largo entre 9 y 10 caracteres
        if(rut.length < 9 || rut.length > 10){
            alert("El Rut debe tener entre 9 y 10 caracteres.");
            return;
        }

        // Nombre, Apellidos: largo entre 3 y 20 caracteres
        if(nombre.length < 3 || nombre.length > 20 ||
            apellidoPaterno.length < 3 || apellidoPaterno.length > 20 ||
            apellidoMaterno.length < 3 || apellidoMaterno.length > 20){
            alert("El Nombre y los Apellidos deben tener entre 3 y 20 caracteres.");
            return;
        }

        // Edad: Validación de edad 
    



        
        // Género: seleccionado
        if(genero === ""){
            alert("Por favor, seleccione un Género.");
            return;
        }

        // Celular: largo entre 9 y 12 caracteres
        if(celular.length < 9 || celular.length > 12){
            alert("El Celular debe tener entre 9 y 12 caracteres.");
            return;
        }

        // Si todas las validaciones pasan, se puede enviar el formulario
        alert("¡Registro exitoso!");
        // Aquí podrías enviar el formulario utilizando AJAX o cualquier otro método
    });
});


function EliminarProductoCarrito(Obj){
    var idProducto = $(Obj).parent().parent().find('.idProducto').attr('value');
    var fd = new FormData();
    fd.append("idproducto", idProducto);
    $(Obj).parent().parent().remove();
    $.ajax({
        type: "POST",
        url: "/eliminarproductocarrito/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado') {
                alert('Producto eliminado con éxito');
                actualizarPrecio();
                if ($('#tablaProductos tbody tr').length == 0){
                    window.location.href = '/carrito/';
                }

            } else {
                alert('Falló la eliminación del producto');
            }
        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });
}

function actualizarPrecio(){
    var total = 0;

   $('.precioProducto').each(function() {
        var precio = parseInt($(this).text());
        var cantidad = parseInt($(this).parent().find('.cantidadProducto').val());
        total = total + (precio * cantidad);
    });
    $('#textototal').text("Total: $"+total);

}

function agregarAlCarrito(idProducto){
    var fd = new FormData();
    fd.append("idproducto", idProducto);


    console.log('entre');
    $.ajax({
        type: "POST",
        url: "/agregaralcarro/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado' ) {
                alert('Se agrego al carro');
              
            }
            
            if (response.estado === 'fallido') {
                alert('No se pudo agregar al carro');
             
            }

        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });


}

function crearnavbar(){
    const navbarSuperior = `
<nav class="navbar navbar-expand-lg navbar-taller">
    <div class="container-fluid">
        <div class="navbar-header">
            <a class="navbar-brand" href="/">
                <img src="../../static/img/logo/logo.png" style="max-width:100%;height:auto;" alt="Logo" width="100">
            </a>
        </div>
        <div class="d-flex ml-auto align-items-center">
            <div class="search-bar d-flex align-items-center mr-4">
                <input type="text" placeholder="Buscar..." class="form-control">
                <button type="submit" class="btn btn-primary ml-2">Buscar</button>
            </div>
            <!-- Menú de navegación y botones -->
            <ul class="navbar-nav d-flex align-items-center">
                <li class="nav-item">
                    <a href="/registro/"
                       class="btn"
                       style="background-color: #70bc34; color: rgb(255, 246, 216); margin-right: 10px;">Regístrate</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="btn dropdown-toggle"
                       style="background-color: #70bc34; color: rgb(255, 246, 216); margin-right: 10px;"
                       id="loginDropdown" role="button" data-toggle="dropdown" aria-haspopup="true"
                       aria-expanded="false">Iniciar Sesión</a>
                    <div class="dropdown-menu dropdown-menu-right p-3" aria-labelledby="loginDropdown" style="z-index: 2;">
                        <form class="form" method="post" action="iniciarsesion">
                        <div class="row">
                            <div class="form-group">
                                <label for="username">Usuario</label>
                                <input type="text" class="form-control" id="username"
                                       placeholder="Usuario">
                            </div>
                            <div class="form-group">
                                <label for="password">Contraseña</label>
                                <input type="password" class="form-control" id="password"
                                       placeholder="Contraseña">
                            </div>
                            <button type="button" onclick="iniciarsesion();" class="btn btn-primary">Iniciar Sesión</button>
                            <button type="button" onclick="UsuarioAdmin();" class="btn btn-primary">Usuario Admin</button>
                        </div>
                        </form>
                    </div>
                </li>
                <li class="nav-item">
                    <a href="/"
                       class="btn"
                       style="background-color: #70bc34; color: rgb(255, 246, 216);">Volver Inicio</a>
                </li>
            </ul>
            <ul class="navbar-nav ml-auto">
                <li class="nav-item dropdown">
                    <a class="btn btn-success ml-2"
                    href="/carrito/"
                            style="background-color: #70bc34; color: rgb(255, 246, 216);">Carrito de Compras</a>
                </li>
            </ul>
        </div>
    </div>
</nav>`;
const navbarInferior = `
<nav class="navbar navbar-expand-lg navbar-taller" style="z-index: 1;">
    <div class="container d-flex justify-content-between">
        <a href="/arbustos/" class="btn1" style="background-color: #70bc34; color: rgb(255, 246, 216);">Arbustos</a>
        <a href="/tierrahoja/" class="btn1" style="background-color: #70bc34; color: rgb(255, 246, 216);">Tierra de hojas</a>
        <a href="/flores/" class="btn1" style="background-color: #70bc34; color: rgb(255, 246, 216);">Flores</a>
        <a href="/maceteros/" class="btn1" style="background-color: #70bc34; color: rgb(255, 246, 216);">Maceteros</a>
        <a href="/contacto/" class="btn1" style="background-color: #70bc34; color: rgb(255, 246, 216);">Contacto</a>
    </div>
</nav>`;
    $('#navbarSuperior').html(navbarSuperior);
    $('#navbarInferior').html(navbarInferior);


    
}


function iniciarsesion(){
    var contrasena = $('#password').val();
    var usuario = $('#username').val();
    if (usuario === '' || contrasena === '') {
        return alert( '\nPor favor, rellene los campos.');
    }
    var fd = new FormData();
    fd.append("usuario", usuario);
    fd.append("contrasena", contrasena);


    console.log('entre');
    $.ajax({
        type: "POST",
        url: "/iniciarsesion/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado' && response.tipo_usuario == 1) {
                alert('Inicio de sesión exitoso');
                window.location.href = '/administrar/';
            }
            if(response.estado === 'completado' && response.tipo_usuario != 1) {
                alert('Inicio de sesión exitoso');
                window.location.href = '/';

            }
            if (response.estado === 'fallido') {
                alert('Inicio de sesión fallido');
                window.location.href = '/';
            }

        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });




}


function agregarPromocion(){
    var descripcion = $('#descripcion').val();
    var descuento = $('#descuento').val();
    var producto = $('#cmbProducto').val();
    var msg = '';
    if (descripcion === '' || descuento === '' || producto == '0') {
        msg = msg + '\nPor favor, rellene todos los campos.';
    }
    if (isNaN(parseInt(descuento)) || parseInt(descuento) <= 0 || parseInt(descuento) > 100) {
        msg = msg + '\nPor favor, introduzca un descuento valido.';
    }
    if (msg != '') {
        alert(msg);
        return;
    }
    var fd = new FormData();
    fd.append("descripcion", descripcion);
    fd.append("descuento", descuento);
    fd.append("producto", producto);
    $.ajax({
        type: "POST",
        url: "/agregarPromocion/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado') {
                alert('Promoción agregada exitosamente');
                window.location.href = '/administrar/mantenedorPromocion/';
            }
            if (response.estado === 'fallido') {
                alert('No se pudo agregar la promoción');
                window.location.href = '/administrar/mantenedorPromocion/';
            }

        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });

}
    
function agregarSuscripcion(){
    var usuario = $('#cmbUsuario').val();
    var fechaInicio = $('#fecha_inicio').val();
    var fechaTermino = $('#fecha_fin').val();
    var msg = '';

    if (usuario == '0' || fechaInicio === '' || fechaTermino === '') {
        msg = msg + '\nPor favor, rellene todos los campos.';
    }
    if (fechaInicio > fechaTermino) {
        msg = msg + '\nLa fecha de inicio no puede ser mayor a la fecha de término.';
    }
    var fd = new FormData();
    fd.append("usuario", usuario);
    fd.append("fechaInicio", fechaInicio);
    fd.append("fechaTermino", fechaTermino);
    if (msg != '') {
        alert(msg);
        return;
    }
    $.ajax({
        type: "POST",
        url: "/agregarSuscripcion/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado') {
                alert('Suscripción agregada exitosamente');

                window.location.href = '/administrar/mantenedorSuscripcion/';
            }
            if (response.estado === 'fallido') {
                alert('No se pudo agregar la suscripción');
                window.location.href = '/administrar/mantenedorSuscripcion/';
            }

        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });

}





function agregarUsuario(){
    nombre = $('#nombre').val();
    correo = $('#email').val();
    contrasena = $('#password').val();
    tipoUsuario = $('#cmbTipoUsuario').val();

    if (nombre === '' || correo === '' || contrasena === '' || tipoUsuario === '') {
        return alert('Por favor, rellene los campos.');
    }
    if (tipoUsuario == '0') {
        return alert('Por favor, seleccione un tipo de usuario.');
    }


    var fd = new FormData();
    fd.append("nombre", nombre);
    fd.append("correo", correo);
    fd.append("contrasena", contrasena);
    fd.append("tipoUsuario", tipoUsuario);
    $.ajax({
        type: "POST",
        url: "/agregarUsuario/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado') {
                alert('Usuario agregado exitosamente');
                window.location.href = '/administrar/mantenedorUsuarios/';
            }
            if (response.estado === 'fallido') {
                alert('No se pudo agregar el usuario');
                window.location.href = '/administrar/mantenedorUsuarios/';
            }

        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });

}


function agregarTipoUsuario(){
    if ($('#nombre').val() === '') {
        return alert('Por favor, rellene los campos.');
    }

    nombre = $('#nombre').val();
    var fd = new FormData();
    fd.append("nombre", nombre);
    $.ajax({
        type: "POST",
        url: "/agregarTipoUsuario/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado') {
                alert('Tipo de usuario agregado exitosamente');
                window.location.href = '/administrar/mantenedorTipoUsuario/';
            }
            if (response.estado === 'fallido') {
                alert('No se pudo agregar el tipo de usuario');
                window.location.href = '/administrar/mantenedorTipoUsuario/';
            }

        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });

}

// agregar tipo producto
function agregarTipoProducto(){
    nombre = $('#nombre').val();
    var fd = new FormData();
    fd.append("nombre", nombre);
    $.ajax({
        type: "POST",
        url: "/agregarTipoProducto/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado') {
                alert('Tipo de producto agregado exitosamente');
                window.location.href = '/administrar/mantenedorTipoProducto/';
            }
            if (response.estado === 'fallido') {
                alert('No se pudo agregar el tipo de producto');
                window.location.href = '/administrar/mantenedorTipoProducto/';
            }

        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });

}





function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function grabarProducto(){
    var msg = '';
    var nombre = $('#nombre').val();
    var precio = $('#precio').val();
    var stock = $('#stock').val();
    var tipo = $('#cmbTipoProducto').val();
    var archivo = $('#ImagenProducto').prop('files')[0];

    if (nombre.toString() === '' || precio.toString() === '' || stock.toString() === ''|| tipo.toString() === '') {
        msg = msg + '\nPor favor, rellene todos los campos.';
    }
    if (tipo.toString() === '0') {
        msg = msg + '\nPor favor, seleccione un tipo de producto.';
    }
    if (isNaN(parseFloat(precio)) || parseFloat(precio) <= 0) {
        msg = msg + '\nPor favor, introduzca un precio valido.';
    }
    if (isNaN(parseInt(stock)) || parseInt(stock) < 0) {
        msg = msg + '\nPor favor, introduzca un stock valido.';
    }
    if (archivo == null) {
        msg = msg + '\nPor favor, seleccione una imagen.';
    }
    else if (archivo.name.split('.').pop().toLowerCase() != 'jpg' && archivo.name.split('.').pop().toLowerCase() != 'jpeg' && archivo.name.split('.').pop().toLowerCase() != 'png') {
        msg = msg + '\nPor favor, seleccione una imagen con formato jpg, jpeg o png.';
    }

    if (msg != '') {
        alert(msg);
        return;
    }
    var fd = new FormData();
    fd.append("Nombre", nombre);
    fd.append("PrecioUnitario", precio);
    fd.append("Stock", stock);
    fd.append("TipoProducto", tipo);
    fd.append("Imagen", archivo);

    $.ajax({
        type: "POST",
        url: "/GrabarProducto/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado') {
                alert('Producto creado con éxito');
                window.location.href = '/administrar/mantenedorProductos/';
            } else {
                alert('Falló la creación del producto');
            }
        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });
}

function buscarProductoEditar(idProducto){
var fd = new FormData();
fd.append("idProducto", idProducto);
$.ajax({
    type: "POST",
    url: "/BuscarProductoEditar/",
    data: fd,
    contentType: false,
    processData: false,
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    success: function (response) {
        console.log(response);
        if (response.Excepciones != null) {
            alert('Ha ocurrido un error inesperado');
            console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
            return;
        }
        if (response.error != null) {
            alert(response.error);
            return;
        }
        if(response.estado === 'completado') {
            $('#nombre').val(response.producto.nombre);
            $('#precio').val(response.producto.precio);
            $('#stock').val(response.producto.stock);
            $('#cmbTipoProducto').val(response.producto.tipo_producto.IdTipoProducto);
            $('#divImagen').html('<img src="../../../static/img/imagenesProducto/' + response.producto.imagen + '" alt="Imagen actual del producto" style="max-width: 100%; height: auto;">');
        } else {
            alert('Falló la búsqueda del producto');
        }
    },
    error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
    failure: function (response) { alert(response); }
});



}


function confirmarEditarProducto(){
    var msg = '';
    var nombre = $('#nombre').val();
    var precio = $('#precio').val();
    var stock = $('#stock').val();
    var tipo = $('#cmbTipoProducto').val();
    var archivo = $('#ImagenProducto').prop('files')[0];

    if (nombre.toString() === '' || precio.toString() === '' || stock.toString() === ''|| tipo.toString() === '') {
        msg = msg + '\nPor favor, rellene todos los campos.';
    }
    if (tipo.toString() === '0') {
        msg = msg + '\nPor favor, seleccione un tipo de producto.';
    }
    if (isNaN(parseFloat(precio)) || parseFloat(precio) <= 0) {
        msg = msg + '\nPor favor, introduzca un precio valido.';
    }
    if (isNaN(parseInt(stock)) || parseInt(stock) < 0) {
        msg = msg + '\nPor favor, introduzca un stock valido.';
    }
    if (archivo != null) {
        if (archivo.name.split('.').pop().toLowerCase() != 'jpg' && archivo.name.split('.').pop().toLowerCase() != 'jpeg' && archivo.name.split('.').pop().toLowerCase() != 'png') {
            msg = msg + '\nPor favor, seleccione una imagen con formato jpg, jpeg o png.';
        }
    }

    if (msg != '') {
        alert(msg);
        return;
    }
    var fd = new FormData();
    fd.append("Nombre", nombre);
    fd.append("PrecioUnitario", precio);
    fd.append("Stock", stock);
    fd.append("TipoProducto", tipo);
    fd.append("Imagen", archivo);
    fd.append("idProducto", $('#idProducto').text());

    $.ajax({
        type: "POST",
        url: "/ConfirmarEditarProducto/",
        data: fd,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        success: function (response) {
            console.log(response);
            if (response.Excepciones != null) {
                alert('Ha ocurrido un error inesperado');
                console.log(response.Excepciones.message + '\n' + response.Excepciones.type + '\n' + response.Excepciones.details);
                return;
            }
            if (response.error != null) {
                alert(response.error);
                return;
            }
            if(response.estado === 'completado') {
                alert('Producto editado con éxito');
                window.location.href = '/administrar/mantenedorProductos/';
            } else {
                alert('Falló la edición del producto');
                window.location.href = '/administrar/mantenedorProductos/';

            }

        }
    });


}
function UsuarioAdmin(){
    $('#username').val('admin@admin.cl');
    $('#password').val('1234');
    iniciarsesion();
}