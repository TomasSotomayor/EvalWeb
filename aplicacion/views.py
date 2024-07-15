# aplicacion/views.py
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from .models import Usuario, TipoUsuario, TipoProducto, Producto, Compra,Suscripcion,DetalleCompra,Promocion
import traceback
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from datetime import datetime, timedelta
from .forms import TipoUsuarioForm,TipoProductoForm,UsuarioForm,PromocionForm
from django.views.decorators.csrf import csrf_exempt
import json

import os
        
@csrf_exempt
def cerrarsesion(request):
    if request.method == 'POST':
        try:
            if 'tipousuario' in request.session:
                del request.session['tipousuario']
            if 'idUsuario' in request.session:
                del request.session['idUsuario']
            if 'carro' in request.session:
                del request.session['carro']
            return JsonResponse({'estado': 'completado'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                    }
            })

@csrf_exempt
def administrar(request):
    return render(request, 'aplicacion/admin.html')   





@csrf_exempt
def desuscribirse(request):
    if request.method == 'POST':
        try:
            id_usuario = request.session['idUsuario']
            suscripcion = Suscripcion.objects.filter(usuario_id=id_usuario).all()
            if suscripcion:
                suscripcion.delete()
                return JsonResponse({'estado': 'completado'})
            else:
                return JsonResponse({'estado': 'fallido', 'error': 'No hay suscripción activa para este usuario.'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                    }
            })
    else:
        return JsonResponse({'estado': 'fallido'})

@csrf_exempt
def suscribirse(request):
    if request.method == 'POST':
        try:
            id_usuario = request.session['idUsuario']
            fecha_actual = datetime.now()
            fecha_fin = fecha_actual + timedelta(days=30)
            suscripcion = Suscripcion(usuario_id=id_usuario, fecha_inicio=fecha_actual, fecha_fin=fecha_fin)
            suscripcion.save()
            return JsonResponse({'estado': 'completado'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                    }
            })

@csrf_exempt
def recuperardatosusuario(request):
    if request.method == 'POST':
        try:
            id_usuario = request.session['idUsuario']
            usuario = Usuario.objects.get(IdUsuario=id_usuario)
            usuario_dict = model_to_dict(usuario)

            suscrito = Suscripcion.objects.filter(usuario_id=id_usuario).exists()
            if suscrito:
                return JsonResponse({'estado': 'completado', 'usuario': usuario_dict , 'suscrito': True})
            else:
                return JsonResponse({'estado': 'completado', 'usuario': usuario_dict , 'suscrito': False})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                    }
            })
    else:
        return JsonResponse({'estado': 'fallido'})

@csrf_exempt
def miperfil(request):
    return render(request, 'aplicacion/infocuenta.html')


@csrf_exempt
def arbustos(request):
    productos = Producto.objects.raw('''
                SELECT p.*, pr.descuento as descuento, pr.id_promocion as promocion_id
                FROM aplicacion_producto p
                LEFT JOIN aplicacion_promocion pr ON p.IdProducto = pr.id_producto_id
                WHERE tipo_producto_id = %s ''' , [12])
    productos_dict = []
    for producto in productos:
                producto_dict = model_to_dict(producto)
                producto_dict['id_promocion'] = producto.promocion_id if producto.promocion_id else None
                producto_dict['descuento'] = producto.descuento if producto.descuento else 0
                producto_dict['precio_descuento'] = producto.precio - (producto.precio * producto_dict['descuento'] / 100)
                productos_dict.append(producto_dict)
    return render(request, 'aplicacion/arbustos.html',{'productos': productos_dict})

@csrf_exempt
def contacto(request):
    return render(request, 'aplicacion/contacto.html')

@csrf_exempt
def flores(request):
    productos = Producto.objects.raw('''
                SELECT p.*, pr.descuento as descuento, pr.id_promocion as promocion_id
                FROM aplicacion_producto p
                LEFT JOIN aplicacion_promocion pr ON p.IdProducto = pr.id_producto_id
                WHERE tipo_producto_id = %s ''' , [10])
    productos_dict = []
    for producto in productos:
                producto_dict = model_to_dict(producto)
                producto_dict['id_promocion'] = producto.promocion_id if producto.promocion_id else None
                producto_dict['descuento'] = producto.descuento if producto.descuento else 0
                producto_dict['precio_descuento'] = producto.precio - (producto.precio * producto_dict['descuento'] / 100)
                productos_dict.append(producto_dict)
    return render(request, 'aplicacion/flores.html',{'productos': productos_dict})

