# evalweb/urls.py

from django.urls import path,include
from aplicacion import views

urlpatterns = [
    path('', include('aplicacion.urls') ),
    path('registro/', views.registro, name='registro'),
    path('administrar/', include('aplicacion.urls')),
]
