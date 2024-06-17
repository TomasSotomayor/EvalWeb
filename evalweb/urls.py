# evalweb/urls.py

from django.urls import path
from aplicacion import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),  # Ensure this line is present
    # other paths if present
]