@csrf_exempt
def index(request):
    return render(request, 'aplicacion/index.html')

@csrf_exempt
def enviarcontacto(request):
    return render(request, 'aplicacion/index.html')

@csrf_exempt
def maceteros(request):
    productos = Producto.objects.raw('''
                SELECT p.*, pr.descuento as descuento, pr.id_promocion as promocion_id
                FROM aplicacion_producto p
                LEFT JOIN aplicacion_promocion pr ON p.IdProducto = pr.id_producto_id
                WHERE tipo_producto_id = %s ''' , [9])
    productos_dict = []
    for producto in productos:
                producto_dict = model_to_dict(producto)
                producto_dict['id_promocion'] = producto.promocion_id if producto.promocion_id else None
                producto_dict['descuento'] = producto.descuento if producto.descuento else 0
                producto_dict['precio_descuento'] = producto.precio - (producto.precio * producto_dict['descuento'] / 100)
                productos_dict.append(producto_dict)
    return render(request, 'aplicacion/maceteros.html',{'productos': productos_dict})

@csrf_exempt
def registro(request):
    return render(request, 'aplicacion/registro.html')

@csrf_exempt
def tierrahoja(request):
    productos = Producto.objects.raw('''
                SELECT p.*, pr.descuento as descuento, pr.id_promocion as promocion_id
                FROM aplicacion_producto p
                LEFT JOIN aplicacion_promocion pr ON p.IdProducto = pr.id_producto_id
                WHERE tipo_producto_id = %s ''' , [11])
    productos_dict = []
    for producto in productos:
                producto_dict = model_to_dict(producto)
                producto_dict['id_promocion'] = producto.promocion_id if producto.promocion_id else None
                producto_dict['descuento'] = producto.descuento if producto.descuento else 0
                producto_dict['precio_descuento'] = producto.precio - (producto.precio * producto_dict['descuento'] / 100)
                productos_dict.append(producto_dict)
    return render(request, 'aplicacion/tierrahoja.html',{'productos': productos_dict})

@csrf_exempt
def mantenedorUsuarios(request):
    usuarios = Usuario.objects.all()
    tipos_usuarios = TipoUsuario.objects.all() 
    return render(request, 'aplicacion/usuario.html', {'usuarios': usuarios , 'tipos_usuarios': tipos_usuarios})

@csrf_exempt
def mantenedorTipoProducto(request):
    tipos_productos = TipoProducto.objects.all()  # Obtiene todos los objetos de TipoUsuario
    return render(request, 'aplicacion/tipoproducto.html', {'tipos_productos': tipos_productos})

@csrf_exempt
def mantenedorProductos(request):
    productos = Producto.objects.all()
    tipos_producto = TipoProducto.objects.all()
    return render(request, 'aplicacion/producto.html' , {'productos': productos , 'tipos_producto': tipos_producto})

@csrf_exempt
def mantenedorTipoUsuario(request):
    tipos_usuarios = TipoUsuario.objects.all() 
    return render(request, 'aplicacion/tipousuario.html', {'tipos_usuarios': tipos_usuarios})

@csrf_exempt
def mantenedorSuscripcion(request):
    usuario = Usuario.objects.all()
    suscripciones = Suscripcion.objects.all()
    return render(request, 'aplicacion/suscripcion.html', {'suscripciones': suscripciones, 'usuarios': usuario})

@csrf_exempt
def mantenedorPromocion(request):
    producto = Producto.objects.all()
    promociones = Promocion.objects.raw('''
                SELECT p.*, pr.nombre as producto_nombre
                FROM aplicacion_promocion p
                LEFT JOIN aplicacion_producto pr ON p.id_producto_id = pr.IdProducto
            '''
            )

    promociones_dict = []
    for promocion in promociones:
                promocion_dict = model_to_dict(promocion)
                promocion_dict['producto_nombre'] = promocion.producto_nombre
                promociones_dict.append(promocion_dict)
    return render(request, 'aplicacion/promocion.html', {'productos': producto, 'promociones': promociones_dict})


