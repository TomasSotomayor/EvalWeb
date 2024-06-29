from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'), 
    path('arbustos/', views.arbustos, name='arbustos'),
    path('contacto/', views.contacto, name='contacto'),
    path('flores/', views.flores, name='flores'),
    path('maceteros/', views.maceteros, name='maceteros'),
    path('registro/', views.registro, name='registro'),
    path('tierrahoja/', views.tierrahoja, name='tierrahoja'),
    path('enviarcontacto/', views.enviarcontacto, name='enviarcontacto'),
    path('admin/', admin.site.urls),
    path('iniciarsesion/' , views.iniciarsesion, name= 'iniciarsesion'),
    # Otras rutas de URL aquí si las tienes
]



