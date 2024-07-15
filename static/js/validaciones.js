

var GL_SESION_VALIDA = 0;
var GL_SUSCRITO = 0;




function EliminarProductoCarrito(Obj){
    var idProducto = $(Obj).parent().parent().find('.idProducto').data('idproducto');
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



function comprarProductos(){
    console.log('entre comprar');
    var msg = '';
    var fd = new FormData();
    var total = 0;
    var arrayProductos = [];
    $("#tablaProductos tbody tr").each(function() {
            if ($(this).find('.cantidadProducto').val() <= 0) {
                msg = msg + '\nPor favor, introduzca una cantidad valida para el producto '+ $(this).find('.idProducto').text() +'.';
            }
            else if (parseInt($(this).find('.cantidadProducto').val()) > parseInt($(this).find('.stockProducto').text())) {
                msg = msg + '\nLa cantidad del producto '+ $(this).find('.idProducto').text() +' no puede ser mayor al stock.';
            }
        
            var descuento = parseInt($(this).find('.descuentoProducto').text());
            var id_producto = $(this).find('.idProducto').data('idproducto');
            var cantidad = $(this).find('.cantidadProducto').val();
            var precio = $(this).find('.precioProducto').text();   
            console.log('id_producto: '+id_producto);
            console.log('cantidad: '+cantidad);
            console.log('precio: '+precio);    
            precio = parseInt(precio) * (100 - descuento) * parseInt(cantidad) / 100; 
            arrayProductos.push({id_producto: id_producto, cantidad: cantidad, precio: precio});
            
    });
    console.log(arrayProductos);
    console.log(JSON.stringify(arrayProductos));
    fd.append('Productos', JSON.stringify(arrayProductos));
    if (msg != '') {
        alert(msg);
        return;
    }



    $.ajax({
        type: "POST",
        url: "/comprarproductos/",
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
                alert('Compra realizada con éxito');
                window.location.href = '/carrito/';
            } else {
                alert('Falló la compra');
            }
        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });
}


function actualizarPrecio(){
    var total = 0;
    var descontado = 0;
   $('.precioProducto').each(function() {
        var precio = parseInt($(this).text());
        var descuento = parseInt($(this).parent().find('.descuentoProducto').text());
        var cantidad = parseInt($(this).parent().find('.cantidadProducto').val());
        descontado = descontado + (precio * cantidad * descuento / 100);
        total = total + (precio * ( 100 - descuento) / 100 * cantidad);
    });
    $('#descuento').text("Descuento: $"+descontado);
    if (GL_SUSCRITO == 1) { 
        descontado = descontado + total * 0.1;
        total = total * 0.9;
        $('#suscrito').text("Suscrito: Si");
    }
    else {
        $('#suscrito').text("Suscrito: No ");

    }
    $('#descuento').text("Descuento: $"+descontado);
    $('#textototal').text("Total: $"+total);

}

function agregarAlCarrito(idProducto){
    var fd = new FormData();
    fd.append("idproducto", idProducto);
    if (GL_SESION_VALIDA==0) {

        alert('Debe iniciar sesion');
        return;

    }

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
    if (GL_SESION_VALIDA == 1) {
    var navbarSuperior = `
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
                    <a onclick="cerrarSesion();"
                       class="btn"
                       style="background-color: #70bc34; color: rgb(255, 246, 216); margin-right: 10px;">Cerrar Sesion</a>
                </li>
                <li class="nav-item">
                    <a href="/miperfil/"
                          class="btn"
                            style="background-color: #70bc34; color: rgb(255, 246, 216); margin-right: 10px;">Mi Perfil</a>
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
var navbarInferior = `
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
    if (GL_SESION_VALIDA == 0) {
        var navbarSuperior = `
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
                                    <button type="button" onclick="UsuarioCliente();" class="btn btn-primary">Usuario Cliente</button>
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
        


        var navbarInferior = `
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

    
}


function recuperarDatosUsuario(){
    $.ajax({
        type: "POST",
        url: "/recuperardatosusuario/",
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
                var nombre = response.usuario.nombre.split(' ')[0];
                var apellido = response.usuario.nombre.split(' ')[1] ? response.usuario.nombre.split(' ')[1] : '';
                $('#nombre').val(nombre);
                $('#apellido').val(apellido);
                $('#email').val(response.usuario.email);
                if (response.suscrito == true) {
                    $('#botonSuscripcion').text('Desuscribirse');
                    $('#botonSuscripcion').attr('onclick', 'desuscribirse();');
                    GL_SUSCRITO = 1;
                    actualizarPrecio();
                }
                if (response.suscrito == false) {
                    $('#botonSuscripcion').text('Suscribirse por 10$');
                    $('#botonSuscripcion').attr('onclick', 'suscribirse();');
                    GL_SUSCRITO = 0;
                }
            } else {
                alert('Falló la recuperación de datos');
            }
        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });
}


function desuscribirse(){
    $.ajax({
        type: "POST",
        url: "/desuscribirse/", 
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
                alert('Desuscripción realizada con éxito');
                window.location.href = '/miperfil/';
            } else {
                alert('Falló la desuscripción');
            }
        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });
}


function suscribirse(){
    $.ajax({
        type: "POST",
        url: "/suscribirse/",
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
                alert('Suscripción realizada con éxito');
                window.location.href = '/miperfil/';
            } else {
                alert('Falló la suscripción');
            }
        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });
}

function obtenerSesion(){
    $.ajax({
        type: "POST",
        url: "/obtenersesion/",
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
            if(response.estado === 'completado' && response.tipousuario == null) {
               console.log('entre tipo nulo');
               GL_SESION_VALIDA = 0;
               crearnavbar();

            }
            if(response.estado === 'completado' && response.tipousuario != null) {
                console.log('entre tipo no nulo');
                GL_SESION_VALIDA = 1;
                crearnavbar();
            }
            if (response.estado === 'fallido') {
                console.log('entre fallido');
                GL_SESION_VALIDA = 0;
                crearnavbar();
            }
            
        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });

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
    //ksaidwkd


    function RegistrarseFormulario(){
        console.log(1);
        var nombre = $('#nombre').val();
        var email = $('#e-mail').val();
        var contrasena = $('#Contrasena').val();
        var msg = '';
        if (nombre === '' || email === '' || contrasena == '') {
            msg = msg + '\nPor favor, rellene todos los campos.';
        }

        if (msg != '') {
            alert(msg);
            return;
        }
        var fd = new FormData();
        fd.append("nombre", nombre);
        fd.append("email", email);
        fd.append("contrasena", contrasena);
        $.ajax({
            type: "POST",
            url: "/RegistrarseFormulario/",
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
                    alert('Registrado exitosamente');
                    window.location.href = '/';
                }
                if (response.estado === 'fallido') {
                    alert('No se pudo registrar');
                    window.location.href = '/';
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


function cerrarSesion(){
    $.ajax({
        type: "POST",
        url: "/cerrarsesion/",
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
                alert('Sesión cerrada con éxito');
                window.location.href = '/';
            } else {
                alert('Falló el cierre de sesión');
            }
        },
        error: function (XMLHttpRequest, text, error) { ; alert(XMLHttpRequest.responseText); },
        failure: function (response) { alert(response); }
    });
}


function UsuarioCliente(){
    $('#username').val('cliente@cliente.cl');
    $('#password').val('1234');
    iniciarsesion();
}