@csrf_exempt
def eliminarproductocarrito(request):
    if request.method == 'POST':
        try:
            idproducto = request.POST.get('idproducto')
            carro = request.session.get('carro', {})
            if idproducto in carro['productos']:
                carro['productos'].pop(idproducto, None)
                request.session['carro'] = carro
                return JsonResponse({'estado': 'completado'})
            else:
                return JsonResponse({'error': 'El Producto no esta en el carro'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                    }
            })
    else:
        return JsonResponse({'estado': 'fallido'})

@csrf_exempt
def carrito(request):
    carro = request.session.get('carro', {})
    if carro == {} or carro['productos'] == {}:
        return render(request, 'aplicacion/carrito.html', {'productos': [], 'total': 0})
    else:
        # Initialize an empty list to hold products with discounts
        productos_con_descuento = []

        # Query for products and promotions as before
        productos = Producto.objects.filter(IdProducto__in=carro['productos'].keys())
        promociones = Promocion.objects.filter(id_producto_id__in=carro['productos'].keys())

        for producto in productos:
            descuentoPromocion = 0
            # Check if there is a promotion for the current product
            promocion_filtrada = promociones.filter(id_producto_id=producto.IdProducto)
            if promocion_filtrada:
                descuentoPromocion = promocion_filtrada[0].descuento
            # Create a dictionary for the product and its discount
            producto_con_descuento = {
                'producto': producto,
                'descuentoPromocion': descuentoPromocion
            }
            # Append the dictionary to the list
            productos_con_descuento.append(producto_con_descuento)

        # Calculate the total considering the discounts
        total = sum(p['producto'].precio - p['descuentoPromocion'] for p in productos_con_descuento)

        # Render the template with the modified list of products
    return render(request, 'aplicacion/carrito.html', {'productos': productos_con_descuento, 'total': total})

@csrf_exempt
def editar_promocion(request, pk):
    promocion = get_object_or_404(Promocion, id_promocion=pk)
    if request.method == 'POST':
        form = PromocionForm(request.POST, instance=promocion)
        if form.is_valid():
            form.save()
            return redirect('../../administrar/mantenedorPromocion/')
    else:
        form = PromocionForm(instance=promocion)
    return render(request, 'aplicacion/editar_promocion.html', {'form': form})

@csrf_exempt
def agregarSuscripcion(request):
    if request.method == 'POST':
        try:
            id_usuario = request.POST.get('usuario')
            fecha_inicio_suscripcion = request.POST.get('fechaInicio')
            fecha_fin_suscripcion = request.POST.get('fechaTermino')

            fecha_inicio_nueva = datetime.strptime(fecha_inicio_suscripcion, "%Y-%m-%d").date()
            fecha_fin_nueva = datetime.strptime(fecha_fin_suscripcion, "%Y-%m-%d").date()


            usuario = get_object_or_404(Usuario, pk=id_usuario)

            raw_query = """
            SELECT * FROM aplicacion_suscripcion
            WHERE usuario_id = %s
            AND (
                (fecha_inicio <= %s AND fecha_fin >= %s)
                OR
                (fecha_inicio <= %s AND fecha_fin >= %s)
                OR
                (%s between fecha_inicio AND fecha_fin)
                OR
                (%s between fecha_inicio AND fecha_fin)
                OR
                (fecha_inicio = %s)
            )
            """
            suscripciones_existentes = Suscripcion.objects.raw(raw_query, [id_usuario, fecha_fin_nueva, fecha_inicio_nueva, fecha_fin_nueva, fecha_inicio_nueva, fecha_inicio_nueva, fecha_fin_nueva,fecha_fin_nueva])

            # Verificar si hay resultados
            if len(list(suscripciones_existentes)) > 0:
                return JsonResponse({'estado': 'fallido', 'error': 'Ya existe una suscripción activa en ese rango de fechas para este usuario.'})


            suscripcion = Suscripcion(usuario=usuario, fecha_inicio=fecha_inicio_nueva, fecha_fin=fecha_fin_nueva)
            suscripcion.save()
            return JsonResponse({'estado': 'completado'})

        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})
    




