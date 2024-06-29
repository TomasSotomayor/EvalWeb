# aplicacion/views.py
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from .models import Usuario, TipoUsuario, TipoProducto, Producto, Compra,Suscripcion,DetalleCompra
import traceback
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from .forms import TipoUsuarioForm,TipoProductoForm

import os

def administrar(request):
    return render(request, 'aplicacion/admin.html')
     

def arbustos(request):
    return render(request, 'aplicacion/arbustos.html')

def contacto(request):
    return render(request, 'aplicacion/contacto.html')

def flores(request):
    return render(request, 'aplicacion/flores.html')

def index(request):
    return render(request, 'aplicacion/index.html')

def enviarcontacto(request):

    
    return render(request, 'aplicacion/index.html')

def maceteros(request):
    return render(request, 'aplicacion/maceteros.html')

def registro(request):
    return render(request, 'aplicacion/registro.html')

def tierrahoja(request):
    return render(request, 'aplicacion/tierrahoja.html')

def mantenedorUsuarios(request):
    return render(request, 'aplicacion/usuario.html')

def mantenedorTipoProducto(request):
    tipos_productos = TipoProducto.objects.all()  # Obtiene todos los objetos de TipoUsuario
    return render(request, 'aplicacion/tipoproducto.html', {'tipos_productos': tipos_productos})

def mantenedorProductos(request):
    return render(request, 'aplicacion/producto.html')

def mantenedorTipoUsuario(request):
    tipos_usuarios = TipoUsuario.objects.all()  # Obtiene todos los objetos de TipoUsuario
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