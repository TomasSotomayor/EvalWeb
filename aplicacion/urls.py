from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'), 
    path('carrito/', views.carrito, name= 'carrito'),
    path('agregaralcarro/', views.agregaralcarro, name= 'agregaralcarro'),
    path('eliminarproductocarrito/', views.eliminarproductocarrito, name= 'eliminarproductocarrito'),
    path('arbustos/', views.arbustos, name='arbustos'),
    path('contacto/', views.contacto, name='contacto'),
    path('flores/', views.flores, name='flores'),
    path('maceteros/', views.maceteros, name='maceteros'),
    path('registro/', views.registro, name='registro'),
    path('tierrahoja/', views.tierrahoja, name='tierrahoja'),
    path('enviarcontacto/', views.enviarcontacto, name='enviarcontacto'),
    path('admin/', admin.site.urls),
    path('iniciarsesion/' , views.iniciarsesion, name= 'iniciarsesion'),
    path('administrar/', views.administrar, name= 'administrar'),
    path('administrar/mantenedorUsuarios/', views.mantenedorUsuarios, name='mantenedorUsuarios'),
    path('administrar/mantenedorProductos/', views.mantenedorProductos, name='mantenedorProductos'),
    path('administrar/mantenedorTipoUsuario/', views.mantenedorTipoUsuario, name='mantenedorTipoUsuario'),
    path('administrar/mantenedorTipoProducto/', views.mantenedorTipoProducto, name='mantenedorTipoProducto'),
    path('administrar/mantenedorSuscripcion/', views.mantenedorSuscripcion, name='mantenedorSuscripcion'),
    path('administrar/mantenedorPromocion/', views.mantenedorPromocion, name='mantenedorPromocion'),
    path('BuscarProductoEditar/', views.BuscarProductoEditar, name='BuscarProductoEditar'),
    path('ConfirmarEditarProducto/', views.ConfirmarEditarProducto, name='ConfirmarEditarProducto'),
    path('obtenersesion/', views.obtenersesion, name='obtenersesion'),
    path('cerrarsesion/', views.cerrarsesion, name='cerrarsesion'),
    path('agregarPromocion/', views.agregarPromocion, name='agregarPromocion'),
    path('GrabarProducto/', views.GrabarProducto, name='GrabarProducto'),
    path('eliminar_promocion//<int:pk>/', views.eliminar_promocion, name='eliminar_promocion'),
    path('editar_promocion/<int:pk>/', views.editar_promocion, name='editar_promocion'),
    path('agregarSuscripcion/', views.agregarSuscripcion, name='agregarSuscripcion'),
    path('eliminar_suscripcion//<int:pk>/', views.eliminar_suscripcion, name='eliminar_suscripcion'),
    

    path('mantenedorUsuarios/lista-usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('editar-usuario/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar-usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('agregarUsuario/', views.agregarUsuario, name='agregarUsuario'),
    


    path('mantenedorTipoUsuario/lista-tipos-usuario/', views.lista_tipos_usuario, name='lista_tipos_usuario'),
    path('editar-tipo-usuario/<int:pk>/', views.editar_tipo_usuario, name='editar_tipo_usuario'),
    path('eliminar-tipo-usuario/<int:pk>/', views.eliminar_tipo_usuario, name='eliminar_tipo_usuario'),
    path('agregarTipoUsuario/', views.agregarTipoUsuario, name='agregarTipoUsuario'),


    path('mantenedorTipoProducto/lista-tipos-producto/', views.lista_tipos_producto, name='lista_tipos_producto'),
    path('editar-tipo-producto/<int:pk>/', views.editar_tipo_producto, name='editar_tipo_producto'),
    path('eliminar-tipo-producto/<int:pk>/', views.eliminar_tipo_producto, name='eliminar_tipo_producto'),
    path('agregarTipoProducto/', views.agregarTipoProducto, name='agregarTipoProducto'),


    path('mantenedorTipoProducto/lista-producto/', views.lista_producto, name='lista_producto'),
    path('editar-producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    

    
]