@csrf_exempt
def comprarproductos(request):
    if request.method == 'POST':
        try:
            id_usuario = request.session['idUsuario']
            fecha_actual = datetime.now()
            productos_json = request.POST.get('Productos')
            productos = json.loads(productos_json)

            for producto in productos:
                id_producto = producto['id_producto']
                cantidad = producto['cantidad']
                precio = producto['precio']
                productoValidar = Producto.objects.get(IdProducto=id_producto)
                if productoValidar.stock < int(cantidad):
                    producto_nombre = Producto.objects.get(id_producto=id_producto).nombre
                    return JsonResponse({'estado': 'fallido', 'error': 'No hay suficiente stock de '+ producto_nombre +'.'})

            compra = Compra(usuario_id=id_usuario, fecha_compra=fecha_actual)
            compra.save()

            max_id_compra = Compra.objects.raw('SELECT IdCompra, MAX(IdCompra) as id_compra FROM aplicacion_compra WHERE usuario_id = %s GROUP BY IdCompra ORDER BY IdCompra DESC LIMIT 1', [id_usuario])
            for producto in productos:
                id_producto = producto['id_producto']
                cantidad = producto['cantidad']
                precio = producto['precio']
                Producto.objects.filter(IdProducto=int(id_producto)).update(stock=Producto.objects.get(IdProducto=int(id_producto)).stock - int(cantidad))
                detalle_compra = DetalleCompra(compra_id=max_id_compra[0].id_compra, producto_id=id_producto, cantidad=cantidad, precio_unitario=precio)        
                detalle_compra.save()
            del request.session['carro']
            return JsonResponse({'estado': 'completado'})
            
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name__,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})



# Agregar al carro
@csrf_exempt
def agregaralcarro(request):
    if request.method == 'POST':
            try:
                idproducto = request.POST.get('idproducto')
                

                # Comprueba si existe un usuario con el correo y contraseña proporcionados
                carro = request.session.get('carro', {})

                if 'productos' not in carro:
                    carro['productos'] = {}
                if idproducto in carro['productos']:
                    return JsonResponse({'error': 'El Producto esta en el carro'})
                else:
                    carro['productos'][idproducto] = {'idProducto': idproducto}

                # Guarda el carro actualizado en la sesión
                request.session['carro'] = carro

                return JsonResponse({'estado': 'completado'})
            except Exception as e:
                return JsonResponse({
                    'Excepciones': {
                        'message': str(e),  # Mensaje de la excepción
                        'type': type(e).__name,  # Tipo de la excepción
                        'details': traceback.format_exc()  # Detalles de la excepción
                        }
                })
    else:
            return JsonResponse({'estado': 'fallido'})

@csrf_exempt
def eliminar_suscripcion(request, pk):
    suscripcion = get_object_or_404(Suscripcion,IdSuscripcion=pk)
    if request.method == 'POST':
        suscripcion.delete()
        return redirect('../../../administrar/mantenedorSuscripcion/')
    return render(request, 'aplicacion/confirma_eliminarSuscripcion.html', {'suscripcion': suscripcion})

@csrf_exempt
def eliminar_promocion(request, pk):
    promocion = get_object_or_404(Promocion, id_promocion=pk)
    if request.method == 'POST':
        promocion.delete()
        return redirect('../../../administrar/mantenedorPromocion/')
    return render(request, 'aplicacion/confirma_eliminarPromocion.html', {'promocion': promocion})

@csrf_exempt
def agregarPromocion(request):
    if request.method == 'POST':
        try:
            descripcion = request.POST.get('descripcion')
            producto_id = request.POST.get('producto')
            descuento = request.POST.get('descuento')

    
            producto = Producto.objects.get(IdProducto=producto_id)
            existe_promocion = Promocion.objects.filter(id_producto=producto).exists()
            if existe_promocion:
                return JsonResponse({'estado': 'fallido', 'error': 'Ya existe una promoción para este producto.'})
            promocion = Promocion(descripcion=descripcion, id_producto=producto, descuento=descuento)
            promocion.save()
            return JsonResponse({'estado': 'completado'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})

@csrf_exempt
def obtenersesion(request):
    if request.method == 'POST':
        try:
            tipousuario = request.session.get('tipousuario', None)
            idUsuario = request.session.get('idUsuario', None)
            if tipousuario:
                return JsonResponse({'estado': 'completado', 'tipousuario': tipousuario, 'idUsuario': idUsuario})
            else:
                return JsonResponse({'estado': 'fallido'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})

