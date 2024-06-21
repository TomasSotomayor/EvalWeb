# aplicacion/views.py

from django.shortcuts import render

def arbustos(request):
    return render(request, 'aplicacion/arbustos.html')

def contacto(request):
    return render(request, 'aplicacion/contacto.html')

def flores(request):
    return render(request, 'aplicacion/flores.html')

def index(request):
    return render(request, 'aplicacion/index.html')

def maceteros(request):
    return render(request, 'aplicacion/maceteros.html')

def registro(request):
    return render(request, 'aplicacion/registro.html')

def tierrahoja(request):
    return render(request, 'aplicacion/tierrahoja.html')
