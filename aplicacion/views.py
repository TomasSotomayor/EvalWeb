# aplicacion/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def registro(request):
    # Add your registration logic here
    return render(request, 'registro.html')