#iniciar sesion
@csrf_exempt
def iniciarsesion(request):
    if request.method == 'POST':
            try:
                correo = request.POST.get('usuario')
                contrasena = request.POST.get('contrasena')

                # Comprueba si existe un usuario con el correo y contraseña proporcionados
                usuario = Usuario.objects.filter(email=correo, password=contrasena).first()
                if usuario:
                    request.session['tipousuario'] = usuario.tipo_usuario.IdTipoUsuario
                    request.session['idUsuario'] = usuario.IdUsuario
                    return JsonResponse({'estado': 'completado', 'tipo_usuario': usuario.tipo_usuario.IdTipoUsuario})
                else:
                    return JsonResponse({'error': 'Correo o contraseña incorrectos.'})
            except Exception as e:
                return JsonResponse({
                    'Excepciones': {
                        'message': str(e),  # Mensaje de la excepción
                        'type': type(e).__name,  # Tipo de la excepción
                        'details': traceback.format_exc()  # Detalles de la excepción
                        }
                })
    else:
            return JsonResponse({'estado': 'fallido'})


# INICIO VISTAS USUARIO

@csrf_exempt
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'aplicacion/lista_usuarios.html', {'usuarios': usuarios})

@csrf_exempt
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, IdUsuario=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('../../administrar/mantenedorUsuarios/')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'aplicacion/editar_usuario.html', {'form': form})

@csrf_exempt
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, IdUsuario=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('../../administrar/mantenedorUsuarios/')
    return render(request, 'aplicacion/confirma_eliminarUsuario.html', {'usuario': usuario})

