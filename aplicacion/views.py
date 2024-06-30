# aplicacion/views.py
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from .models import Usuario, TipoUsuario, TipoProducto, Producto, Compra,Suscripcion,DetalleCompra
import traceback
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from .forms import TipoUsuarioForm,TipoProductoForm,UsuarioForm

import os

def administrar(request):
    return render(request, 'aplicacion/admin.html')
     

def arbustos(request):
    productos = Producto.objects.raw('SELECT * FROM aplicacion_producto WHERE tipo_producto_id = %s', [12])
    return render(request, 'aplicacion/arbustos.html',{'productos': productos})


def contacto(request):
    return render(request, 'aplicacion/contacto.html')

def flores(request):
    productos = Producto.objects.raw('SELECT * FROM aplicacion_producto WHERE tipo_producto_id = %s', [10])
    return render(request, 'aplicacion/flores.html',{'productos': productos})

def index(request):
    return render(request, 'aplicacion/index.html')

def enviarcontacto(request):

    
    return render(request, 'aplicacion/index.html')

def maceteros(request):
    productos = Producto.objects.raw('SELECT * FROM aplicacion_producto WHERE tipo_producto_id = %s', [9])
    return render(request, 'aplicacion/maceteros.html',{'productos': productos})

def registro(request):
    return render(request, 'aplicacion/registro.html')

def tierrahoja(request):
    productos = Producto.objects.raw('SELECT * FROM aplicacion_producto WHERE tipo_producto_id = %s', [11])
    return render(request, 'aplicacion/tierrahoja.html',{'productos': productos})

def mantenedorUsuarios(request):
    usuarios = Usuario.objects.all()
    tipos_usuarios = TipoUsuario.objects.all() 
    return render(request, 'aplicacion/usuario.html', {'usuarios': usuarios , 'tipos_usuarios': tipos_usuarios})

def mantenedorTipoProducto(request):
    tipos_productos = TipoProducto.objects.all()  # Obtiene todos los objetos de TipoUsuario
    return render(request, 'aplicacion/tipoproducto.html', {'tipos_productos': tipos_productos})

def mantenedorProductos(request):
    productos = Producto.objects.all()
    tipos_producto = TipoProducto.objects.all()
    return render(request, 'aplicacion/producto.html' , {'productos': productos , 'tipos_producto': tipos_producto})

def mantenedorTipoUsuario(request):
    tipos_usuarios = TipoUsuario.objects.all() 
    return render(request, 'aplicacion/tipousuario.html', {'tipos_usuarios': tipos_usuarios})

def iniciarsesion(request):
    if request.method == 'POST':
            try:
                correo = request.POST.get('usuario')
                contrasena = request.POST.get('contrasena')

                # Comprueba si existe un usuario con el correo y contraseña proporcionados
                usuario = Usuario.objects.filter(email=correo, password=contrasena).first()
                if usuario:
                    # request.session['tipousuario'] = usuario.tipousuario.id_tipo_usuario
                    # request.session['idUsuario'] = usuario.id_usuario
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

def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'aplicacion/lista_usuarios.html', {'usuarios': usuarios})

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

def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, IdUsuario=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('../../administrar/mantenedorUsuarios/')
    return render(request, 'aplicacion/confirma_eliminarUsuario.html', {'usuario': usuario})

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
def lista_tipos_usuario(request):
    tipos_usuarios = TipoUsuario.objects.all()
    return render(request, 'aplicacion/lista_tipos_usuario.html', {'tipos_usuarios': tipos_usuarios})

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

def eliminar_tipo_usuario(request, pk):
    tipo_usuario = get_object_or_404(TipoUsuario, IdTipoUsuario=pk)
    if request.method == 'POST':
        tipo_usuario.delete()
        return redirect('../../administrar/mantenedorTipoUsuario/')
    return render(request, 'aplicacion/confirma_eliminarTipoUsuario.html', {'tipo_usuario': tipo_usuario})

    

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
def lista_tipos_producto(request):
    tipos_producto = TipoProducto.objects.all()
    return render(request, 'aplicacion/lista_tipos_producto.html', {'tipos_productos': tipos_producto})

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

def eliminar_tipo_producto(request, pk):
    tipo_producto = get_object_or_404(TipoProducto, IdTipoProducto=pk)
    if request.method == 'POST':
        tipo_producto.delete()
        return redirect('../../administrar/mantenedorTipoProducto/')
    return render(request, 'aplicacion/confirma_eliminarTipoProducto.html', {'tipo_producto': tipo_producto})

    

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

def lista_producto(request):
    tipos_producto = Producto.objects.all()
    return render(request, 'aplicacion/lista_producto.html', {'tipos_productos': tipos_producto})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, IdProducto=pk)
    tipos_productos = TipoProducto.objects.all() 
    return render(request, 'aplicacion/editar_producto.html', {'pk': pk , 'producto': producto , 'tipos_productos': tipos_productos})




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