@csrf_exempt
def agregarUsuario(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            contrasena = request.POST.get('contrasena')
            tipo_usuario = TipoUsuario.objects.get(IdTipoUsuario=request.POST.get('tipoUsuario'))
            usuario = Usuario(nombre=nombre, email=correo, password=contrasena, tipo_usuario=tipo_usuario)
            usuario.save()
            return JsonResponse({'estado': 'completado'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})
    




# FIN VISTAS USUARIO




# INICIO VISTAS TIPO USUARIO    
@csrf_exempt
def lista_tipos_usuario(request):
    tipos_usuarios = TipoUsuario.objects.all()
    return render(request, 'aplicacion/lista_tipos_usuario.html', {'tipos_usuarios': tipos_usuarios})

@csrf_exempt
def editar_tipo_usuario(request, pk):
    tipo_usuario = get_object_or_404(TipoUsuario, IdTipoUsuario=pk)
    if request.method == 'POST':
        form = TipoUsuarioForm(request.POST, instance=tipo_usuario)
        if form.is_valid():
            form.save()
            return redirect('../../administrar/mantenedorTipoUsuario/')
    else:
        form = TipoUsuarioForm(instance=tipo_usuario)
    return render(request, 'aplicacion/editar_tipo_usuario.html', {'form': form})

@csrf_exempt
def eliminar_tipo_usuario(request, pk):
    tipo_usuario = get_object_or_404(TipoUsuario, IdTipoUsuario=pk)
    if request.method == 'POST':
        tipo_usuario.delete()
        return redirect('../../administrar/mantenedorTipoUsuario/')
    return render(request, 'aplicacion/confirma_eliminarTipoUsuario.html', {'tipo_usuario': tipo_usuario})

    

@csrf_exempt
def agregarTipoUsuario (request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            tipo_usuario = TipoUsuario(nombre=nombre)
            tipo_usuario.save()
            return JsonResponse({'estado': 'completado'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})
# FIN VISTAS TIPO USUARIO





# INICIO VISTAS TIPO Producto 
@csrf_exempt
def lista_tipos_producto(request):
    tipos_producto = TipoProducto.objects.all()
    return render(request, 'aplicacion/lista_tipos_producto.html', {'tipos_productos': tipos_producto})

@csrf_exempt
def editar_tipo_producto(request, pk):
    tipo_producto = get_object_or_404(TipoProducto, IdTipoProducto=pk)
    if request.method == 'POST':
        form = TipoProductoForm(request.POST, instance=tipo_producto)
        if form.is_valid():
            form.save()
            return redirect('../../administrar/mantenedorTipoProducto/')
    else:
        form = TipoProductoForm(instance=tipo_producto)
    return render(request, 'aplicacion/editar_tipo_producto.html', {'form': form})

@csrf_exempt
def eliminar_tipo_producto(request, pk):
    tipo_producto = get_object_or_404(TipoProducto, IdTipoProducto=pk)
    if request.method == 'POST':
        tipo_producto.delete()
        return redirect('../../administrar/mantenedorTipoProducto/')
    return render(request, 'aplicacion/confirma_eliminarTipoProducto.html', {'tipo_producto': tipo_producto})

    
@csrf_exempt
def agregarTipoProducto (request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            tipo_producto = TipoProducto(nombre=nombre)
            tipo_producto.save()
            return JsonResponse({'estado': 'completado'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})
# FIN VISTAS TIPO Producto


# INICIO VISTAS PRODUCTO
@csrf_exempt
def GrabarProducto(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('Nombre')
            tipo_producto_id = request.POST.get('TipoProducto')
            precio = request.POST.get('PrecioUnitario')
            stock = request.POST.get('Stock')

            imagen_archivo = request.FILES.get('Imagen')  
            imagen = f"{nombre}-{imagen_archivo.name}"
            fs = FileSystemStorage(location='static/img/imagenesProducto')
            if fs.exists(imagen):
                return JsonResponse({'error': 'Ya existe un archivo con este nombre, suba otra.'})
            filename = fs.save(imagen, imagen_archivo)
            ruta_completa = fs.url(filename)

            tipo_producto = get_object_or_404(TipoProducto, pk=tipo_producto_id)
            producto = Producto(nombre=nombre, tipo_producto=tipo_producto, precio=precio, stock=stock, imagen=imagen)
            producto.save()
            return JsonResponse({'estado': 'completado'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name__,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})

@csrf_exempt
def BuscarProductoEditar(request):
    if request.method == 'POST':
        try:
            id_producto = request.POST.get('idProducto')
            producto = get_object_or_404(Producto, IdProducto=id_producto)
            
            # Convertir el objeto producto a un diccionario
            producto_dict = model_to_dict(producto)
            # Asegúrate de que el modelo Producto tiene un campo 'tipo_producto' que es una FK a TipoProducto
            tipo_producto_dict = model_to_dict(producto.tipo_producto)
            
            # Agregar el diccionario del tipo de producto al diccionario del producto
            producto_dict['tipo_producto'] = tipo_producto_dict
            
            return JsonResponse({'estado': 'completado', 'producto': producto_dict})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name__,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'})

@csrf_exempt
def lista_producto(request):
    tipos_producto = Producto.objects.all()
    return render(request, 'aplicacion/lista_producto.html', {'tipos_productos': tipos_producto})

@csrf_exempt
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, IdProducto=pk)
    tipos_productos = TipoProducto.objects.all() 
    return render(request, 'aplicacion/editar_producto.html', {'pk': pk , 'producto': producto , 'tipos_productos': tipos_productos})



@csrf_exempt
def ConfirmarEditarProducto(request):
    if request.method == 'POST':
        try:
            id_producto = request.POST.get('idProducto')
            nombre = request.POST.get('Nombre')
            tipo_producto_id = request.POST.get('TipoProducto')
            precio = request.POST.get('PrecioUnitario')
            stock = request.POST.get('Stock')

            imagen_archivo = request.FILES.get('Imagen')  
            tipo_producto = get_object_or_404(TipoProducto, pk=tipo_producto_id)
            producto = Producto.objects.get(IdProducto=id_producto)
            if imagen_archivo is not None:
                imagenBorrar = producto.imagen
                imagen = f"{nombre}-{imagen_archivo.name}"
                fs = FileSystemStorage(location='static/img/imagenesProducto')
                fs.delete(imagenBorrar)
                if fs.exists(imagen):
                    return JsonResponse({'error': 'Ya existe un archivo con este nombre, suba otra.'})
                filename = fs.save(imagen, imagen_archivo)
                ruta_completa = fs.url(filename)
                producto.imagen = imagen

            producto.nombre = nombre
            producto.tipo_producto = tipo_producto
            producto.precio = precio
            producto.stock = stock
            producto.save()
            return JsonResponse({'estado': 'completado'})
        except Exception as e:
            return JsonResponse({
                'Excepciones': {
                    'message': str(e),  # Mensaje de la excepción
                    'type': type(e).__name__,  # Tipo de la excepción
                    'details': traceback.format_exc()  # Detalles de la excepción
                }
            })
    else:
        return JsonResponse({'estado': 'fallido'}) 

@csrf_exempt
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, IdProducto=pk)
    if request.method == 'POST':
        fs = FileSystemStorage(location='static/img/imagenesProducto/')
        if fs.exists(producto.imagen):
             fs.delete(producto.imagen)
        producto.delete()
        return redirect('../../administrar/mantenedorProductos/')
    return render(request, 'aplicacion/confirma_eliminarProducto.html', {'producto': producto})

# FIN VISTAS PRODUCTO








# vistas 